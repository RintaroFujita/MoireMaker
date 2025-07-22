#!/usr/bin/env python3
"""
動的モアレ生成器 ランチャー
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class MoireLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("動的モアレ生成器 ランチャー")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        title_label = ttk.Label(main_frame, text="動的モアレ生成器", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 説明
        desc_label = ttk.Label(main_frame, text="起動したいアプリケーションを選択してください", 
                              font=("Arial", 10))
        desc_label.pack(pady=(0, 20))
        
        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(expand=True)
        
        # 基本アプリケーションボタン
        basic_btn = ttk.Button(button_frame, text="基本モアレアプリケーション", 
                              command=self.launch_basic, width=25)
        basic_btn.pack(pady=10)
        
        # 高度なアプリケーションボタン
        advanced_btn = ttk.Button(button_frame, text="高度なモアレアプリケーション", 
                                 command=self.launch_advanced, width=25)
        advanced_btn.pack(pady=10)
        
        # 情報ボタン
        info_btn = ttk.Button(button_frame, text="アプリケーション情報", 
                             command=self.show_info, width=25)
        info_btn.pack(pady=10)
        
        # 終了ボタン
        exit_btn = ttk.Button(button_frame, text="終了", 
                             command=self.root.quit, width=25)
        exit_btn.pack(pady=10)
        
        # ステータスラベル
        self.status_label = ttk.Label(main_frame, text="", font=("Arial", 9))
        self.status_label.pack(pady=(20, 0))
    
    def launch_basic(self):
        """基本アプリケーションを起動"""
        try:
            self.status_label.config(text="基本アプリケーションを起動中...")
            self.root.update()
            
            if os.path.exists("moire_app.py"):
                subprocess.Popen([sys.executable, "moire_app.py"])
                self.status_label.config(text="基本アプリケーションが起動しました")
            else:
                messagebox.showerror("エラー", "moire_app.py が見つかりません")
                self.status_label.config(text="エラー: ファイルが見つかりません")
        except Exception as e:
            messagebox.showerror("エラー", f"アプリケーションの起動に失敗しました: {str(e)}")
            self.status_label.config(text="エラー: 起動に失敗しました")
    
    def launch_advanced(self):
        """高度なアプリケーションを起動"""
        try:
            self.status_label.config(text="高度なアプリケーションを起動中...")
            self.root.update()
            
            if os.path.exists("advanced_moire.py"):
                subprocess.Popen([sys.executable, "advanced_moire.py"])
                self.status_label.config(text="高度なアプリケーションが起動しました")
            else:
                messagebox.showerror("エラー", "advanced_moire.py が見つかりません")
                self.status_label.config(text="エラー: ファイルが見つかりません")
        except Exception as e:
            messagebox.showerror("エラー", f"アプリケーションの起動に失敗しました: {str(e)}")
            self.status_label.config(text="エラー: 起動に失敗しました")
    
    def show_info(self):
        """アプリケーション情報を表示"""
        info_text = """動的モアレ生成器

基本アプリケーション:
- 線形モアレパターンの生成
- リアルタイムアニメーション
- スライダーによるパラメータ制御

高度なアプリケーション:
- 4種類のモアレパターン（線形、円形、ラジアル、スパイラル）
- より詳細なパラメータ制御
- プリセット機能

必要なパッケージ:
- matplotlib
- numpy
- tkinter（標準ライブラリ）

詳細は README.md を参照してください。"""
        
        info_window = tk.Toplevel(self.root)
        info_window.title("アプリケーション情報")
        info_window.geometry("500x400")
        info_window.resizable(False, False)
        
        # 情報テキスト
        text_widget = tk.Text(info_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)
        
        # 閉じるボタン
        close_btn = ttk.Button(info_window, text="閉じる", 
                              command=info_window.destroy)
        close_btn.pack(pady=10)

def main():
    root = tk.Tk()
    app = MoireLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main() 