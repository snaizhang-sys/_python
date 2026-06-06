import requests
import tkinter as tk
from tkinter import ttk, messagebox

url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"


class YouBikeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouBike站點查詢")
        self.root.geometry("800x600")

        self.data = []
        self.load_data()

        # 查詢區
        frame = ttk.Frame(root)
        frame.pack(pady=10)

        ttk.Label(frame, text="輸入區域或站名：").pack(side=tk.LEFT)

        self.keyword_var = tk.StringVar()
        self.entry = ttk.Entry(frame, textvariable=self.keyword_var, width=30)
        self.entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(frame, text="查詢", command=self.search).pack(side=tk.LEFT)

        # 結果數量
        self.count_label = ttk.Label(root, text="共 0 個據點")
        self.count_label.pack()

        # 結果列表
        self.text = tk.Text(root, width=100, height=30)
        self.text.pack(padx=10, pady=10)

    def load_data(self):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.data = response.json()
                print(f"成功下載 {len(self.data)} 筆資料")
            else:
                messagebox.showerror("錯誤", "下載資料失敗")
        except Exception as e:
            messagebox.showerror("錯誤", str(e))

    def search(self):
        keyword = self.keyword_var.get().strip().lower()

        self.text.delete(1.0, tk.END)

        if keyword == "":
            messagebox.showwarning("提醒", "請輸入查詢關鍵字")
            return

        results = []

        for site in self.data:
            station_name = site["sna"].lower()
            area = site["sarea"].lower()

            if keyword in station_name or keyword in area:
                results.append(site)

        self.count_label.config(text=f"共找到 {len(results)} 個據點")

        for site in results:
            self.text.insert(
                tk.END,
                f"站名：{site['sna']}\n"
                f"行政區：{site['sarea']}\n"
                f"可借車：{site['available_rent_bikes']}\n"
                f"可還車：{site['available_return_bikes']}\n"
                f"地址：{site['ar']}\n"
                f"{'-'*60}\n"
            )


def main():
    root = tk.Tk()
    app = YouBikeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()