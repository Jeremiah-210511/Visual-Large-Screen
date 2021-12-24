import json
import requests
import pandas as pd


def Domestic():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    reponse = requests.get(url=url).json()
    data = json.loads(reponse['data'])
    return data

def Oversea():
    url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoCountryConfirmAdd,WomWorld,WomAboard'
    reponse = requests.post(url=url).json()
    data = reponse['data']
    return data

domestic = Domestic()
oversea = Oversea()

# 提取国内各地区数据明细
areaTree = domestic['areaTree']
# 提取国外地区数据明细
foreignList = oversea['WomAboard']

china_data = areaTree[0]['children']
china_list = []
for a in range(len(china_data)):
    province = china_data[a]['name']
    confirm = china_data[a]['total']['confirm']
    heal = china_data[a]['total']['heal']
    dead = china_data[a]['total']['dead']
    nowConfirm = confirm - heal - dead
    china_dict = {}
    china_dict['province'] = province
    china_dict['nowConfirm'] = nowConfirm
    china_list.append(china_dict)

china_data = pd.DataFrame(china_list)
china_data.to_excel("国内疫情.xlsx", index=False)

world_data = foreignList
world_list = []

for a in range(len(world_data)):
    # 提取数据
    country = world_data[a]['name']
    nowConfirm = world_data[a]['nowConfirm']
    confirm = world_data[a]['confirm']
    dead = world_data[a]['dead']
    heal = world_data[a]['heal']
    # 存放数据
    world_dict = {}
    world_dict['country'] = country
    world_dict['nowConfirm'] = nowConfirm
    world_dict['confirm'] = confirm
    world_dict['dead'] = dead
    world_dict['heal'] = heal
    world_list.append(world_dict)

world_data = pd.DataFrame(world_list)

confirm = areaTree[0]['total']['confirm']  # 提取中国累计确诊数据
heal = areaTree[0]['total']['heal']  # 提取中国累计治愈数据
dead = areaTree[0]['total']['dead']  # 提取中国累计死亡数据
nowConfirm = confirm - heal - dead  # 计算中国现有确诊数量

# 将中国疫情数据加入到国际疫情数据中
world_data = world_data.append({'country': "中国", 'nowConfirm': nowConfirm,
                                'confirm': confirm, 'heal': heal, 'dead': dead}, ignore_index=True)

# 匹配国家英文名称
world_name = pd.read_excel("国家中英文对照表.xlsx")
world_data_t = pd.merge(world_data, world_name, left_on="country", right_on="中文", how="inner")
world_data_t.to_excel('./全球疫情.xlsx')