import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")
st.title("🎵 beatmania IIDX プレイ傾向ダッシュボード")

# ✅ サンプルデータを自動生成（30日分）
data = []
today = datetime.today()
for i in range(30):
    day = (today - timedelta(days=29 - i)).strftime("%Y-%m-%d")
    data.append({
        "日付": day,
        "鍵盤": random.randint(5000, 30000),
        "スクラッチ": random.randint(200, 3000)
    })

df = pd.DataFrame(data)

# ✅ UIレイアウト：2列カード風に表示
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔷 鍵盤入力数（直近30日）")
    fig1 = px.line(df, x="日付", y="鍵盤", markers=True, height=300)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### 🟠 スクラッチ回数（直近30日）")
    fig2 = px.line(df, x="日付", y="スクラッチ", markers=True, height=300)
    st.plotly_chart(fig2, use_container_width=True)

# ✅ 集計表示
st.markdown("---")
st.markdown("### 📊 総合統計")
col3, col4 = st.columns(2)
col3.metric("総鍵盤数", f"{df['鍵盤'].sum():,}")
col4.metric("総スクラッチ数", f"{df['スクラッチ'].sum():,}")
