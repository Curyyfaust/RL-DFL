import pandapower as pp
import numpy as np
from ieee141 import ieee141  # 导入141节点网络函数

# def create_ieee6bus_trunk():
#     """创建6节点输电主干网"""
#     net = pp.create_empty_network()
#     buses = [pp.create_bus(net, vn_kv=110, name=f"Trunk_{i+1}") for i in range(6)]
    
#     # 创建6-bus输电网络拓扑（环形结构）
#     pp.create_line_from_parameters(net, buses[0], buses[1], length_km=10, r_ohm_per_km=0.1, x_ohm_per_km=0.2, c_nf_per_km=10, max_i_ka=1)
#     pp.create_line_from_parameters(net, buses[1], buses[2], length_km=15, r_ohm_per_km=0.1, x_ohm_per_km=0.2, c_nf_per_km=10, max_i_ka=1)
#     pp.create_line_from_parameters(net, buses[2], buses[3], length_km=12, r_ohm_per_km=0.1, x_ohm_per_km=0.2, c_nf_per_km=10, max_i_ka=1)
#     pp.create_line_from_parameters(net, buses[3], buses[4], length_km=8, r_ohm_per_km=0.1, x_ohm_per_km=0.2, c_nf_per_km=10, max_i_ka=1)
#     pp.create_line_from_parameters(net, buses[4], buses[5], length_km=20, r_ohm_per_km=0.1, x_ohm_per_km=0.2, c_nf_per_km=10, max_i_ka=1)
#     pp.create_line_from_parameters(net, buses[5], buses[0], length_km=18, r_ohm_per_km=0.1, x_ohm_per_km=0.2, c_nf_per_km=10, max_i_ka=1)
    
#     # 添加输电网负荷
#     for i in range(1, 6):
#         pp.create_load(net, bus=buses[i], p_mw=50, q_mvar=30, name=f"Trunk_Load_{i+1}")
    
#     # 设置slack节点
#     pp.create_ext_grid(net, bus=buses[0], vm_pu=1.0, name="Slack")
#     return net, buses

