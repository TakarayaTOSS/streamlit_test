import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def app():
    # Streamlitのタイトル設定
    st.title('地点指定による気温データの表示')

    # 地図の表示
    map_data = pd.DataFrame({'lat': [31.731439977203646], 'lon': [130.72877999636088]})
    st.map(map_data)

    # ユーザーに緯度と経度を入力させる
    lat = st.number_input('緯度を入力してください', value=31.731439977203646)  # デフォルトの緯度
    lon = st.number_input('経度を入力してください', value=130.72877999636088)  # デフォルトの経度

    # 日付の範囲を設定
    today = datetime.now()
    start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = (today + timedelta(days=7)).strftime('%Y-%m-%d')

    # OpenMeteo APIへのリクエスト
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start={start_date}&end={end_date}&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    # データの整理
    times = [datetime.fromisoformat(t) for t in data['hourly']['time']]
    temperatures = data['hourly']['temperature_2m']
    df = pd.DataFrame({'Time': times, 'Temperature': temperatures})

    # グラフの描画
    plt.figure(figsize=(10, 4))
    plt.plot(df['Time'], df['Temperature'], marker='o')
    plt.axvline(x=today, color='red', linestyle='--')  # 現在の日時に縦線を追加
    plt.title('Temperature Over Time')
    plt.xlabel('Date and Time')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Streamlitにグラフを表示
    st.pyplot(plt)
