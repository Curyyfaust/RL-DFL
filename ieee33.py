import pandapower.networks as pn
import pandapower as pp
import numpy as np
import matplotlib.pyplot as plt

def DFLieee33(wind_power, sunny_power):
    pi_G = 10
    pi_T = 20
    
    
    net = pn.case33bw()  # IEEE33
    
    # 放大所有负荷
    net.load['p_mw'] *= 1.5
    net.load['q_mvar'] *= 1.5
    
    # 将线路阻抗除以2
    net.line['r_ohm_per_km'] /= 2
    net.line['x_ohm_per_km'] /= 2
    
    # 记录原始可再生能源容量
    original_wind_total = wind_power * 2  # 2个风电节点
    original_solar_total = sunny_power * 2  # 2个太阳能节点
    
    # 风电 - 设置为可控制的静态发电机
    wind_buses = [18, 25]
    for bus in wind_buses:
        pp.create_sgen(net, bus=bus-1, p_mw=wind_power, q_mvar=0.0,
                      controllable=True, max_p_mw=wind_power, min_p_mw=0.0,
                      name=f"Wind_{bus}")
    
    # 太阳能 - 设置为可控制的静态发电机
    solar_buses = [6, 15]
    for i, bus in enumerate(solar_buses):
        pp.create_sgen(net, bus=bus-1, p_mw=sunny_power, q_mvar=0.0,
                      controllable=True, max_p_mw=sunny_power, min_p_mw=0.0,
                      name=f"Solar_{bus}")
    
    # DG 发电机
    dg_buses = [7, 13, 17]
    dg_bus_indices = [bus - 1 for bus in dg_buses]
    for i in dg_bus_indices:
        pp.create_sgen(net, bus=i, p_mw=1.0, q_mvar=0.0, name=f"DG at Bus {i+1}",
                       controllable=True, min_p_mw=0.0, max_p_mw=1.5, min_q_mvar=-0.5, max_q_mvar=0.5)


    if len(net.poly_cost) > 0:
        net.poly_cost.drop(net.poly_cost.index, inplace=True)
    
    # 为外部电网设置购电成本函数
    for idx in net.ext_grid.index:
        pp.create_poly_cost(net, element=idx, et="ext_grid", cp1_eur_per_mw=pi_T)
    
    dg_bus_indices = [bus - 1 for bus in dg_buses]  # 转换为索引
    for idx in net.sgen.index:
        if net.sgen.loc[idx, 'bus'] in dg_bus_indices:
            pp.create_poly_cost(net, element=idx, et="sgen", cp1_eur_per_mw=pi_G)

#     #新能源惩罚
#    # 新能源弃风弃光惩罚成本函数
#     curtailment_penalty = 20  # 弃风弃光惩罚系数

#     # 为新能源发电机设置弃风弃光惩罚成本
#     for idx in net.sgen.index:
#         bus_idx = net.sgen.loc[idx, 'bus']
#         if bus_idx not in dg_bus_indices:  # 新能源发电机（风电和太阳能）
#             # 判断是风电还是太阳能
#             if bus_idx in [bus-1 for bus in wind_buses]:
#                 max_available_power = wind_power  # 预测的风电出力
#             elif bus_idx in [bus-1 for bus in solar_buses]:
#                 max_available_power = sunny_power  # 预测的太阳能出力
#             else:
#                 max_available_power = 0
            
#             # 弃风弃光成本函数：curtailment_penalty * (max_available - actual_output)
#             # 转换为最小化问题：-curtailment_penalty * actual_output + curtailment_penalty * max_available
#             pp.create_poly_cost(net, element=idx, et="sgen",
#                             cp1_eur_per_mw=-curtailment_penalty,  # 一次项系数（负号表示弃电惩罚）
#                             cp0_eur=curtailment_penalty * max_available_power)  # 常数
    # 运行最优潮流
    try:
        pp.runopp(net)
        #print("最优潮流求解成功")
    except:
        #print("最优潮流求解失败")
        return None, None, 


    # print(f"总负荷: {net.res_load['p_mw'].sum():.3f} MW")
    # print(f"总发电量: {(net.res_ext_grid['p_mw'].sum() + net.res_sgen['p_mw'].sum()):.3f} MW")
    
    # 计算总成本
    ext_grid_cost = sum(net.res_ext_grid['p_mw'] * pi_T)
    dg_cost = sum([net.res_sgen.loc[idx, 'p_mw'] * pi_G 
               for idx in net.sgen.index 
               if net.sgen.loc[idx, 'bus'] in dg_bus_indices])

    total_cost = net.res_cost

    vm_pu = net.res_bus['vm_pu'].values
    
    # 提取决策变量
    # 外部电网功率
    ext_grid_p = net.res_ext_grid['p_mw'].values
    
    # 可控分布式电源功率
    # 分别提取DG和新能源功率
    dg_p = []
    renewable_p = []

    for idx in net.sgen.index:
        bus_idx = net.sgen.loc[idx, 'bus']
        power = net.res_sgen.loc[idx, 'p_mw']
    
        if bus_idx in dg_bus_indices:  # DG发电机
            dg_p.append(power)
        else:  # 新能源发电机（风电和太阳能）
            renewable_p.append(power)

    dg_p = np.array(dg_p)
    renewable_p = np.array(renewable_p)