def create_ieee6bus_trunk():
    """创建标准IEEE 6-bus输电系统"""
    net = pp.create_empty_network()
    
    # 创建6个节点，按照IEEE 6-bus标准
    buses = []
    buses.append(pp.create_bus(net, vn_kv=230, name="Bus_1"))  # 发电节点
    buses.append(pp.create_bus(net, vn_kv=230, name="Bus_2"))  # 发电节点
    buses.append(pp.create_bus(net, vn_kv=230, name="Bus_3"))  # 发电节点
    buses.append(pp.create_bus(net, vn_kv=230, name="Bus_4"))  # 负荷节点
    buses.append(pp.create_bus(net, vn_kv=230, name="Bus_5"))  # 负荷节点
    buses.append(pp.create_bus(net, vn_kv=230, name="Bus_6"))  # 负荷节点
    
    # 创建标准IEEE 6-bus线路连接 (基于标准参数)
    # Line 1-2
    pp.create_line_from_parameters(net, buses[0], buses[1], length_km=50,
                                   r_ohm_per_km=0.1, x_ohm_per_km=0.2, 
                                   c_nf_per_km=0, max_i_ka=4.0, name="Line_1_2")
    
    # Line 1-4  
    pp.create_line_from_parameters(net, buses[0], buses[3], length_km=60,
                                   r_ohm_per_km=0.05, x_ohm_per_km=0.25,
                                   c_nf_per_km=0, max_i_ka=6.0, name="Line_1_4")
    
    # Line 1-5
    pp.create_line_from_parameters(net, buses[0], buses[4], length_km=80,
                                   r_ohm_per_km=0.08, x_ohm_per_km=0.3,
                                   c_nf_per_km=0, max_i_ka=4.0, name="Line_1_5")
    
    # Line 2-3
    pp.create_line_from_parameters(net, buses[1], buses[2], length_km=70,
                                   r_ohm_per_km=0.05, x_ohm_per_km=0.25,
                                   c_nf_per_km=0, max_i_ka=6.0, name="Line_2_3")
    
    # Line 2-4
    pp.create_line_from_parameters(net, buses[1], buses[3], length_km=90,
                                   r_ohm_per_km=0.06, x_ohm_per_km=0.25,
                                   c_nf_per_km=0, max_i_ka=4.0, name="Line_2_4")
    
    # Line 2-5
    pp.create_line_from_parameters(net, buses[1], buses[4], length_km=100,
                                   r_ohm_per_km=0.06, x_ohm_per_km=0.25,
                                   c_nf_per_km=0, max_i_ka=2.0, name="Line_2_5")
    
    # Line 2-6
    pp.create_line_from_parameters(net, buses[1], buses[5], length_km=110,
                                   r_ohm_per_km=0.06, x_ohm_per_km=0.25,
                                   c_nf_per_km=0, max_i_ka=2.0, name="Line_2_6")
    
    # Line 3-5
    pp.create_line_from_parameters(net, buses[2], buses[4], length_km=120,
                                   r_ohm_per_km=0.04, x_ohm_per_km=0.2,
                                   c_nf_per_km=0, max_i_ka=2.0, name="Line_3_5")
    
    # Line 3-6
    pp.create_line_from_parameters(net, buses[2], buses[5], length_km=130,
                                   r_ohm_per_km=0.02, x_ohm_per_km=0.1,
                                   c_nf_per_km=0, max_i_ka=3.2, name="Line_3_6")
    
    # Line 4-5
    pp.create_line_from_parameters(net, buses[3], buses[4], length_km=140,
                                   r_ohm_per_km=0.08, x_ohm_per_km=0.3,
                                   c_nf_per_km=0, max_i_ka=1.6, name="Line_4_5")
    
    # Line 5-6
    pp.create_line_from_parameters(net, buses[4], buses[5], length_km=150,
                                   r_ohm_per_km=0.1, x_ohm_per_km=0.4,
                                   c_nf_per_km=0, max_i_ka=1.6, name="Line_5_6")
    
    # 添加发电机 (Bus 1, 2, 3为发电节点)
    # pp.create_gen(net, bus=buses[1], p_mw=50, vm_pu=1.05, 
    #               min_p_mw=0, max_p_mw=200, name="Gen_2")
    # pp.create_gen(net, bus=buses[2], p_mw=60, vm_pu=1.04, 
    #               min_p_mw=0, max_p_mw=150, name="Gen_3")
    
    # 添加负荷 (Bus 4, 5, 6为负荷节点)
    pp.create_load(net, bus=buses[3], p_mw=70, q_mvar=35, name="Load_4")
    pp.create_load(net, bus=buses[4], p_mw=70, q_mvar=35, name="Load_5")
    pp.create_load(net, bus=buses[5], p_mw=70, q_mvar=35, name="Load_6")
    
    # 设置Bus 1为slack节点
    pp.create_ext_grid(net, bus=buses[0], vm_pu=1.06, name="Slack")
    
    return net, buses

def create_ieee141_net_modified():
    """创建修改后的141节点配电网（移除slack节点）"""
    net = ieee141()  # 调用原始ieee141函数
    
    # 移除原来的slack节点，因为要接入输电网
    net.ext_grid.drop(net.ext_grid.index, inplace=True)
    
    # 返回网络和第一个节点索引（用于连接）
    first_bus = net.bus.index[0]  # 获取第一个bus的实际索引
    return net, first_bus

