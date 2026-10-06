import requests
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# 10분간 결과 캐싱
@st.cache_data(ttl=600)
def get_hourly_temperature(lat, lon):
    resp = requests.get(
        FORECAST_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m",
            "forecast_days": 2,
            "timezone": "auto",
        },
        timeout=10,
    )
    resp.raise_for_status()
    hourly = resp.json()["hourly"]
    df = pd.DataFrame({
        "time": pd.to_datetime(hourly["time"]),
        "Temperature (°C)": hourly["temperature_2m"],
    })
    return df.set_index("time")

st.set_page_config(page_title="Interactive Weather Map", layout="centered")
st.title("Interactive Weather Dashboard")
st.caption("Arts and Advanced Big Data | Open API, Service 2")

# 1. 지도에서 위치 선택
st.subheader("1. Pick a place (click the map)")
fmap = folium.Map(location=[36.5, 127.5], zoom_start=6)
result = st_folium(fmap, height=380, width=700)

clicked = (result or {}).get("last_clicked")
if not clicked:
    st.info("Click anywhere on the map to load the hourly temperature for that place.")
    st.stop()

# 2. 선택한 위치의 날씨 정보 가져오기
lat, lon = round(clicked["lat"], 3), round(clicked["lng"], 3)
st.subheader(f"2. Hourly temperature at {lat}, {lon}")

try:
    df = get_hourly_temperature(lat, lon)
except requests.RequestException:
    st.error("Could not reach the weather service right now. Please try again in a minute.")
    st.stop()

# 지표 및 차트 표시
col1, col2, col3 = st.columns(3)
col1.metric("Now (first hour)", f"{df.iloc[0, 0]:.1f} °C")
col2.metric("Highest", f"{df.iloc[:, 0].max():.1f} °C")
col3.metric("Lowest", f"{df.iloc[:, 0].min():.1f} °C")

st.line_chart(df)
st.caption("Data: Open-Meteo.com (free for non-commercial use).")
```[cite: 7, 8]

#### **3. 날씨 앱 배포하기**[cite: 8]
1. `weather_map.py` 파일도 STEP 5에서 만든 같은 GitHub 저장소에 업로드합니다[cite: 8].
2. Streamlit Cloud에서 다시 **Create app**을 누르고, **Main file path**만 `weather_map.py`로 변경하여 새로 배포합니다 (하나의 GitHub 저장소로 여러 앱 실행 가능)[cite: 8].

---

**다음 단계 안내:**
여기까지 완료하시면 API 키를 안전하게 관리하고 Streamlit Secrets에 저장하는 **STEP 7**으로 넘어가실 수 있습니다[cite: 8]. 다음 단계 설명이 필요하시면 말씀해 주세요!
