import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ✅ フォント読み込み（Noto Sans JP）
font_path = "fonts/NotoSansJP-Regular.ttf"
font_prop = fm.FontProperties(fname=font_path)

# デバッグ：フォント名の確認（ローカル実行時のみ出力）
print("✅ 読み込んだフォント名:", font_prop.get_name())

# 🔽 Streamlitアプリ開始
st.title("beatmania IIDX プレイ傾向ダッシュボード")

# ✅ CSVファイルアップロード
uploaded_file = st.file_uploader("プレイデータCSVをアップロードしてください", type="csv")
if uploaded_file:
    # CSV読み込み
    df = pd.read_csv(uploaded_file)
    df["プレー日"] = pd.to_datetime(df["プレー日"])
    df = df.sort_values("プレー日")

    # 📈 折れ線グラフ：鍵盤 & スクラッチ
    st.subheader("日別プレイ入力数（鍵盤・スクラッチ）")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["プレー日"], df["鍵盤"], label="鍵盤", marker="o")
    ax.plot(df["プレー日"], df["スクラッチ"], label="スクラッチ", marker="x")

    # ✅ 日本語フォントを適用
    ax.set_title("日別プレイ入力数（鍵盤・スクラッチ）", fontproperties=font_prop)
    ax.set_xlabel("日付", fontproperties=font_prop)
    ax.set_ylabel("入力数", fontproperties=font_prop)
    ax.legend(prop=font_prop)
    ax.grid(True)

    # グラフ表示
    st.pyplot(fig)

    # 📊 総合統計表示
    st.subheader("総合統計")
    st.metric("総鍵盤数", int(df["鍵盤"].sum()))
    st.metric("総スクラッチ数", int(df["スクラッチ"].sum()))
else:
    st.info("CSVファイルをアップロードしてください。")
