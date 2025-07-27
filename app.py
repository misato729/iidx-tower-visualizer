import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🎵 beatmania IIDX プレイ傾向ダッシュボード")

uploaded_file = st.file_uploader("📁 プレイデータCSVをアップロードしてください", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df["プレー日"] = pd.to_datetime(df["プレー日"])
        df = df.sort_values("プレー日")
        df["月"] = df["プレー日"].dt.to_period("M").astype(str)

        # ✅ 鍵盤・スクラッチを縦持ちに変換
        melted = df.melt(id_vars=["プレー日", "月"], value_vars=["鍵盤", "スクラッチ"],
                         var_name="種別", value_name="入力数")

        # ✅ Plotlyグラフ：背景を薄いピンク + スクラッチは赤
        st.markdown("### 📈 鍵盤 & スクラッチ 入力数推移")
        fig = px.line(
            melted,
            x="プレー日",
            y="入力数",
            color="種別",
            color_discrete_map={
                "鍵盤": "#636EFA",       # デフォルト青
                "スクラッチ": "#FF4D4D"  # 鮮やかな赤
            },
            markers=True,
            height=400
        )

        # ✅ 背景色変更（薄いピンク）
        fig.update_layout(
            plot_bgcolor="#FFF0F5",    # 薄ピンク (LavenderBlush)
            paper_bgcolor="#FFF0F5",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ✅ 月ごとの合計・平均集計
        summary = df.groupby("月").agg({
            "鍵盤": ["sum", "mean"],
            "スクラッチ": ["sum", "mean"]
        }).round().astype(int)

        summary.columns = ["鍵盤_合計", "鍵盤_平均", "スクラッチ_合計", "スクラッチ_平均"]
        summary = summary.reset_index()

        st.markdown("### 📅 月別集計")
        st.dataframe(summary, use_container_width=True)

        # ✅ 合計表示
        st.markdown("---")
        st.markdown("### 📊 総合統計")
        col1, col2 = st.columns(2)
        col1.metric("総鍵盤数", f"{df['鍵盤'].sum():,}")
        col2.metric("総スクラッチ数", f"{df['スクラッチ'].sum():,}")

    except Exception as e:
        st.error(f"❌ エラー: {e}")
else:
    st.info("CSVファイルをアップロードしてください。")
