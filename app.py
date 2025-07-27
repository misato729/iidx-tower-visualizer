import streamlit as st
from streamlit_elements import dashboard, mui, recharts
import random
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🎵 beatmania IIDX プレイ傾向ダッシュボード")

# -----------------------------
# サンプルデータを自動生成
# -----------------------------
data = []
today = datetime.today()
for i in range(30):
    day = (today - timedelta(days=29 - i)).strftime("%Y-%m-%d")
    data.append({
        "日付": day,
        "鍵盤": random.randint(5000, 30000),
        "スクラッチ": random.randint(200, 3000)
    })

# -----------------------------
# ダッシュボードレイアウト
# -----------------------------
layout = [
    dashboard.Item("keyboard_chart", 0, 0, 6, 4),
    dashboard.Item("scratch_chart", 6, 0, 6, 4),
]

# -----------------------------
# UI描画
# -----------------------------
with dashboard.Grid(layout, draggable=True, resizable=True):
    
    # 🔷 鍵盤グラフ
    with mui.Card(key="keyboard_chart"):
        mui.CardHeader(title="🔷 鍵盤入力数（直近30日）")
        with mui.CardContent():
            recharts.ResponsiveContainer(width="100%", height=250)(
                recharts.LineChart(data=data)(
                    recharts.XAxis(dataKey="日付"),
                    recharts.YAxis(),
                    recharts.Tooltip(),
                    recharts.Legend(),
                    recharts.Line(type="monotone", dataKey="鍵盤", stroke="#8884d8"),
                )
            )

    # 🟠 スクラッチグラフ
    with mui.Card(key="scratch_chart"):
        mui.CardHeader(title="🟠 スクラッチ回数（直近30日）")
        with mui.CardContent():
            recharts.ResponsiveContainer(width="100%", height=250)(
                recharts.LineChart(data=data)(
                    recharts.XAxis(dataKey="日付"),
                    recharts.YAxis(),
                    recharts.Tooltip(),
                    recharts.Legend(),
                    recharts.Line(type="monotone", dataKey="スクラッチ", stroke="#ff7300"),
                )
            )