def merge_nets_advanced(big_net, sub_net):
    """高级网络合并函数"""
    bus_mapping = {}
    for idx, row in sub_net.bus.iterrows():
        new_bus_idx = pp.create_bus(big_net, vn_kv=row.vn_kv, name=row.name)
        bus_mapping[idx] = new_bus_idx
    
    # 合并线路
    for _, row in sub_net.line.iterrows():
        pp.create_line_from_parameters(
            big_net,
            from_bus=bus_mapping[row.from_bus],
            to_bus=bus_mapping[row.to_bus],
            length_km=row.length_km if 'length_km' in row else 1.0,
            r_ohm_per_km=row.r_ohm_per_km if 'r_ohm_per_km' in row else row.r_pu * 100,
            x_ohm_per_km=row.x_ohm_per_km if 'x_ohm_per_km' in row else row.x_pu * 100,
            c_nf_per_km=row.c_nf_per_km if 'c_nf_per_km' in row else 0,
            max_i_ka=row.max_i_ka if 'max_i_ka' in row else 1,
            name=getattr(row, 'name', f"Line_{row.from_bus}_{row.to_bus}")
        )
    
    # 合并负荷
    for _, row in sub_net.load.iterrows():
        pp.create_load(
            big_net, 
            bus=bus_mapping[row.bus], 
            p_mw=row.p_mw * 15,  # 放大负荷
            q_mvar=row.q_mvar * 15, 
            name=getattr(row, 'name', f"Load_{row.bus}")
        )
    
    # 合并静态发电机（如果有）
    if not sub_net.sgen.empty:
        for _, row in sub_net.sgen.iterrows():
            pp.create_sgen(
                big_net,
                bus=bus_mapping[row.bus],
                p_mw=row.p_mw,
                q_mvar=row.q_mvar,
                name=getattr(row, 'name', f"Sgen_{row.bus}")
            )
    
    return bus_mapping

def add_generators_to_141net(big_net, bus_mapping, network_id):
    """为141配电网添加各种发电机"""
    # 原141网络中的节点映射（1-based转换为实际bus索引）
    dg_buses = [8, 15, 23, 34, 47, 56, 62, 71]
    wind_buses = [8, 28, 68]  
    solar_buses = [12, 36, 62]
    # storage_buses = [10, 25, 40, 58]  # 移除储能
    
    generators_info = {
        'dg_indices': [],
        'wind_indices': [],
        'solar_indices': [],
        # 'storage_indices': []  # 移除储能
    }
    
    # 添加DG发电机
    for bus in dg_buses:
        mapped_bus = bus_mapping[bus - 1]  # bus-1因为ieee141中bus索引是0-based
        idx = pp.create_sgen(big_net, bus=mapped_bus, p_mw=1.0, q_mvar=0.0, 
                             name=f"DG_Net{network_id}_Bus{bus}",
                             controllable=True, min_p_mw=0.0, max_p_mw=2, 
                             min_q_mvar=-0.5, max_q_mvar=0.5)
        generators_info['dg_indices'].append(idx)
    
    # 添加风电
    for bus in wind_buses:
        mapped_bus = bus_mapping[bus - 1]
        idx = pp.create_sgen(big_net, bus=mapped_bus, p_mw=0.5, q_mvar=0.0,
                             controllable=True, max_p_mw=2.0, min_p_mw=0.0,
                             name=f"Wind_Net{network_id}_Bus{bus}")
        generators_info['wind_indices'].append(idx)
    
    # 添加太阳能
    for bus in solar_buses:
        mapped_bus = bus_mapping[bus - 1]
        idx = pp.create_sgen(big_net, bus=mapped_bus, p_mw=0.3, q_mvar=0.0,
                             controllable=True, max_p_mw=1.5, min_p_mw=0.0,
                             name=f"Solar_Net{network_id}_Bus{bus}")
        generators_info['solar_indices'].append(idx)
    
    # # 添加储能 - 移除这部分代码
    # for bus in storage_buses:
    #     mapped_bus = bus_mapping[bus - 1]
    #     idx = pp.create_storage(big_net, bus=mapped_bus, p_mw=0.0, max_e_mwh=1.0, 
    #                            soc_percent=50, q_mvar=0.0, min_e_mwh=0.0,
    #                            name=f"Storage_Net{network_id}_Bus{bus}")
    #     generators_info['storage_indices'].append(idx)
    
    return generators_info

