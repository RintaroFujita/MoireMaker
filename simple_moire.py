#!/usr/bin/env python3
"""
Simple Moire Pattern Generator
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class SimpleMoireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Moire Generator")
        self.root.geometry("1000x700")
        
        # パラメータ
        self.freq1 = 8.0
        self.freq2 = 9.0
        self.angle1 = 0.0
        self.angle2 = 45.0
        self.phase1 = 0.0
        self.phase2 = 0.0
        
        self.setup_ui()
        self.create_pattern()
    
    def setup_ui(self):
        # メインフレーム
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左側のコントロール
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 周波数1
        ttk.Label(control_frame, text="Frequency 1:").pack(anchor=tk.W)
        self.freq1_var = tk.DoubleVar(value=self.freq1)
        freq1_scale = ttk.Scale(control_frame, from_=1, to=20, variable=self.freq1_var, 
                               orient=tk.HORIZONTAL, command=self.update_pattern)
        freq1_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 周波数2
        ttk.Label(control_frame, text="Frequency 2:").pack(anchor=tk.W)
        self.freq2_var = tk.DoubleVar(value=self.freq2)
        freq2_scale = ttk.Scale(control_frame, from_=1, to=20, variable=self.freq2_var, 
                               orient=tk.HORIZONTAL, command=self.update_pattern)
        freq2_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 角度1
        ttk.Label(control_frame, text="Angle 1 (degrees):").pack(anchor=tk.W)
        self.angle1_var = tk.DoubleVar(value=self.angle1)
        angle1_scale = ttk.Scale(control_frame, from_=0, to=180, variable=self.angle1_var, 
                                orient=tk.HORIZONTAL, command=self.update_pattern)
        angle1_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 角度2
        ttk.Label(control_frame, text="Angle 2 (degrees):").pack(anchor=tk.W)
        self.angle2_var = tk.DoubleVar(value=self.angle2)
        angle2_scale = ttk.Scale(control_frame, from_=0, to=180, variable=self.angle2_var, 
                                orient=tk.HORIZONTAL, command=self.update_pattern)
        angle2_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 位相1
        ttk.Label(control_frame, text="Phase 1:").pack(anchor=tk.W)
        self.phase1_var = tk.DoubleVar(value=self.phase1)
        phase1_scale = ttk.Scale(control_frame, from_=0, to=2*np.pi, variable=self.phase1_var, 
                                orient=tk.HORIZONTAL, command=self.update_pattern)
        phase1_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 位相2
        ttk.Label(control_frame, text="Phase 2:").pack(anchor=tk.W)
        self.phase2_var = tk.DoubleVar(value=self.phase2)
        phase2_scale = ttk.Scale(control_frame, from_=0, to=2*np.pi, variable=self.phase2_var, 
                                orient=tk.HORIZONTAL, command=self.update_pattern)
        phase2_scale.pack(fill=tk.X, pady=(0, 10))
        
        # ボタン
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Animate", command=self.start_animation).pack(side=tk.LEFT)
        
        # 情報表示
        self.info_label = ttk.Label(control_frame, text="", font=("Arial", 9))
        self.info_label.pack(pady=10)
        
        # 右側の表示エリア
        display_frame = ttk.LabelFrame(main_frame, text="Moire Pattern", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # アニメーション用変数
        self.animation_running = False
        self.animation_id = None
    
    def create_pattern(self):
        # グリッド作成
        x = np.linspace(-5, 5, 200)
        y = np.linspace(-5, 5, 200)
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
        
        # プロット
        self.ax.clear()
        self.ax.imshow(moire_pattern, cmap='gray', extent=[-5, 5, -5, 5], 
                      aspect='equal', vmin=-1, vmax=1)
        self.ax.set_title('Moire Pattern')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        
        self.canvas.draw()
        self.update_info()
    
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
    
    def start_animation(self):
        if not self.animation_running:
            self.animation_running = True
            self.animate()
        else:
            self.animation_running = False
            if self.animation_id:
                self.root.after_cancel(self.animation_id)

def main():
    root = tk.Tk()
    app = SimpleMoireApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 