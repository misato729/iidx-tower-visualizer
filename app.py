import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🎵 beatmania IIDX プレイ傾向ダッシュボード")

# 📁 CSVアップロード
uploaded_file = st.file_uploader("📁 プレイデータCSVをアップロードしてください（例：プレー日, 鍵盤, スクラッチ）", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df["プレー日"] = pd.to_datetime(df["プレー日"])
        df = df.sort_values("プレー日")

        # 🔄 データ整形（鍵盤・スクラッチを1列にまとめる）
        melted = df.melt(id_vars="プレー日", value_vars=["鍵盤", "スクラッチ"],
                         var_name="種別", value_name="入力数")

        # 📈 グラフ（1枚に2線）
        st.markdown("### 🔷 鍵盤 / 🟠 スクラッチ 入力数推移（1グラフ）")
        fig = px.line(
            melted,
            x="プレー日",
            y="入力数",
            color="種別",
            markers=True,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # 📊 統計
        st.markdown("---")
        st.markdown("### 📊 総合統計")
        col1, col2 = st.columns(2)
        col1.metric("総鍵盤数", f"{df['鍵盤'].sum():,}")
        col2.metric("総スクラッチ数", f"{df['スクラッチ'].sum():,}")

    except Exception as e:
        st.error(f"❌ エラーが発生しました: {e}")
else:
    st.info("CSVファイルをアップロードしてください。")