# def create_transformer_connection(net, hv_bus, lv_bus, s_mva=50, vn_hv_kv=110, vn_lv_kv=12.66):
#     """创建变压器连接输电网和配电网"""
#     trafo_idx=pp.create_transformer_from_parameters(
#         net,
#         hv_bus=hv_bus,
#         lv_bus=lv_bus,
#         sn_mva=s_mva,
#         vn_hv_kv=vn_hv_kv,
#         vn_lv_kv=vn_lv_kv,
#         vkr_percent=1.0,
#         vk_percent=10.0,
#         pfe_kw=10,
#         i0_percent=0.1
#     )
#     net.trafo.at[trafo_idx, 'name'] = f"Trafo_{hv_bus}_{lv_bus}"
#     return trafo_idx

# def build_large_grid_with_generators():
#     """构建带发电机的大型电网"""
#     print("正在构建大型电网...")
    
#     # 1. 创建输电主干网
#     print("创建6节点输电主干网...")
#     trunk_net, trunk_buses = create_ieee6bus_trunk()
#     big_net = trunk_net
    
#     # 2. 创建并接入4个141节点配电网
#     all_generators_info = []
#     connection_points = [1, 2, 3, 4]
    
#     for i in range(4):
#         print(f"接入第{i+1}个141节点配电网...")
        
#         # 创建141节点网络
#         ieee141_net, first_bus_orig = create_ieee141_net_modified()
        
#         # 合并到大网络
#         bus_mapping = merge_nets_advanced(big_net, ieee141_net)
        
#         # 添加发电机到该配电网
#         generators_info = add_generators_to_141net(big_net, bus_mapping, i+1)
#         all_generators_info.append(generators_info)
        
#         # 获取配电网第一个节点的新索引
#         first_bus_new = bus_mapping[first_bus_orig]
        
#         # 用变压器连接输电网和配电网（移除name参数）
#         create_transformer_connection(
#             big_net,
#             hv_bus=trunk_buses[connection_points[i]],
#             lv_bus=first_bus_new,
#             s_mva=50
#         )
        
#         print(f"  第{i+1}个配电网已连接，包含：")
#         print(f"    DG: {len(generators_info['dg_indices'])}台")
#         print(f"    风电: {len(generators_info['wind_indices'])}台")
#         print(f"    太阳能: {len(generators_info['solar_indices'])}台")
#         #print(f"    储能: {len(generators_info['storage_indices'])}台")
    
#     print(f"\n大型电网构建完成！")
#     print(f"总节点数: {len(big_net.bus)}")
#     print(f"总线路数: {len(big_net.line)}")
#     print(f"变压器数: {len(big_net.trafo)}")
#     print(f"总负荷数: {len(big_net.load)}")
#     print(f"总发电机数: {len(big_net.sgen)}")
#     #print(f"总储能数: {len(big_net.storage)}")
    
#     return big_net, trunk_buses, all_generators_info

# 同时需要修改变压器连接函数的默认参数
def create_transformer_connection(net, hv_bus, lv_bus, s_mva=100, vn_hv_kv=230, vn_lv_kv=12.66):
    """创建变压器连接输电网和配电网"""
    trafo_idx = pp.create_transformer_from_parameters(
        net,
        hv_bus=hv_bus,
        lv_bus=lv_bus,
        sn_mva=s_mva,
        vn_hv_kv=vn_hv_kv,  # 改为230kV匹配IEEE 6-bus
        vn_lv_kv=vn_lv_kv,
        vkr_percent=1.0,
        vk_percent=10.0,
        pfe_kw=10,
        i0_percent=0.1
    )
    net.trafo.at[trafo_idx, 'name'] = f"Trafo_{hv_bus}_{lv_bus}"
    return trafo_idx