# 合成决策变量数组：[外部电网功率, DG功率, 新能源功率]
    decision_vars = np.concatenate([ext_grid_p, dg_p, renewable_p])
    # 合成电压和决策变量
    combined_array = np.concatenate([vm_pu, decision_vars])
    
    return total_cost, decision_vars

def DFL_realtime_ieee33(day_ahead_decision, actual_wind_power, actual_sunny_power):
    """
    实时调度函数：最小化与日前计划的偏差
    
    参数:
    day_ahead_decision: 日前调度的决策变量 [外部电网, DG功率, 新能源功率]
    actual_wind_power: 实际风电出力
    actual_sunny_power: 实际太阳能出力
    """
    
    # 惩罚系数
    pi_G = 10
    pi_T = 20
    penalty_renewable=100 #再调度成本
    curtailment_penalty = 20  # 弃风弃光惩罚系数
    
    net = pn.case33bw()  # IEEE33
    
    # 放大所有负荷（保持与日前相同）
    net.load['p_mw'] *= 1.5
    net.load['q_mvar'] *= 1.5
    
    # 将线路阻抗除以2（保持与日前相同）
    net.line['r_ohm_per_km'] /= 2
    net.line['x_ohm_per_km'] /= 2
    
    # 解析日前决策变量
    day_ahead_ext_grid = day_ahead_decision[0]  # 外部电网
    day_ahead_dg = day_ahead_decision[1:4]      # DG功率
    day_ahead_renewable = day_ahead_decision[4:8]  # 新能源功率
    
    # 风电 - 使用实际出力
    wind_buses = [18, 25]
    for i, bus in enumerate(wind_buses):
        pp.create_sgen(net, bus=bus-1, p_mw=actual_wind_power, q_mvar=0.0,
                      controllable=True, max_p_mw=actual_wind_power, min_p_mw=0.0,
                      name=f"Wind_{bus}")
    
    # 太阳能 - 使用实际出力
    solar_buses = [6, 15]
    for i, bus in enumerate(solar_buses):
        pp.create_sgen(net, bus=bus-1, p_mw=actual_sunny_power, q_mvar=0.0,
                      controllable=True, max_p_mw=actual_sunny_power, min_p_mw=0.0,
                      name=f"Solar_{bus}")

    # 定义 DG 节点索引
    
    # DG 发电机 - 以日前计划为目标值
    dg_buses = [7, 13, 17]
    dg_bus_indices = [bus - 1 for bus in dg_buses]
    for i, bus_idx in enumerate(dg_bus_indices):
        pp.create_sgen(net, bus=bus_idx, p_mw=day_ahead_dg[i], q_mvar=0.0, 
                       name=f"DG at Bus {bus_idx+1}",
                       controllable=True, min_p_mw=0.0, max_p_mw=2.0, 
                       min_q_mvar=-0.5, max_q_mvar=0.5)
    
    # # 删除现有的成本函数
    if len(net.poly_cost) > 0:
        net.poly_cost.drop(net.poly_cost.index, inplace=True)
    
    
   # 为外部电网设置购电成本函数
    for idx in net.ext_grid.index:
        pp.create_poly_cost(net, element=idx, et="ext_grid", cp1_eur_per_mw=pi_T)
    # ...existing code...
    
    # 为DG设置发电成本和再调度成本
    dg_bus_indices = [bus - 1 for bus in dg_buses]  # 转换为索引
    for idx in net.sgen.index:
        bus_idx = net.sgen.loc[idx, 'bus']
        if bus_idx in dg_bus_indices:
            # 找到对应的日前DG计划值
            dg_index = dg_bus_indices.index(bus_idx)
            day_ahead_dg_power = day_ahead_dg[dg_index]
            
            # DG成本函数：发电成本 + 再调度成本
            # 总成本 = pi_G * P + penalty_renewable * |P - day_ahead_power|
            # 为了处理绝对值，这里使用线性化方法或者简化为二次成本
            # 使用二次成本：penalty_renewable * (P - day_ahead_power)^2
            # 展开：penalty_renewable * (P^2 - 2*day_ahead_power*P + day_ahead_power^2)
            
            pp.create_poly_cost(net, element=idx, et="sgen", 
                            cp2_eur_per_mw2=penalty_renewable,  # 二次项系数
                            cp1_eur_per_mw= pi_G- 2*penalty_renewable*day_ahead_dg_power,  # 一次项系数
                            cp0_eur=penalty_renewable*day_ahead_dg_power**2)  # 常数项
            
            # pp.create_poly_cost(net, element=idx, et="sgen", 
            #                 cp2_eur_per_mw2=penalty_renewable,  # 二次项系数
            #                 cp1_eur_per_mw= - 2*penalty_renewable*day_ahead_dg_power,  # 一次项系数
            #                 cp0_eur=penalty_renewable*day_ahead_dg_power**2)  # 常数项
        

    # 合并再调度成本和弃风弃光成本
    # ...existing code...
    for idx in net.sgen.index:
        bus_idx = net.sgen.loc[idx, 'bus']
        if bus_idx not in dg_bus_indices:  # 新能源发电机（风电和太阳能）
            # 判断是风电还是太阳能
            if bus_idx in [bus-1 for bus in wind_buses]:
                actual_power = actual_wind_power
                # 找到对应的日前新能源计划值
                renewable_index = 0  # 风电在renewable数组中的索引
                day_ahead_renewable_power = day_ahead_renewable[renewable_index]
            elif bus_idx in [bus-1 for bus in solar_buses]:
                actual_power = actual_sunny_power
                # 找到对应的日前新能源计划值
                renewable_index = 2  # 太阳能在renewable数组中的索引（假设有2个风电，2个太阳能）
                day_ahead_renewable_power = day_ahead_renewable[renewable_index]
            else:
                actual_power = 0  # 默认值
                day_ahead_renewable_power = 0
            
            # 新能源成本函数：弃风弃光成本 + 再调度成本
            # 弃风弃光成本：curtailment_penalty * (actual_power - P)
            # 再调度成本：penalty_renewable * (P - day_ahead_power)^2
            # 总成本 = -curtailment_penalty * P + curtailment_penalty * actual_power + penalty_renewable * (P - day_ahead_power)^2
            
            pp.create_poly_cost(net, element=idx, et="sgen",
                            cp2_eur_per_mw2=0,  # 二次项系数（再调度）
                            cp1_eur_per_mw=-1*curtailment_penalty,  # 一次项系数
                            cp0_eur=curtailment_penalty*actual_power)  # 常数项.

    # 运行最优潮流
    try:
        pp.runopp(net)
        #print("实时调度求解成功")
    except Exception as e:
        #print(f"实时调度求解失败: {e}")
        return None, None, None
    
    # print(f"总负荷: {net.res_load['p_mw'].sum():.3f} MW")
    # print(f"总发电量: {(net.res_ext_grid['p_mw'].sum() + net.res_sgen['p_mw'].sum()):.3f} MW")
    
    # 计算偏差成本
    deviation_cost = net.res_cost #目标函数
    
    # 提取实时调度结果
    vm_pu = net.res_bus['vm_pu'].values
    
    # 提取决策变量
    ext_grid_p = net.res_ext_grid['p_mw'].values
    
    # 分别提取DG和新能源功率
    dg_p = []
    renewable_p = []
    
    for idx in net.sgen.index:
        bus_idx = net.sgen.loc[idx, 'bus']
        power = net.res_sgen.loc[idx, 'p_mw']
        
        if bus_idx in dg_bus_indices:  # DG发电机
            dg_p.append(power)
        else:  # 新能源发电机（风电和太阳能）
            renewable_p.append(power)
    
    dg_p = np.array(dg_p)
    renewable_p = np.array(renewable_p)
    
    # 合成决策变量数组：[外部电网功率, DG功率, 新能源功率]
    realtime_decision = np.concatenate([ext_grid_p, dg_p, renewable_p])
    
    # 计算各项偏差
    ext_grid_deviation = abs(ext_grid_p[0] - day_ahead_ext_grid)
    dg_deviation = np.abs(dg_p - day_ahead_dg)
    renewable_deviation = np.abs(renewable_p - day_ahead_renewable)


    redispatch_cost = 0
    curtailment_cost = 0
    
    # 分别提取DG和新能源功率
    dg_p = []
    renewable_p = []
    
    for idx in net.sgen.index:
        bus_idx = net.sgen.loc[idx, 'bus']
        power = net.res_sgen.loc[idx, 'p_mw']
        
        if bus_idx in dg_bus_indices:  # DG发电机
            dg_p.append(power)
            # 计算再调度成本
            dg_index = dg_bus_indices.index(bus_idx)
            day_ahead_dg_power = day_ahead_dg[dg_index]
            redispatch_cost += penalty_renewable * (power - day_ahead_dg_power)**2
        else:  # 新能源发电机（风电和太阳能）
            renewable_p.append(power)
            # 计算弃风弃光成本
            if bus_idx in [bus-1 for bus in wind_buses]:
                actual_power = actual_wind_power
                curtailment_amount = actual_power - power
            elif bus_idx in [bus-1 for bus in solar_buses]:
                actual_power = actual_sunny_power
                curtailment_amount = actual_power - power
            else:
                curtailment_amount = 0
            
            if curtailment_amount > 0:
                curtailment_cost += curtailment_penalty * curtailment_amount
    
    # 打印成本详情
    # print(f"\n=== 成本分析 ===")
    # print(f"再调度成本: {redispatch_cost:.2f}")
    # print(f"弃风弃光成本: {curtailment_cost:.2f}")
    # print(f"总成本: {net.res_cost:.2f}")
    # print(f"其中基础运行成本: {net.res_cost - redispatch_cost - curtailment_cost:.2f}")

    
    # print(f"\n=== 偏差分析 ===")
    # print(f"外部电网偏差: {ext_grid_deviation:.3f} MW")
    # print(f"DG偏差: {dg_deviation}")
    # print(f"新能源偏差: {renewable_deviation}")
    # print(f"总偏差成本: {deviation_cost:.2f}")
    
    return deviation_cost, realtime_decision, {
        'ext_grid_deviation': ext_grid_deviation,
        'dg_deviation': dg_deviation,
        'renewable_deviation': renewable_deviation
    }

