#!/usr/bin/env python3
"""
Button-based Moire Pattern Generator - Using buttons instead of sliders
"""

import tkinter as tk
import numpy as np
import os

# macOSでの表示問題を回避
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class ButtonMoireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Button Moire Generator")
        self.root.geometry("1000x700")
        
        # macOSでの表示設定
        self.root.configure(bg='white')
        
        # パラメータ
        self.freq1 = 8.0
        self.freq2 = 9.0
        self.angle1 = 0.0
        self.angle2 = 45.0
        self.phase1 = 0.0
        self.phase2 = 0.0
        
        # キャンバスサイズ
        self.width = 400
        self.height = 400
        
        print("Setting up button-based UI...")
        self.setup_ui()
        print("Creating initial pattern...")
        self.create_pattern()
        
        # アニメーション用変数
        self.animation_running = False
        self.animation_id = None
        
        print("Button app should be visible now!")
    
    def setup_ui(self):
        # メインフレーム
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左側のコントロール
        control_frame = tk.LabelFrame(main_frame, text="Controls", bg='white', fg='black', 
                                     font=('Arial', 12, 'bold'))
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        print("Adding frequency controls...")
        
        # 周波数1
        freq1_frame = tk.LabelFrame(control_frame, text="Frequency 1", bg='white', fg='black')
        freq1_frame.pack(fill=tk.X, pady=5)
        
        self.freq1_var = tk.DoubleVar(value=self.freq1)
        self.freq1_label = tk.Label(freq1_frame, text=f"{self.freq1:.1f}", 
                                   bg='white', fg='black', font=('Arial', 12, 'bold'))
        self.freq1_label.pack()
        
        freq1_buttons = tk.Frame(freq1_frame, bg='white')
        freq1_buttons.pack(pady=5)
        
        tk.Button(freq1_buttons, text="-", command=lambda: self.change_freq1(-1),
                 bg='lightcoral', fg='black', width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(freq1_buttons, text="+", command=lambda: self.change_freq1(1),
                 bg='lightgreen', fg='black', width=3).pack(side=tk.LEFT, padx=2)
        
        # 周波数2
        freq2_frame = tk.LabelFrame(control_frame, text="Frequency 2", bg='white', fg='black')
        freq2_frame.pack(fill=tk.X, pady=5)
        
        self.freq2_var = tk.DoubleVar(value=self.freq2)
        self.freq2_label = tk.Label(freq2_frame, text=f"{self.freq2:.1f}", 
                                   bg='white', fg='black', font=('Arial', 12, 'bold'))
        self.freq2_label.pack()
        
        freq2_buttons = tk.Frame(freq2_frame, bg='white')
        freq2_buttons.pack(pady=5)
        
        tk.Button(freq2_buttons, text="-", command=lambda: self.change_freq2(-1),
                 bg='lightcoral', fg='black', width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(freq2_buttons, text="+", command=lambda: self.change_freq2(1),
                 bg='lightgreen', fg='black', width=3).pack(side=tk.LEFT, padx=2)
        
        print("Adding angle controls...")
        
        # 角度1
        angle1_frame = tk.LabelFrame(control_frame, text="Angle 1 (degrees)", bg='white', fg='black')
        angle1_frame.pack(fill=tk.X, pady=5)
        
        self.angle1_var = tk.DoubleVar(value=self.angle1)
        self.angle1_label = tk.Label(angle1_frame, text=f"{self.angle1:.1f}°", 
                                    bg='white', fg='black', font=('Arial', 12, 'bold'))
        self.angle1_label.pack()
        
        angle1_buttons = tk.Frame(angle1_frame, bg='white')
        angle1_buttons.pack(pady=5)
        
        tk.Button(angle1_buttons, text="-10°", command=lambda: self.change_angle1(-10),
                 bg='lightcoral', fg='black', width=6).pack(side=tk.LEFT, padx=2)
        tk.Button(angle1_buttons, text="+10°", command=lambda: self.change_angle1(10),
                 bg='lightgreen', fg='black', width=6).pack(side=tk.LEFT, padx=2)
        
        # 角度2
        angle2_frame = tk.LabelFrame(control_frame, text="Angle 2 (degrees)", bg='white', fg='black')
        angle2_frame.pack(fill=tk.X, pady=5)
        
        self.angle2_var = tk.DoubleVar(value=self.angle2)
        self.angle2_label = tk.Label(angle2_frame, text=f"{self.angle2:.1f}°", 
                                    bg='white', fg='black', font=('Arial', 12, 'bold'))
        self.angle2_label.pack()
        
        angle2_buttons = tk.Frame(angle2_frame, bg='white')
        angle2_buttons.pack(pady=5)
        
        tk.Button(angle2_buttons, text="-10°", command=lambda: self.change_angle2(-10),
                 bg='lightcoral', fg='black', width=6).pack(side=tk.LEFT, padx=2)
        tk.Button(angle2_buttons, text="+10°", command=lambda: self.change_angle2(10),
                 bg='lightgreen', fg='black', width=6).pack(side=tk.LEFT, padx=2)
        
        print("Adding phase controls...")
        
        # 位相1
        phase1_frame = tk.LabelFrame(control_frame, text="Phase 1", bg='white', fg='black')
        phase1_frame.pack(fill=tk.X, pady=5)
        
        self.phase1_var = tk.DoubleVar(value=self.phase1)
        self.phase1_label = tk.Label(phase1_frame, text=f"{self.phase1:.2f}", 
                                    bg='white', fg='black', font=('Arial', 12, 'bold'))
        self.phase1_label.pack()
        
        phase1_buttons = tk.Frame(phase1_frame, bg='white')
        phase1_buttons.pack(pady=5)
        
        tk.Button(phase1_buttons, text="-0.5", command=lambda: self.change_phase1(-0.5),
                 bg='lightcoral', fg='black', width=6).pack(side=tk.LEFT, padx=2)
        tk.Button(phase1_buttons, text="+0.5", command=lambda: self.change_phase1(0.5),
                 bg='lightgreen', fg='black', width=6).pack(side=tk.LEFT, padx=2)
        
        # 位相2
        phase2_frame = tk.LabelFrame(control_frame, text="Phase 2", bg='white', fg='black')
        phase2_frame.pack(fill=tk.X, pady=5)
        
        self.phase2_var = tk.DoubleVar(value=self.phase2)
        self.phase2_label = tk.Label(phase2_frame, text=f"{self.phase2:.2f}", 
                                    bg='white', fg='black', font=('Arial', 12, 'bold'))
        self.phase2_label.pack()
        
        phase2_buttons = tk.Frame(phase2_frame, bg='white')
        phase2_buttons.pack(pady=5)
        
        tk.Button(phase2_buttons, text="-0.5", command=lambda: self.change_phase2(-0.5),
                 bg='lightcoral', fg='black', width=6).pack(side=tk.LEFT, padx=2)
        tk.Button(phase2_buttons, text="+0.5", command=lambda: self.change_phase2(0.5),
                 bg='lightgreen', fg='black', width=6).pack(side=tk.LEFT, padx=2)
        
        print("Adding control buttons...")
        
        # 制御ボタン
        control_buttons = tk.Frame(control_frame, bg='white')
        control_buttons.pack(fill=tk.X, pady=15)
        
        self.animate_button = tk.Button(control_buttons, text="Start Animation", command=self.toggle_animation,
                                       bg='lightblue', fg='black', relief=tk.RAISED,
                                       font=('Arial', 10, 'bold'), width=15)
        self.animate_button.pack(side=tk.LEFT, padx=(0, 5))
        
        reset_button = tk.Button(control_buttons, text="Reset", command=self.reset,
                                bg='lightgreen', fg='black', relief=tk.RAISED,
                                font=('Arial', 10, 'bold'), width=8)
        reset_button.pack(side=tk.LEFT)
        
        print("Creating display area...")
        
        # 右側の表示エリア
        display_frame = tk.LabelFrame(main_frame, text="Moire Pattern", bg='white', fg='black',
                                     font=('Arial', 12, 'bold'))
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # キャンバス
        self.canvas = tk.Canvas(display_frame, width=self.width, height=self.height, 
                               bg='white', highlightbackground='black')
        self.canvas.pack(expand=True, padx=10, pady=10)
        
        print("Button UI setup complete!")
    
    def change_freq1(self, delta):
        new_value = max(1, min(20, self.freq1_var.get() + delta))
        self.freq1_var.set(new_value)
        self.freq1_label.config(text=f"{new_value:.1f}")
        self.create_pattern()
    
    def change_freq2(self, delta):
        new_value = max(1, min(20, self.freq2_var.get() + delta))
        self.freq2_var.set(new_value)
        self.freq2_label.config(text=f"{new_value:.1f}")
        self.create_pattern()
    
    def change_angle1(self, delta):
        new_value = (self.angle1_var.get() + delta) % 180
        self.angle1_var.set(new_value)
        self.angle1_label.config(text=f"{new_value:.1f}°")
        self.create_pattern()
    
    def change_angle2(self, delta):
        new_value = (self.angle2_var.get() + delta) % 180
        self.angle2_var.set(new_value)
        self.angle2_label.config(text=f"{new_value:.1f}°")
        self.create_pattern()
    
    def change_phase1(self, delta):
        new_value = (self.phase1_var.get() + delta) % (2 * np.pi)
        self.phase1_var.set(new_value)
        self.phase1_label.config(text=f"{new_value:.2f}")
        self.create_pattern()
    
    def change_phase2(self, delta):
        new_value = (self.phase2_var.get() + delta) % (2 * np.pi)
        self.phase2_var.set(new_value)
        self.phase2_label.config(text=f"{new_value:.2f}")
        self.create_pattern()
    
    def create_pattern(self):
        try:
            # グリッド作成
            x = np.linspace(-5, 5, self.width)
            y = np.linspace(-5, 5, self.height)
            X, Y = np.meshgrid(x, y)
            
            # 第1パターン
            angle1_rad = np.radians(self.angle1_var.get())
            rotated_x1 = X * np.cos(angle1_rad) + Y * np.sin(angle1_rad)
            pattern1 = np.sin(2 * np.pi * self.freq1_var.get() * rotated_x1 + self.phase1_var.get())
            
            # 第2パターン
            angle2_rad = np.radians(self.angle2_var.get())
            rotated_x2 = X * np.cos(angle2_rad) + Y * np.sin(angle2_rad)
            pattern2 = np.sin(2 * np.pi * self.freq2_var.get() * rotated_x2 + self.phase2_var.get())
            
            # モアレパターン
            moire_pattern = pattern1 * pattern2
            
            # キャンバスに描画
            self.canvas.delete("all")
            
            # パターンを点で描画
            step = 3  # より細かい描画
            for i in range(0, self.width, step):
                for j in range(0, self.height, step):
                    value = moire_pattern[i, j]
                    # 値に基づいて色を決定
                    if value > 0.5:
                        color = 'black'
                    elif value < -0.5:
                        color = 'white'
                    else:
                        color = 'gray'
                    
                    self.canvas.create_oval(i, j, i+2, j+2, fill=color, outline=color)
            
        except Exception as e:
            print(f"Error creating pattern: {e}")
    
    def reset(self):
        self.freq1_var.set(8.0)
        self.freq2_var.set(9.0)
        self.angle1_var.set(0.0)
        self.angle2_var.set(45.0)
        self.phase1_var.set(0.0)
        self.phase2_var.set(0.0)
        
        self.freq1_label.config(text="8.0")
        self.freq2_label.config(text="9.0")
        self.angle1_label.config(text="0.0°")
        self.angle2_label.config(text="45.0°")
        self.phase1_label.config(text="0.00")
        self.phase2_label.config(text="0.00")
        
        self.create_pattern()
    
    def animate(self):
        if self.animation_running:
            # 位相を更新
            self.change_phase1(0.1)
            self.change_phase2(0.08)
            self.animation_id = self.root.after(100, self.animate)
    
    def toggle_animation(self):
        if not self.animation_running:
            self.animation_running = True
            self.animate_button.config(text="Stop Animation", bg='lightcoral')
            self.animate()
        else:
            self.animation_running = False
            self.animate_button.config(text="Start Animation", bg='lightblue')
            if self.animation_id:
                self.root.after_cancel(self.animation_id)

def main():
    root = tk.Tk()
    app = ButtonMoireApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 