# 修改构建函数中的连接点说明
def build_large_grid_with_generators():
    """构建带发电机的大型电网"""
    print("正在构建大型电网...")
    
    # 1. 创建标准IEEE 6-bus输电主干网
    print("创建标准IEEE 6-bus输电主干网...")
    trunk_net, trunk_buses = create_ieee6bus_trunk()
    big_net = trunk_net
    
    # 2. 创建并接入4个141节点配电网
    all_generators_info = []
    # 连接到Bus 4, 5, 6 (负荷节点) 和 Bus 2 (发电节点)
    connection_points = [3, 4, 5, 1]  # 对应Bus 4, 5, 6, 2 (索引从0开始)
    
    for i in range(4):
        print(f"接入第{i+1}个141节点配电网...")
        
        # 创建141节点网络
        ieee141_net, first_bus_orig = create_ieee141_net_modified()
        
        # 合并到大网络
        bus_mapping = merge_nets_advanced(big_net, ieee141_net)
        
        # 添加发电机到该配电网
        generators_info = add_generators_to_141net(big_net, bus_mapping, i+1)
        all_generators_info.append(generators_info)
        
        # 获取配电网第一个节点的新索引
        first_bus_new = bus_mapping[first_bus_orig]
        
        # 用变压器连接输电网和配电网
        create_transformer_connection(
            big_net,
            hv_bus=trunk_buses[connection_points[i]],
            lv_bus=first_bus_new,
            s_mva=100,  # 增大变压器容量
            vn_hv_kv=230  # 匹配IEEE 6-bus的230kV
        )
        
        print(f"  第{i+1}个配电网已连接到Bus_{connection_points[i]+1}，包含：")
        print(f"    DG: {len(generators_info['dg_indices'])}台")
        print(f"    风电: {len(generators_info['wind_indices'])}台")
        print(f"    太阳能: {len(generators_info['solar_indices'])}台")
    
    print(f"\n基于IEEE 6-bus的大型电网构建完成！")
    print(f"总节点数: {len(big_net.bus)}")
    print(f"总线路数: {len(big_net.line)}")
    print(f"变压器数: {len(big_net.trafo)}")
    print(f"总负荷数: {len(big_net.load)}")
    print(f"总发电机数: {len(big_net.sgen)} (静态) + {len(big_net.gen)} (常规)")
    
    return big_net, trunk_buses, all_generators_info


def day_ahead_dispatch(net, wind_forecast, solar_forecast, all_generators_info):
    """日前调度"""
    # 价格参数
    pi_G = 10      # DG成本
    pi_T = 20      # 外部电网成本  
    pi_S = 5       # 储能成本
    
    # 设置预测新能源出力
    for i, gen_info in enumerate(all_generators_info):
        # 设置风电预测出力
        for wind_idx in gen_info['wind_indices']:
            net.sgen.at[wind_idx, 'p_mw'] = wind_forecast[i] if isinstance(wind_forecast, list) else wind_forecast
            net.sgen.at[wind_idx, 'max_p_mw'] = wind_forecast[i] if isinstance(wind_forecast, list) else wind_forecast
        
        # 设置太阳能预测出力
        for solar_idx in gen_info['solar_indices']:
            net.sgen.at[solar_idx, 'p_mw'] = solar_forecast[i] if isinstance(solar_forecast, list) else solar_forecast
            net.sgen.at[solar_idx, 'max_p_mw'] = solar_forecast[i] if isinstance(solar_forecast, list) else solar_forecast
    
    # 清除现有成本函数
    if len(net.poly_cost) > 0:
        net.poly_cost.drop(net.poly_cost.index, inplace=True)
    
    # 外部电网成本
    for idx in net.ext_grid.index:
        pp.create_poly_cost(net, element=idx, et="ext_grid", cp1_eur_per_mw=pi_T)
    
    # DG成本
    for gen_info in all_generators_info:
        for idx in gen_info['dg_indices']:
            pp.create_poly_cost(net, element=idx, et="sgen", cp1_eur_per_mw=pi_G)
    
    # # 储能成本
    # for idx in net.storage.index:
    #     pp.create_poly_cost(net, element=idx, et="storage", cp1_eur_per_mw=pi_S)
    
    # 设置电压约束
    net.bus["min_vm_pu"] = 0.9
    net.bus["max_vm_pu"] = 1.1
    
    try:
        pp.runopp(net)
        day_ahead_cost = net.res_cost
        
        # 提取日前调度决策
        day_ahead_decision = {
            'ext_grid': net.res_ext_grid['p_mw'].values,
            'dg': {},
            'wind': {},
            'solar': {},
            'storage': net.res_storage['p_mw'].values if len(net.res_storage) > 0 else np.array([])
        }
        
        # 按配电网提取DG、风电、太阳能决策
        for i, gen_info in enumerate(all_generators_info):
            day_ahead_decision['dg'][i] = net.res_sgen.loc[gen_info['dg_indices'], 'p_mw'].values
            day_ahead_decision['wind'][i] = net.res_sgen.loc[gen_info['wind_indices'], 'p_mw'].values
            day_ahead_decision['solar'][i] = net.res_sgen.loc[gen_info['solar_indices'], 'p_mw'].values
        
        return day_ahead_cost, day_ahead_decision, True
        
    except Exception as e:
        print(f"日前调度失败: {e}")
        return None, None, False

