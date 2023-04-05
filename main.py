import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkinter import StringVar

class AccountApp:
    def __init__(self, master):
        self.master = master
        self.master.title("产品销售记录")
        self.master.geometry("900x600")

        self.create_widgets()
        self.create_database()
        self.load_transactions()
        self.load_product_names()
        self.calculate_total_profit()

    def create_widgets(self):
        # 标题
        self.title_label = ttk.Label(self.master, text="产品销售记录", font=("Arial", 20))
        self.title_label.grid(row=0, column=1, padx=10, pady=10)

        # 交易记录列表
        self.transactions_listbox = tk.Listbox(self.master, width=50)
        self.transactions_listbox.grid(row=1, column=0, rowspan=6, padx=10, pady=10, sticky="ns")

        # 产品名称
        self.name_label = ttk.Label(self.master, text="产品名称")
        self.name_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.name_combobox = ttk.Combobox(self.master)
        self.name_combobox.grid(row=1, column=2, padx=10, pady=5)


        # 进价
        self.cost_label = ttk.Label(self.master, text="进价")
        self.cost_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.cost_entry = ttk.Entry(self.master)
        self.cost_entry.grid(row=2, column=2, padx=10, pady=5)

        # 售价
        self.price_label = ttk.Label(self.master, text="售价")
        self.price_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.price_entry = ttk.Entry(self.master)
        self.price_entry.grid(row=3, column=2, padx=10, pady=5)

        # 销售数量
        self.quantity_label = ttk.Label(self.master, text="销售数量")
        self.quantity_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(self.master)
        self.quantity_entry.grid(row=4, column=2, padx=10, pady=5)

        # 按钮
        self.add_button = ttk.Button(self.master, text="添加", command=self.add_transaction)
        self.add_button.grid(row=5, column=1, padx=10, pady=5)
        self.delete_button = ttk.Button(self.master, text="删除", command=self.delete_transaction)
        self.delete_button.grid(row=5, column=2, padx=10, pady=5)

        # 总利润标签
        self.total_profit_label = ttk.Label(self.master, text="总利润: 0")
        self.total_profit_label.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

        # 总销售数量标签
        self.total_sales_label_var = StringVar(self.master)
        self.total_sales_label = ttk.Label(self.master, textvariable=self.total_sales_label_var)
        self.total_sales_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.total_sales_label_var.set("所选产品总销售数量: 0")

    def create_database(self):
        self.conn = sqlite3.connect("transactions.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                name TEXT,
                cost REAL,
                price REAL,
                quantity INTEGER,
                profit REAL,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def load_transactions(self):
        self.transactions_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM transactions")
        rows = self.cursor.fetchall()
        for row in rows:
            self.transactions_listbox.insert(tk.END, f"{row[1]} - 数量: {row[4]} - 利润: {row[5]} - 时间: {row[6]}")
        # 添加此行以绑定所选事件
        self.transactions_listbox.bind("<<ListboxSelect>>", self.display_product_sales)
        
    def add_transaction(self):
        name = self.name_combobox.get()
        cost = float(self.cost_entry.get())
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        profit = (price - cost) * quantity
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if name and cost and price and quantity:
            self.cursor.execute("INSERT INTO transactions (name, cost, price, quantity, profit, timestamp) VALUES (?, ?, ?, ?, ?, ?)", (name, cost, price, quantity, profit, timestamp))
            self.conn.commit()
            self.transactions_listbox.insert(tk.END, f"{name} - 数量: {quantity} - 利润: {profit} - 时间: {timestamp}")

            # 清除输入框
            self.name_combobox.set('')
            self.cost_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)

            # 更新总利润
            self.calculate_total_profit()
    def load_product_names(self):
            self.cursor.execute("SELECT DISTINCT name FROM transactions")
            product_names = [row[0] for row in self.cursor.fetchall()]
            self.name_combobox["values"] = product_names
        

    def delete_transaction(self):
        selected = self.transactions_listbox.curselection()
        if selected:
            self.cursor.execute("DELETE FROM transactions WHERE id=?", (selected[0] + 1,))
            self.conn.commit()
            self.transactions_listbox.delete(selected)
            self.calculate_total_profit()

    def calculate_total_profit(self):
        self.cursor.execute("SELECT SUM(profit) FROM transactions")
        total_profit = self.cursor.fetchone()[0]
        if total_profit is None:
            total_profit = 0
        self.total_profit_label.config(text=f"总利润: {total_profit}")

    def close_database(self):
        self.conn.close()
    def display_product_sales(self, event):
        selected = self.transactions_listbox.curselection()
        if selected:
            self.cursor.execute("SELECT name FROM transactions WHERE id=?", (selected[0] + 1,))
            product_name = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT SUM(quantity) FROM transactions WHERE name=?", (product_name,))
            total_sales = self.cursor.fetchone()[0]
            if total_sales is None:
                total_sales = 0
            self.total_sales_label_var.set(f"所选产品总销售数量: {total_sales}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AccountApp(root)
    root.mainloop()
    app.close_database()