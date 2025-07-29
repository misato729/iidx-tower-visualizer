import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from streamlit_elements import mui, dashboard, elements

# ページ設定
st.set_page_config(layout="wide")
st.title("🎵 beatmania IIDX プレイ傾向ダッシュボード")

# CSVアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 日付変換と並び替え
    df["プレー日"] = pd.to_datetime(df["プレー日"])
    df = df.sort_values("プレー日")

    # 月単位の集計
    df["月"] = df["プレー日"].dt.to_period("M")
    monthly_sum = df.groupby("月")[["鍵盤", "スクラッチ"]].sum().reset_index()
    monthly_sum["月"] = monthly_sum["月"].astype(str)

    # 全期間の月平均
    average_row = pd.DataFrame({
        "月": ["月平均"],
        "鍵盤": [int(monthly_sum["鍵盤"].mean())],
        "スクラッチ": [int(monthly_sum["スクラッチ"].mean())]
    })

    # 結合して表に
    monthly_table = pd.concat([monthly_sum, average_row], ignore_index=True)

    # ダッシュボードレイアウト
    layout = [
        dashboard.Item("line_chart", 0, 0, 12, 5),
        dashboard.Item("stats_table", 0, 5, 12, 3),
    ]

    with elements("dashboard"):
        with dashboard.Grid(layout, draggable=False, resizable=True):

            # 📈 折れ線グラフ（Y軸共有）
            with mui.Card(key="line_chart"):
                mui.CardHeader(title="📈 鍵盤 & スクラッチ（10倍）入力数推移（Y軸共有）")
                with mui.CardContent():
                    fig = go.Figure()

                        # 🔵 鍵盤（左Y軸）
                        fig.add_trace(go.Scatter(
                            x=df["プレー日"], y=df["鍵盤"],
                            mode="lines+markers", name="鍵盤", line=dict(color="blue"),
                            yaxis="y1"
                        ))
                        
                        # 🔴 スクラッチ（右Y軸）→ 実数を表示、軸だけ1/10スケールにする
                        fig.add_trace(go.Scatter(
                            x=df["プレー日"], y=df["スクラッチ"],
                            mode="lines+markers", name="スクラッチ",
                            line=dict(color="red"),
                            yaxis="y2"
                        ))
                        
                        # 背景・軸設定
                        fig.update_layout(
                            height=400,
                            plot_bgcolor="#F5F5F5",
                            paper_bgcolor="#F5F5F5",
                            hovermode="x unified",
                            legend=dict(bgcolor="#F5F5F5"),
                            yaxis=dict(  # 左軸（鍵盤）
                                title="鍵盤",
                                showgrid=True,
                            ),
                            yaxis2=dict(  # 右軸（スクラッチ）
                                title="スクラッチ",
                                overlaying='y',
                                side='right',
                                showgrid=False,
                                range=[
                                    df["鍵盤"].min() / 10,
                                    df["鍵盤"].max() / 10
                                ]
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)


            # 📊 月別表
            with mui.Card(key="stats_table"):
                mui.CardHeader(title="📊 月別 合計入力数 & 月平均")
                with mui.CardContent():
                    st.dataframe(monthly_table.style.format(thousands=","), use_container_width=True)
