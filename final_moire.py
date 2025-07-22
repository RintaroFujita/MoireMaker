#!/usr/bin/env python3
"""
Final Moire Pattern Generator - Optimized for macOS
"""

import tkinter as tk
import numpy as np
import os

# macOSでの表示問題を回避
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class FinalMoireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Final Moire Generator")
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
        
        print("Setting up final UI...")
        self.setup_ui()
        print("Creating initial pattern...")
        self.create_pattern()
        
        # アニメーション用変数
        self.animation_running = False
        self.animation_id = None
        
        print("Final app should be visible now!")
        print("If you can see the window, try moving the sliders!")
    
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
        tk.Label(control_frame, text="Frequency 1:", bg='white', fg='black', 
                font=('Arial', 10)).pack(anchor=tk.W, pady=(5, 0))
        self.freq1_var = tk.DoubleVar(value=self.freq1)
        freq1_scale = tk.Scale(control_frame, from_=1, to=20, variable=self.freq1_var, 
                              orient=tk.HORIZONTAL, command=self.update_pattern,
                              bg='white', fg='black', highlightbackground='white',
                              length=200, font=('Arial', 9))
        freq1_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 周波数2
        tk.Label(control_frame, text="Frequency 2:", bg='white', fg='black', 
                font=('Arial', 10)).pack(anchor=tk.W, pady=(5, 0))
        self.freq2_var = tk.DoubleVar(value=self.freq2)
        freq2_scale = tk.Scale(control_frame, from_=1, to=20, variable=self.freq2_var, 
                              orient=tk.HORIZONTAL, command=self.update_pattern,
                              bg='white', fg='black', highlightbackground='white',
                              length=200, font=('Arial', 9))
        freq2_scale.pack(fill=tk.X, pady=(0, 10))
        
        print("Adding angle controls...")
        
        # 角度1
        tk.Label(control_frame, text="Angle 1 (degrees):", bg='white', fg='black', 
                font=('Arial', 10)).pack(anchor=tk.W, pady=(5, 0))
        self.angle1_var = tk.DoubleVar(value=self.angle1)
        angle1_scale = tk.Scale(control_frame, from_=0, to=180, variable=self.angle1_var, 
                               orient=tk.HORIZONTAL, command=self.update_pattern,
                               bg='white', fg='black', highlightbackground='white',
                               length=200, font=('Arial', 9))
        angle1_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 角度2
        tk.Label(control_frame, text="Angle 2 (degrees):", bg='white', fg='black', 
                font=('Arial', 10)).pack(anchor=tk.W, pady=(5, 0))
        self.angle2_var = tk.DoubleVar(value=self.angle2)
        angle2_scale = tk.Scale(control_frame, from_=0, to=180, variable=self.angle2_var, 
                               orient=tk.HORIZONTAL, command=self.update_pattern,
                               bg='white', fg='black', highlightbackground='white',
                               length=200, font=('Arial', 9))
        angle2_scale.pack(fill=tk.X, pady=(0, 10))
        
        print("Adding phase controls...")
        
        # 位相1
        tk.Label(control_frame, text="Phase 1:", bg='white', fg='black', 
                font=('Arial', 10)).pack(anchor=tk.W, pady=(5, 0))
        self.phase1_var = tk.DoubleVar(value=self.phase1)
        phase1_scale = tk.Scale(control_frame, from_=0, to=2*np.pi, variable=self.phase1_var, 
                               orient=tk.HORIZONTAL, command=self.update_pattern,
                               bg='white', fg='black', highlightbackground='white',
                               length=200, font=('Arial', 9))
        phase1_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 位相2
        tk.Label(control_frame, text="Phase 2:", bg='white', fg='black', 
                font=('Arial', 10)).pack(anchor=tk.W, pady=(5, 0))
        self.phase2_var = tk.DoubleVar(value=self.phase2)
        phase2_scale = tk.Scale(control_frame, from_=0, to=2*np.pi, variable=self.phase2_var, 
                               orient=tk.HORIZONTAL, command=self.update_pattern,
                               bg='white', fg='black', highlightbackground='white',
                               length=200, font=('Arial', 9))
        phase2_scale.pack(fill=tk.X, pady=(0, 10))
        
        print("Adding buttons...")
        
        # ボタン
        button_frame = tk.Frame(control_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=15)
        
        self.animate_button = tk.Button(button_frame, text="Start Animation", command=self.toggle_animation,
                                       bg='lightblue', fg='black', relief=tk.RAISED,
                                       font=('Arial', 10, 'bold'), width=12)
        self.animate_button.pack(side=tk.LEFT, padx=(0, 5))
        
        reset_button = tk.Button(button_frame, text="Reset", command=self.reset,
                                bg='lightgreen', fg='black', relief=tk.RAISED,
                                font=('Arial', 10, 'bold'), width=8)
        reset_button.pack(side=tk.LEFT)
        
        print("Adding info label...")
        
        # 情報表示
        self.info_label = tk.Label(control_frame, text="", font=("Arial", 9), 
                                  bg='white', fg='black', justify=tk.LEFT)
        self.info_label.pack(pady=10)
        
        print("Creating display area...")
        
        # 右側の表示エリア
        display_frame = tk.LabelFrame(main_frame, text="Moire Pattern", bg='white', fg='black',
                                     font=('Arial', 12, 'bold'))
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # キャンバス
        self.canvas = tk.Canvas(display_frame, width=self.width, height=self.height, 
                               bg='white', highlightbackground='black')
        self.canvas.pack(expand=True, padx=10, pady=10)
        
        print("Final UI setup complete!")
    
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
            
            self.update_info()
            
        except Exception as e:
            print(f"Error creating pattern: {e}")
    
    def update_pattern(self, event=None):
        self.create_pattern()
    
    def update_info(self):
        info_text = f"Freq1: {self.freq1_var.get():.1f}\n"
        info_text += f"Freq2: {self.freq2_var.get():.1f}\n"
        info_text += f"Angle1: {self.angle1_var.get():.1f}°\n"
        info_text += f"Angle2: {self.angle2_var.get():.1f}°\n"
        info_text += f"Phase1: {self.phase1_var.get():.2f}\n"
        info_text += f"Phase2: {self.phase2_var.get():.2f}"
        self.info_label.config(text=info_text)
    
    def reset(self):
        self.freq1_var.set(8.0)
        self.freq2_var.set(9.0)
        self.angle1_var.set(0.0)
        self.angle2_var.set(45.0)
        self.phase1_var.set(0.0)
        self.phase2_var.set(0.0)
        self.create_pattern()
    
    def animate(self):
        if self.animation_running:
            # 位相を更新
            self.phase1_var.set((self.phase1_var.get() + 0.1) % (2 * np.pi))
            self.phase2_var.set((self.phase2_var.get() + 0.08) % (2 * np.pi))
            self.create_pattern()
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
    app = FinalMoireApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 