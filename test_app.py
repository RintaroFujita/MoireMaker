#!/usr/bin/env python3
"""
Test Application - Simple Window
"""

import tkinter as tk
from tkinter import ttk

def main():
    # メインウィンドウを作成
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("400x300")
    
    # ウィンドウを前面に表示
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    # ラベルを追加
    label = ttk.Label(root, text="Hello! This is a test window.", font=("Arial", 16))
    label.pack(expand=True)
    
    # ボタンを追加
    button = ttk.Button(root, text="Click me!", command=lambda: print("Button clicked!"))
    button.pack(pady=20)
    
    print("Window should be visible now!")
    
    # メインループを開始
    root.mainloop()

if __name__ == "__main__":
    main() 