#!/usr/bin/env python3
"""
Simple Moire Pattern Test
"""

import tkinter as tk
import numpy as np
import os

# macOSでの表示問題を回避
os.environ['TK_SILENCE_DEPRECATION'] = '1'

def main():
    root = tk.Tk()
    root.title("Simple Moire Test")
    root.geometry("800x600")
    root.configure(bg='white')
    
    print("Creating simple moire test...")
    
    # メインフレーム
    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 左側のコントロール
    control_frame = tk.LabelFrame(main_frame, text="Controls", bg='white', fg='black')
    control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
    
    # パラメータ
    freq1 = tk.DoubleVar(value=8.0)
    freq2 = tk.DoubleVar(value=9.0)
    angle1 = tk.DoubleVar(value=0.0)
    angle2 = tk.DoubleVar(value=45.0)
    
    # 周波数1
    tk.Label(control_frame, text="Frequency 1:", bg='white', fg='black').pack(anchor=tk.W)
    freq1_buttons = tk.Frame(control_frame, bg='white')
    freq1_buttons.pack(pady=5)
    tk.Button(freq1_buttons, text="-", command=lambda: change_freq1(-1),
              bg='lightcoral', fg='black', width=3).pack(side=tk.LEFT, padx=2)
    tk.Button(freq1_buttons, text="+", command=lambda: change_freq1(1),
              bg='lightgreen', fg='black', width=3).pack(side=tk.LEFT, padx=2)
    
    # 周波数2
    tk.Label(control_frame, text="Frequency 2:", bg='white', fg='black').pack(anchor=tk.W)
    freq2_buttons = tk.Frame(control_frame, bg='white')
    freq2_buttons.pack(pady=5)
    tk.Button(freq2_buttons, text="-", command=lambda: change_freq2(-1),
              bg='lightcoral', fg='black', width=3).pack(side=tk.LEFT, padx=2)
    tk.Button(freq2_buttons, text="+", command=lambda: change_freq2(1),
              bg='lightgreen', fg='black', width=3).pack(side=tk.LEFT, padx=2)
    
    # 角度1
    tk.Label(control_frame, text="Angle 1:", bg='white', fg='black').pack(anchor=tk.W)
    angle1_buttons = tk.Frame(control_frame, bg='white')
    angle1_buttons.pack(pady=5)
    tk.Button(angle1_buttons, text="-10°", command=lambda: change_angle1(-10),
              bg='lightcoral', fg='black', width=6).pack(side=tk.LEFT, padx=2)
    tk.Button(angle1_buttons, text="+10°", command=lambda: change_angle1(10),
              bg='lightgreen', fg='black', width=6).pack(side=tk.LEFT, padx=2)
    
    # 角度2
    tk.Label(control_frame, text="Angle 2:", bg='white', fg='black').pack(anchor=tk.W)
    angle2_buttons = tk.Frame(control_frame, bg='white')
    angle2_buttons.pack(pady=5)
    tk.Button(angle2_buttons, text="-10°", command=lambda: change_angle2(-10),
              bg='lightcoral', fg='black', width=6).pack(side=tk.LEFT, padx=2)
    tk.Button(angle2_buttons, text="+10°", command=lambda: change_angle2(10),
              bg='lightgreen', fg='black', width=6).pack(side=tk.LEFT, padx=2)
    
    # 情報表示
    info_label = tk.Label(control_frame, text="", bg='white', fg='black', font=('Arial', 9))
    info_label.pack(pady=10)
    
    # 右側のキャンバス
    display_frame = tk.LabelFrame(main_frame, text="Moire Pattern", bg='white', fg='black')
    display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(display_frame, width=400, height=400, bg='white', highlightbackground='black')
    canvas.pack(expand=True, padx=10, pady=10)
    
    def change_freq1(delta):
        new_value = max(1, min(20, freq1.get() + delta))
        freq1.set(new_value)
        draw_moire()
        update_info()
    
    def change_freq2(delta):
        new_value = max(1, min(20, freq2.get() + delta))
        freq2.set(new_value)
        draw_moire()
        update_info()
    
    def change_angle1(delta):
        new_value = (angle1.get() + delta) % 180
        angle1.set(new_value)
        draw_moire()
        update_info()
    
    def change_angle2(delta):
        new_value = (angle2.get() + delta) % 180
        angle2.set(new_value)
        draw_moire()
        update_info()
    
    def update_info():
        info_text = f"Freq1: {freq1.get():.1f}\n"
        info_text += f"Freq2: {freq2.get():.1f}\n"
        info_text += f"Angle1: {angle1.get():.1f}°\n"
        info_text += f"Angle2: {angle2.get():.1f}°"
        info_label.config(text=info_text)
    
    def draw_moire():
        try:
            print("Drawing moire pattern...")
            canvas.delete("all")
            
            # グリッド作成
            width, height = 400, 400
            x = np.linspace(-5, 5, width)
            y = np.linspace(-5, 5, height)
            X, Y = np.meshgrid(x, y)
            
            # 第1パターン
            angle1_rad = np.radians(angle1.get())
            rotated_x1 = X * np.cos(angle1_rad) + Y * np.sin(angle1_rad)
            pattern1 = np.sin(2 * np.pi * freq1.get() * rotated_x1)
            
            # 第2パターン
            angle2_rad = np.radians(angle2.get())
            rotated_x2 = X * np.cos(angle2_rad) + Y * np.sin(angle2_rad)
            pattern2 = np.sin(2 * np.pi * freq2.get() * rotated_x2)
            
            # モアレパターン
            moire_pattern = pattern1 * pattern2
            
            # キャンバスに描画
            step = 4  # 描画間隔
            for i in range(0, width, step):
                for j in range(0, height, step):
                    value = moire_pattern[i, j]
                    # 値に基づいて色を決定
                    if value > 0.5:
                        color = 'black'
                    elif value < -0.5:
                        color = 'white'
                    else:
                        color = 'gray'
                    
                    canvas.create_oval(i, j, i+2, j+2, fill=color, outline=color)
            
            print("Moire pattern drawn!")
            
        except Exception as e:
            print(f"Error drawing moire: {e}")
            # エラー時は簡単なパターンを描画
            canvas.delete("all")
            for i in range(0, 400, 20):
                for j in range(0, 400, 20):
                    if (i + j) % 40 == 0:
                        canvas.create_oval(i, j, i+10, j+10, fill='black', outline='black')
                    else:
                        canvas.create_oval(i, j, i+10, j+10, fill='gray', outline='gray')
            canvas.create_text(200, 200, text="Error", font=("Arial", 16, "bold"), fill='red')
    
    # 初期描画
    print("Drawing initial moire pattern...")
    draw_moire()
    update_info()
    
    print("Simple moire test should be visible now!")
    print("Try clicking the buttons to change the pattern!")
    
    root.mainloop()

if __name__ == "__main__":
    main() 