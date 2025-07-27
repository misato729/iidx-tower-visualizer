import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV読み込み
uploaded_file = st.file_uploader("プレイデータCSVをアップロードしてください", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["プレー日"] = pd.to_datetime(df["プレー日"])
    df = df.sort_values("プレー日")

    st.title("beatmania IIDX プレイ傾向ダッシュボード")

    st.subheader("日別プレイ入力数（鍵盤・スクラッチ）")
    fig, ax = plt.subplots()
    ax.plot(df["プレー日"], df["鍵盤"], label="鍵盤", marker="o")
    ax.plot(df["プレー日"], df["スクラッチ"], label="スクラッチ", marker="x")
    ax.set_xlabel("日付")
    ax.set_ylabel("入力数")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.subheader("総合統計")
    st.metric("総鍵盤数", int(df["鍵盤"].sum()))
    st.metric("総スクラッチ数", int(df["スクラッチ"].sum()))
