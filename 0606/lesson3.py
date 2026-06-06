import requests
import pandas as pd
from requests import Response

def main():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    response: Response = requests.get(url)

    if response.status_code == 200:
        data: list[dict] = response.json()

        print("下載成功")
        print(f"共 {len(data)} 筆資料")

        # 轉成 DataFrame
        df = pd.DataFrame(data)

        # 匯出 Excel
        file_name = "YouBike即時資料.xlsx"
        df.to_excel(file_name, index=False)

        print(f"已匯出：{file_name}")

    else:
        print("下載失敗")
        print(response.status_code)

if __name__ == '__main__':
    main()
    