def real_time_dispatch(net, day_ahead_decision, actual_wind, actual_solar, all_generators_info):
    """实时调度"""
    # 价格参数
    pi_G = 10
    pi_T = 20
    penalty_renewable = 100  # 再调度惩罚
    curtailment_penalty = 20  # 弃风弃光惩罚
    
    # 更新实际新能源出力
    for i, gen_info in enumerate(all_generators_info):
        # 更新风电实际出力
        actual_wind_power = actual_wind[i] if isinstance(actual_wind, list) else actual_wind
        for wind_idx in gen_info['wind_indices']:
            net.sgen.at[wind_idx, 'max_p_mw'] = actual_wind_power
        
        # 更新太阳能实际出力
        actual_solar_power = actual_solar[i] if isinstance(actual_solar, list) else actual_solar
        for solar_idx in gen_info['solar_indices']:
            net.sgen.at[solar_idx, 'max_p_mw'] = actual_solar_power
    
    # 清除现有成本函数
    if len(net.poly_cost) > 0:
        net.poly_cost.drop(net.poly_cost.index, inplace=True)
    
    # 外部电网成本
    for idx in net.ext_grid.index:
        pp.create_poly_cost(net, element=idx, et="ext_grid", cp1_eur_per_mw=pi_T)
    
    # DG再调度成本（二次惩罚）
    for i, gen_info in enumerate(all_generators_info):
        day_ahead_dg = day_ahead_decision['dg'][i]
        for j, idx in enumerate(gen_info['dg_indices']):
            day_ahead_power = day_ahead_dg[j]
            pp.create_poly_cost(net, element=idx, et="sgen",
                                cp2_eur_per_mw2=penalty_renewable,
                                cp1_eur_per_mw=pi_G - 2*penalty_renewable*day_ahead_power,
                                cp0_eur=penalty_renewable*day_ahead_power**2)
    
    # 新能源弃电成本
    for i, gen_info in enumerate(all_generators_info):
        actual_wind_power = actual_wind[i] if isinstance(actual_wind, list) else actual_wind
        actual_solar_power = actual_solar[i] if isinstance(actual_solar, list) else actual_solar
        
        # 风电弃电成本
        for wind_idx in gen_info['wind_indices']:
            pp.create_poly_cost(net, element=wind_idx, et="sgen",
                                cp1_eur_per_mw=-curtailment_penalty,
                                cp0_eur=curtailment_penalty*actual_wind_power)
        
        # 太阳能弃电成本
        for solar_idx in gen_info['solar_indices']:
            pp.create_poly_cost(net, element=solar_idx, et="sgen",
                                cp1_eur_per_mw=-curtailment_penalty,
                                cp0_eur=curtailment_penalty*actual_solar_power)
    
    # 储能成本
    # for idx in net.storage.index:
    #     pp.create_poly_cost(net, element=idx, et="storage", cp1_eur_per_mw=pi_S)
    
    try:
        pp.runopp(net)
        real_time_cost = net.res_cost
        
        # 提取实时调度决策
        real_time_decision = {
            'ext_grid': net.res_ext_grid['p_mw'].values,
            'dg': {},
            'wind': {},
            'solar': {},
            'storage': net.res_storage['p_mw'].values if len(net.res_storage) > 0 else np.array([])
        }
        
        for i, gen_info in enumerate(all_generators_info):
            real_time_decision['dg'][i] = net.res_sgen.loc[gen_info['dg_indices'], 'p_mw'].values
            real_time_decision['wind'][i] = net.res_sgen.loc[gen_info['wind_indices'], 'p_mw'].values
            real_time_decision['solar'][i] = net.res_sgen.loc[gen_info['solar_indices'], 'p_mw'].values
        
        return real_time_cost, real_time_decision, True
        
    except Exception as e:
        print(f"实时调度失败: {e}")
        return None, None, False

