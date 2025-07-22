#!/usr/bin/env python3
"""
Debug UI - Test each UI element step by step
"""

import tkinter as tk
from tkinter import ttk

def main():
    # メインウィンドウを作成
    root = tk.Tk()
    root.title("Debug UI Test")
    root.geometry("800x600")
    
    # ウィンドウを前面に表示
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    print("Creating main frame...")
    
    # メインフレーム
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    print("Creating control frame...")
    
    # 左側のコントロール
    control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
    control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
    
    print("Adding labels...")
    
    # ラベルを追加
    ttk.Label(control_frame, text="Test Label 1").pack(anchor=tk.W)
    ttk.Label(control_frame, text="Test Label 2").pack(anchor=tk.W)
    
    print("Adding scales...")
    
    # スライダーを追加
    var1 = tk.DoubleVar(value=5.0)
    scale1 = ttk.Scale(control_frame, from_=0, to=10, variable=var1, orient=tk.HORIZONTAL)
    scale1.pack(fill=tk.X, pady=(0, 10))
    
    var2 = tk.DoubleVar(value=3.0)
    scale2 = ttk.Scale(control_frame, from_=0, to=10, variable=var2, orient=tk.HORIZONTAL)
    scale2.pack(fill=tk.X, pady=(0, 10))
    
    print("Adding buttons...")
    
    # ボタンを追加
    button_frame = ttk.Frame(control_frame)
    button_frame.pack(fill=tk.X, pady=10)
    
    ttk.Button(button_frame, text="Test Button 1").pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(button_frame, text="Test Button 2").pack(side=tk.LEFT)
    
    print("Adding info label...")
    
    # 情報表示
    info_label = ttk.Label(control_frame, text="Debug Info:\nScale1: 5.0\nScale2: 3.0", font=("Arial", 9))
    info_label.pack(pady=10)
    
    print("Creating display frame...")
    
    # 右側の表示エリア
    display_frame = ttk.LabelFrame(main_frame, text="Display Area", padding=10)
    display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # キャンバス
    canvas = tk.Canvas(display_frame, width=400, height=400, bg='lightgray')
    canvas.pack(expand=True)
    
    # キャンバスにテスト図形を描画
    canvas.create_rectangle(50, 50, 350, 350, fill='white', outline='black')
    canvas.create_text(200, 200, text="Test Canvas", font=("Arial", 16))
    
    print("Forcing update...")
    
    # 強制更新
    root.update()
    
    print("UI should be visible now!")
    print("You should see:")
    print("- A window with title 'Debug UI Test'")
    print("- Left side: Controls frame with labels, scales, and buttons")
    print("- Right side: Display area with a gray canvas")
    
    # メインループを開始
    root.mainloop()

if __name__ == "__main__":
    main() 