def calculate_reward(predicted_wind_power, predicted_sunny_power, actual_wind_power, actual_sunny_power):
    """
    基于后悔值的奖励函数
    输入：智能体预测的新能源出力和实际出力
    """
    # 1. 基于预测值执行日前调度
    day_ahead_cost, day_ahead_decision = DFLieee33(predicted_wind_power, predicted_sunny_power)
    
    # 如果日前调度失败，返回大负奖励
    if day_ahead_cost is None:
        return -1000
    
    # 2. 基于实际值和日前决策执行实时调度
    deviation_cost, realtime_decision, deviations = DFL_realtime_ieee33(
        day_ahead_decision, actual_wind_power, actual_sunny_power)
    
    # 如果实时调度失败，返回大负奖励
    if deviation_cost is None:
        return -1000
    
    # 3. 计算完美信息调度（基于实际值的最优调度）

    perfect_info_cost, perfect_info_decision = DFLieee33(actual_wind_power, actual_sunny_power)
    perfect_cost, _,_ = DFL_realtime_ieee33(
        perfect_info_decision, actual_wind_power, actual_sunny_power)
    
    # 如果完美信息调度失败，使用实际总成本作为基准
    # if perfect_info_cost is None:
    #       perfect_info_cost = day_ahead_cost + deviation_cost

    # 4. 计算总后悔值
    total_actual_cost = day_ahead_cost + deviation_cost
    total_regret = total_actual_cost - perfect_cost - perfect_info_cost 

    # 5. 奖励 = -后悔值（后悔值越小，奖励越大）
   
    return deviation_cost-perfect_cost,deviation_cost,perfect_cost

def optimization_ieee33(predicted_wind_power, predicted_sunny_power, actual_wind_power, actual_sunny_power):
    # 1. 基于预测值执行日前调度
    day_ahead_cost, day_ahead_decision = DFLieee33(predicted_wind_power, predicted_sunny_power)
    intra_day_cost, realtime_decision, deviations = DFL_realtime_ieee33(day_ahead_decision, actual_wind_power, actual_sunny_power)

    return intra_day_cost
    
if __name__ == "__main__":
    # 使用示例
    predicted_wind = 1.1    # 智能体预测的风电出力
    predicted_solar = 1.1  # 智能体预测的太阳能出力
    actual_wind = 1.2       # 实际风电出力
    actual_solar = 1.1      # 实际太阳能出力

    reward = calculate_reward(predicted_wind, predicted_solar, actual_wind, actual_solar)
    print(f"奖励值: {reward:.2f}")