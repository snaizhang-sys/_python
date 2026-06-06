import streamlit as st
import requests
import pandas as pd

# =========================
# 頁面設定
# =========================
st.set_page_config(
    page_title="美股週漲幅分析器",
    layout="wide"
)

st.title("📈 美股每週漲幅排行榜")

# =========================
# 側邊欄設定
# =========================
st.sidebar.header("查詢設定")

api_token = st.sidebar.text_input(
    "輸入您的 iTick Token",
    type="password"
)

stock_input = st.sidebar.text_area(
    "輸入股票代號 (以逗號分隔)",
    "AAPL,TSLA,NVDA,MSFT,AMD"
)

top_n = st.sidebar.number_input(
    "顯示前幾大漲幅",
    min_value=1,
    max_value=100,
    value=5,
    step=1
)

# =========================
# API查詢函式
# =========================
def get_weekly_change(symbol, token):

    url = "https://api.itick.io/stock/info"

    headers = {
        "token": token
    }

    params = {
        "type": "stock",
        "region": "US",
        "code": symbol
    }

    try:
        res = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        if res.status_code != 200:
            return None

        data = res.json()

        return {
            "Symbol": symbol,
            "Price": data.get("price", 0),
            "WeeklyChange": data.get("change_week", 0)
        }

    except Exception as e:
        print(e)
        return None


# =========================
# 查詢按鈕
# =========================
if st.sidebar.button("🚀 開始查詢"):

    if not api_token:
        st.error("請先輸入 API Token！")

    else:

        stocks = [
            s.strip().upper()
            for s in stock_input.split(",")
            if s.strip()
        ]

        results = []

        with st.spinner("正在從 iTick 取得資料..."):

            for symbol in stocks:

                data = get_weekly_change(
                    symbol,
                    api_token
                )

                if data:
                    results.append(data)

        # =========================
        # 顯示結果
        # =========================
        if len(results) > 0:

            df = pd.DataFrame(results)

            # 依週漲幅排序
            df = df.sort_values(
                by="WeeklyChange",
                ascending=False
            )

            # 只顯示前 N 名
            df = df.head(top_n)

            # 新增排名欄位
            df.insert(
                0,
                "Rank",
                range(1, len(df) + 1)
            )

            st.success(
                f"成功取得 {len(results)} 檔股票資料"
            )

            st.subheader(
                f"🏆 漲幅前 {top_n} 名排行榜"
            )

            # 百分比格式
            display_df = df.copy()

            display_df["WeeklyChange"] = (
                display_df["WeeklyChange"]
                .astype(float)
                .round(2)
            )

            display_df["Price"] = (
                display_df["Price"]
                .astype(float)
                .round(2)
            )

            st.dataframe(
                display_df.style.background_gradient(
                    subset=["WeeklyChange"],
                    cmap="Greens"
                ),
                use_container_width=True
            )

            # 長條圖
            st.subheader("📊 週漲幅視覺化")

            chart_df = df.set_index("Symbol")

            st.bar_chart(
                chart_df["WeeklyChange"]
            )

        else:
            st.warning(
                "無法取得資料，請確認 Token 或股票代號。"
            )

# =========================
# 頁尾
# =========================
st.markdown("---")
st.caption(
    "提示：請確認輸入的股票代號符合美股市場格式，例如 AAPL、TSLA、NVDA。"
)