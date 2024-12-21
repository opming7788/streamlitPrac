from tools import fetch_youbike_data
import streamlit as st

import pandas as pd
import pydeck as pdk

youbike_data:list[dict] = fetch_youbike_data()
# print(youbike_data)

# 使用streamlit分2個欄位
# 使用you_bike_data:list的資料, 取出所有的行政區域(sarea), 不可以重複
# 左邊是選擇行政區域(sarea), 使用下拉式表單
# 右邊是顯示該行政區域的YouBike站點資訊的表格資料
# 最下方是顯示該行政區域的YouBike站點資訊的地圖
sarea_list = sorted(set(map(lambda item:item['sarea'],youbike_data)))
col1,col2 = st.columns([1,5])
with col1:
    selected_sarea = st.selectbox("行政區域",sarea_list)

with col2:
    filter_data = filter(lambda item:item['sarea'] == selected_sarea,youbike_data)
    filter_list:list[dict] = list(filter_data)
    show_data :list[dict] = list({
                            '站點':item['sna'],
                            '總車輛數':item['tot'],
                            '可借車輛數':item['sbi'],
                            '可還空位數':item['bemp'],
                            '營業中':item['act'],
                            'latitude':float(item['lat']),
                            'longitude':float(item['lng'])
                             } for item in filter_list)
    st.dataframe(show_data)

#顯示地圖
# filter_data = list(filter(lambda item:item['sarea'] == selected_sarea,youbike_data))
# locations = [{'lat': float(item['latitude']), 'lon': float(item['longitude'])} for item in show_data]
# st.map(locations)

# st.map(show_data,latitude='latitude',longitude='longitude')

# 轉換資料為DataFrame，方便傳遞給pydeck
map_data = pd.DataFrame(show_data)

# 創建pydeck地圖
deck = pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=map_data['latitude'].mean(),
        longitude=map_data['longitude'].mean(),
        zoom=12
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=map_data,
            get_position='[longitude, latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=100,
            pickable=True,
            auto_highlight=True
        )
    ]
)

# 顯示地圖
st.pydeck_chart(deck)

# 顯示點擊後的站點資訊
if st.session_state.get("clicked_point"):
    point = st.session_state.clicked_point
    st.write(f"選中的站點: {point['站點']}")
    st.write(f"總車輛數: {point['總車輛數']}")
    st.write(f"可借車輛數: {point['可借車輛數']}")
    st.write(f"可還空位數: {point['可還空位數']}")
    st.write(f"營業中: {point['營業中']}")