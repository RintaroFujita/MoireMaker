import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
from matplotlib.animation import FuncAnimation

class MoireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Moire Generator")
        self.root.geometry("1200x800")
        
        # アニメーション用の変数
        self.animation = None
        self.animation_running = False
        self.time = 0
        
        # モアレパラメータ
        self.freq1 = 10.0  # 第1パターンの周波数
        self.freq2 = 11.0  # 第2パターンの周波数
        self.angle1 = 0.0  # 第1パターンの角度
        self.angle2 = 0.0  # 第2パターンの角度
        self.phase1 = 0.0  # 第1パターンの位相
        self.phase2 = 0.0  # 第2パターンの位相
        self.animation_speed = 0.1  # アニメーション速度
        
        self.setup_ui()
        self.create_moire_pattern()
    
    def setup_ui(self):
        # メインフレーム
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左側のコントロールパネル
        control_frame = ttk.LabelFrame(main_frame, text="コントロール", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 周波数制御
        ttk.Label(control_frame, text="第1パターン周波数:").pack(anchor=tk.W)
        self.freq1_var = tk.DoubleVar(value=self.freq1)
        freq1_scale = ttk.Scale(control_frame, from_=1, to=50, variable=self.freq1_var, 
                               orient=tk.HORIZONTAL, command=self.update_pattern)
        freq1_scale.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="第2パターン周波数:").pack(anchor=tk.W)
        self.freq2_var = tk.DoubleVar(value=self.freq2)
        freq2_scale = ttk.Scale(control_frame, from_=1, to=50, variable=self.freq2_var, 
                               orient=tk.HORIZONTAL, command=self.update_pattern)
        freq2_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 角度制御
        ttk.Label(control_frame, text="第1パターン角度 (度):").pack(anchor=tk.W)
        self.angle1_var = tk.DoubleVar(value=self.angle1)
        angle1_scale = ttk.Scale(control_frame, from_=0, to=180, variable=self.angle1_var, 
                                orient=tk.HORIZONTAL, command=self.update_pattern)
        angle1_scale.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="第2パターン角度 (度):").pack(anchor=tk.W)
        self.angle2_var = tk.DoubleVar(value=self.angle2)
        angle2_scale = ttk.Scale(control_frame, from_=0, to=180, variable=self.angle2_var, 
                                orient=tk.HORIZONTAL, command=self.update_pattern)
        angle2_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 位相制御
        ttk.Label(control_frame, text="第1パターン位相:").pack(anchor=tk.W)
        self.phase1_var = tk.DoubleVar(value=self.phase1)
        phase1_scale = ttk.Scale(control_frame, from_=0, to=2*np.pi, variable=self.phase1_var, 
                                orient=tk.HORIZONTAL, command=self.update_pattern)
        phase1_scale.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="第2パターン位相:").pack(anchor=tk.W)
        self.phase2_var = tk.DoubleVar(value=self.phase2)
        phase2_scale = ttk.Scale(control_frame, from_=0, to=2*np.pi, variable=self.phase2_var, 
                                orient=tk.HORIZONTAL, command=self.update_pattern)
        phase2_scale.pack(fill=tk.X, pady=(0, 10))
        
        # アニメーション速度制御
        ttk.Label(control_frame, text="アニメーション速度:").pack(anchor=tk.W)
        self.speed_var = tk.DoubleVar(value=self.animation_speed)
        speed_scale = ttk.Scale(control_frame, from_=0, to=1, variable=self.speed_var, 
                               orient=tk.HORIZONTAL, command=self.update_speed)
        speed_scale.pack(fill=tk.X, pady=(0, 10))
        
        # アニメーション制御ボタン
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.play_button = ttk.Button(button_frame, text="開始", command=self.toggle_animation)
        self.play_button.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="リセット", command=self.reset_parameters).pack(side=tk.LEFT)
        
        # 右側の表示エリア
        display_frame = ttk.LabelFrame(main_frame, text="モアレパターン", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # パラメータ表示ラベル
        self.info_label = ttk.Label(control_frame, text="", font=("Arial", 9))
        self.info_label.pack(pady=10)
    
    def create_moire_pattern(self):
        # グリッド作成
        x = np.linspace(-5, 5, 200)
        y = np.linspace(-5, 5, 200)
        X, Y = np.meshgrid(x, y)
        
        # 第1パターン（正弦波）
        angle1_rad = np.radians(self.angle1_var.get())
        rotated_x1 = X * np.cos(angle1_rad) + Y * np.sin(angle1_rad)
        pattern1 = np.sin(2 * np.pi * self.freq1_var.get() * rotated_x1 + self.phase1_var.get())
        
        # 第2パターン（正弦波）
        angle2_rad = np.radians(self.angle2_var.get())
        rotated_x2 = X * np.cos(angle2_rad) + Y * np.sin(angle2_rad)
        pattern2 = np.sin(2 * np.pi * self.freq2_var.get() * rotated_x2 + self.phase2_var.get())
        
        # モアレパターン（積）
        moire_pattern = pattern1 * pattern2
        
        # プロット
        self.ax.clear()
        im = self.ax.imshow(moire_pattern, cmap='gray', extent=[-5, 5, -5, 5], 
                           aspect='equal', vmin=-1, vmax=1)
        self.ax.set_title('Dynamic Moire Pattern')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        
        # カラーバー（安全な方法）
        try:
            if hasattr(self, 'cbar') and self.cbar is not None:
                self.cbar.remove()
        except:
            pass
        
        try:
            self.cbar = self.fig.colorbar(im, ax=self.ax)
        except:
            pass
        
        self.canvas.draw()
        
        # 情報更新
        self.update_info()
    
    def update_pattern(self, event=None):
        self.create_moire_pattern()
    
    def update_speed(self, event=None):
        self.animation_speed = self.speed_var.get()
    
    def update_info(self):
        info_text = f"周波数1: {self.freq1_var.get():.1f}\n"
        info_text += f"周波数2: {self.freq2_var.get():.1f}\n"
        info_text += f"角度1: {self.angle1_var.get():.1f}°\n"
        info_text += f"角度2: {self.angle2_var.get():.1f}°\n"
        info_text += f"位相1: {self.phase1_var.get():.2f}\n"
        info_text += f"位相2: {self.phase2_var.get():.2f}\n"
        info_text += f"速度: {self.animation_speed:.2f}"
        self.info_label.config(text=info_text)
    
    def animate(self, frame):
        if hasattr(self, 'animation_running') and self.animation_running:
            # 位相を時間とともに更新
            self.phase1_var.set((self.phase1_var.get() + self.animation_speed) % (2 * np.pi))
            self.phase2_var.set((self.phase2_var.get() + self.animation_speed * 0.7) % (2 * np.pi))
            self.create_moire_pattern()
        return []
    
    def start_animation(self):
        self.animation_running = True
        self.animation = FuncAnimation(self.fig, self.animate, interval=50, blit=False, cache_frame_data=False)
        self.play_button.config(text="停止")
    
    def stop_animation(self):
        self.animation_running = False
        if self.animation:
            self.animation.event_source.stop()
        self.play_button.config(text="開始")
    
    def toggle_animation(self):
        if hasattr(self, 'animation_running') and self.animation_running:
            self.stop_animation()
        else:
            self.start_animation()
    
    def reset_parameters(self):
        self.freq1_var.set(10.0)
        self.freq2_var.set(11.0)
        self.angle1_var.set(0.0)
        self.angle2_var.set(0.0)
        self.phase1_var.set(0.0)
        self.phase2_var.set(0.0)
        self.speed_var.set(0.1)
        self.create_moire_pattern()

def main():
    root = tk.Tk()
    app = MoireApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 