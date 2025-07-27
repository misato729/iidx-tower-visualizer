import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
st.title("🎵 beatmania IIDX プレイ傾向ダッシュボード")

uploaded_file = st.file_uploader("📁 プレイデータCSVをアップロードしてください", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df["プレー日"] = pd.to_datetime(df["プレー日"])
        df = df.sort_values("プレー日")
        df["月"] = df["プレー日"].dt.to_period("M").astype(str)

        # 📈 Plotly: 鍵盤（左軸）＋スクラッチ10倍（右軸）
        st.markdown("### 📈 鍵盤 & スクラッチ（10倍）入力数推移")
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=df["プレー日"], y=df["鍵盤"], mode="lines+markers", name="鍵盤", line=dict(color="#636EFA")),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(x=df["プレー日"], y=df["スクラッチ"] * 10, mode="lines+markers", name="スクラッチ ×10", line=dict(color="#FF4D4D")),
            secondary_y=True
        )

        fig.update_layout(
            height=450,
            plot_bgcolor="#F5F5F5",  # 薄グレー背景
            paper_bgcolor="#F5F5F5",
            hovermode="x unified",
            legend=dict(bgcolor="#F5F5F5")
        )

        fig.update_yaxes(title_text="鍵盤", secondary_y=False)
        fig.update_yaxes(title_text="スクラッチ ×10", secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)

        # 📅 月別集計 + 平均行
        summary = df.groupby("月").agg({
            "鍵盤": "sum",
            "スクラッチ": "sum"
        }).reset_index()

        avg_row = {
            "月": "平均",
            "鍵盤": int(df["鍵盤"].mean()),
            "スクラッチ": int(df["スクラッチ"].mean())
        }

        summary = pd.concat([summary, pd.DataFrame([avg_row])], ignore_index=True)

        st.markdown("### 📊 月別合計 + 平均")
        st.dataframe(summary, use_container_width=True)

        # ✅ 総合統計（全期間合計）
        st.markdown("---")
        st.markdown("### 🧮 総合統計")
        col1, col2 = st.columns(2)
        col1.metric("総鍵盤数", f"{df['鍵盤'].sum():,}")
        col2.metric("総スクラッチ数", f"{df['スクラッチ'].sum():,}")

    except Exception as e:
        st.error(f"❌ エラー: {e}")
else:
    st.info("CSVファイルをアップロードしてください。")
