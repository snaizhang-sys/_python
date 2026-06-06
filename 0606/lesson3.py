import streamlit as st
import requests
import pandas as pd

# 設定頁面標題
st.set_page_config(page_title="美股週漲幅分析器", layout="wide")
st.title("📈 美股每週漲幅排行榜")

# 側邊欄：輸入區
st.sidebar.header("設定")
api_token = st.sidebar.text_input("輸入您的 iTick Token", type="password")
stock_input = st.sidebar.text_area("輸入股票代號 (以逗號分隔)", "AAPL,TSLA,NVDA,MSFT,AMD")

def get_weekly_change(symbol, token):
    url = "https://api.itick.io/stock/info" # 請依據 iTick 實際文件調整端點
    headers = {"token": token}
    params = {"type": "stock", "region": "US", "code": symbol}
    
    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        # 假設 API 回傳包含 change_week 或相關漲幅數據
        # 實際請依照您 API 回傳的 JSON 結構調整此處欄位名稱
        return {
            "Symbol": symbol,
            "Price": data.get("price"),
            "WeeklyChange": data.get("change_week", 0) 
        }
    except:
        return None

if st.sidebar.button("開始查詢"):
    if not api_token:
        st.error("請先輸入 API Token！")
    else:
        stocks = [s.strip() for s in stock_input.split(",")]
        results = []
        
        with st.spinner('正在從 iTick 獲取數據...'):
            for s in stocks:
                data = get_weekly_change(s, api_token)
                if data:
                    results.append(data)
        
        if results:
            df = pd.DataFrame(results)
            # 依據每週漲幅由高到低排序
            df = df.sort_values(by="WeeklyChange", ascending=False)
            
            st.subheader("漲幅排行結果")
            st.dataframe(df.style.background_gradient(subset=['WeeklyChange'], cmap='Greens'), use_container_width=True)
        else:
            st.warning("無法獲取數據，請檢查代號或 Token。")

st.markdown("---")
st.caption("提示：請確保輸入的代號符合美股市場格式。")