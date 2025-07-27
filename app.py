import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_elements import mui, dashboard

st.set_page_config(layout="wide")
st.title("🎵 beatmania IIDX プレイ傾向ダッシュボード")

# CSVアップロード
uploaded_file = st.file_uploader("プレイデータCSVをアップロードしてください", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["プレー日"] = pd.to_datetime(df["プレー日"])
    df = df.sort_values("プレー日")

    # 月列を追加
    df["月"] = df["プレー日"].dt.to_period("M").astype(str)

    # 月別合計と平均を計算
    monthly_stats = df.groupby("月")[["鍵盤", "スクラッチ"]].sum().reset_index()
    monthly_avg = pd.DataFrame({
        "月": ["平均"],
        "鍵盤": [int(df["鍵盤"].mean())],
        "スクラッチ": [int(df["スクラッチ"].mean())]
    })
    monthly_table = pd.concat([monthly_stats, monthly_avg], ignore_index=True)

    # -----------------------------
    # UIダッシュボード
    # -----------------------------
    layout = [
        dashboard.Item("line_chart", 0, 0, 12, 5),
        dashboard.Item("stats_table", 0, 5, 12, 4),
    ]

    with dashboard.Grid(layout, draggable=False, resizable=True):

        # 📈 折れ線グラフ（Y軸共有）
        with mui.Card(key="line_chart"):
            mui.CardHeader(title="📈 鍵盤 & スクラッチ（10倍）入力数推移（Y軸共有）")
            with mui.CardContent():
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df["プレー日"], y=df["鍵盤"],
                    mode="lines+markers", name="鍵盤", line=dict(color="blue")
                ))
                fig.add_trace(go.Scatter(
                    x=df["プレー日"], y=df["スクラッチ"] * 10,
                    mode="lines+markers", name="スクラッチ ×10", line=dict(color="red")
                ))
                fig.update_layout(
                    height=400,
                    plot_bgcolor="#F5F5F5",
                    paper_bgcolor="#F5F5F5",
                    hovermode="x unified",
                    legend=dict(bgcolor="#F5F5F5"),
                    yaxis_title="入力数（スクラッチは×10）"
                )
                st.plotly_chart(fig, use_container_width=True)

        # 📊 月別入力数 + 月平均（表）
        with mui.Card(key="stats_table"):
            mui.CardHeader(title="📊 月別 合計入力数 & 月平均")
            with mui.CardContent():
                st.dataframe(monthly_table.style.format(thousands=","), use_container_width=True)
