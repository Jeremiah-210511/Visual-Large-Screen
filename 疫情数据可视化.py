import streamlit as st
import plotly.express as px
import json
import pandas as pd
import numpy as np


@st.cache
def get_data(url):
    return pd.read_excel(url)


@st.cache
def get_china_data():
    url = '国内疫情.xlsx'
    return get_data(url)


@st.cache
def get_international_data():
    url = '全球疫情.xlsx'
    return get_data(url)


@st.cache
def get_country_code():
    url = 'owid-co2-data.csv'
    return pd.read_csv(url)

st.set_page_config(layout="wide")

df_china = get_china_data()
df_international = get_international_data()
df_country_code = get_country_code()

# 匹配国家编码
df_country_code['year'] = df_country_code['year'].astype(int)
df_country_code = df_country_code[df_country_code['year'] == 2020]
df = pd.merge(df_international, df_country_code, left_on="英文", right_on="country", how="inner")
df = df[['中文', '英文', 'iso_code', 'nowConfirm', 'dead', 'heal', 'confirm']]


st.markdown("""# 全球疫情速览
__“现有确诊数”口径取自国家卫健委每日公布的“现有确诊病例数”，该数值反应了当前正在治疗中的确诊人数（含港澳台）。
海外疫情数据来源于Worldometer Coronavirus、霍普金斯大学网站等渠道。__
__将鼠标悬停在任何图表上可查看更多详细信息__
---
""")

col2, space2, col3 = st.columns((10, 1, 10))

with open("china_province.geojson", encoding='utf-8') as f:
    provinces_map = json.load(f)

with col2:
    st.subheader("""COVID-19国内地区现有确诊人数地图""")
    fig = px.choropleth_mapbox(
        df_china,
        geojson=provinces_map,
        color='nowConfirm',
        locations="province",
        featureidkey="properties.NL_NAME_1",
        hover_name="province",
        mapbox_style="carto-darkmatter",
        color_continuous_scale=[[0, 'white'],
                                [.004, 'lightcoral'],
                                [.04, 'brown'],
                                [.4, 'firebrick'],
                                [.8, 'darkred'],
                                [1., 'maroon']],
        center={"lat": 37.110573, "lon": 106.493924},
        zoom=2,
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.subheader("""COVID-19世界各国及各地区现有确诊人数地图""")
    fig = px.choropleth(df,
                        locations="iso_code",
                        hover_name="中文",
                        color="nowConfirm",
                        color_continuous_scale=[[0, 'white'],
                                                [.002, 'lightcoral'],
                                                [.02, 'brown'],
                                                [.2, 'firebrick'],
                                                [.6, 'darkred'],
                                                [1., 'maroon']],
                        )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('___数据来源:___ _腾讯新闻官方_')