def two_stage_dispatch(wind_forecast, solar_forecast, actual_wind, actual_solar):
    """完整的两阶段调度"""
    print("\n=== 开始两阶段调度 ===")
    
    # 1. 构建电网
    net, trunk_buses, all_generators_info = build_large_grid_with_generators()
    
    # 2. 日前调度
    print("\n执行日前调度...")
    day_ahead_cost, day_ahead_decision, success1 = day_ahead_dispatch(
        net, wind_forecast, solar_forecast, all_generators_info)
    
    if not success1:
        return None, None, None
    
    print(f"日前调度成功，总成本: {day_ahead_cost:.2f}")
    
    # 3. 实时调度
    print("执行实时调度...")
    real_time_cost, real_time_decision, success2 = real_time_dispatch(
        net, day_ahead_decision, actual_wind, actual_solar, all_generators_info)
    
    if not success2:
        return None, None, None
    
    print(f"实时调度成功，总成本: {real_time_cost:.2f}")
    
    # 4. 计算总成本和偏差
    total_cost = day_ahead_cost + real_time_cost
    
    # 计算各配电网的偏差
    deviations = {}
    for i in range(4):
        deviations[f'net_{i+1}'] = {
            'dg_deviation': np.abs(real_time_decision['dg'][i] - day_ahead_decision['dg'][i]).sum(),
            'wind_deviation': np.abs(real_time_decision['wind'][i] - day_ahead_decision['wind'][i]).sum(),
            'solar_deviation': np.abs(real_time_decision['solar'][i] - day_ahead_decision['solar'][i]).sum()
        }
    
    print(f"总调度成本: {total_cost:.2f}")
    print("\n各配电网偏差情况:")
    for net_name, dev in deviations.items():
        print(f"{net_name}: DG偏差={dev['dg_deviation']:.3f}, 风电偏差={dev['wind_deviation']:.3f}, 太阳能偏差={dev['solar_deviation']:.3f}")
    
    return total_cost, day_ahead_decision, real_time_decision

# 主程序示例
if __name__ == "__main__":
    # 示例预测和实际值
    wind_forecast = [1.2, 1.5, 1.0, 1.3]  # 4个配电网的风电预测
    solar_forecast = [0.8, 1.0, 0.9, 1.1]  # 4个配电网的太阳能预测
    actual_wind = [1.0, 1.2, 1.1, 1.4]     # 实际风电
    actual_solar = [0.9, 0.8, 1.0, 1.2]    # 实际太阳能
    
    # 执行两阶段调度
    total_cost, day_ahead, real_time = two_stage_dispatch(
        wind_forecast, solar_forecast, actual_wind, actual_solar)
    
    if total_cost is not None:
        print(f"\n=== 调度完成 ===")
        print(f"总成本: {total_cost:.2f}")
    else:
        print("调度失败")