import streamlit as st
import pandas as pd

dataFrame = pd.read_csv("各鄉鎮市區人口密度.csv", encoding="utf-8")
dataFrame.columns = ["統計年", "區域別", "年底人口數", "土地面積", "人口密度"]
df = dataFrame.drop(index=0)
df2 = df.drop("統計年", axis=1)
df2["年底人口數"] = pd.to_numeric(df2["年底人口數"], errors="coerce")
df2 = df2.dropna(subset=["年底人口數"])
df2["年底人口數"] = df2["年底人口數"].astype("int64")
df2["土地面積"] = df2["土地面積"].astype("float")
df2["人口密度"] = df2["人口密度"].astype("int64")

st.title("各鄉鎮市區人口密度查詢")

region = st.selectbox("請選擇區域", df2["區域別"].tolist())

if region:
    row = df2[df2["區域別"] == region].iloc[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("年底人口數", f"{row['年底人口數']:,}")
    col2.metric("土地面積 (km²)", f"{row['土地面積']:.4f}")
    col3.metric("人口密度 (人/km²)", f"{row['人口密度']:,}")

    st.dataframe(
        df2[df2["區域別"] == region][["區域別", "年底人口數", "土地面積", "人口密度"]],
        hide_index=True,
    )
