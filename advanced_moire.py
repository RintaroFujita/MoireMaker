import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.animation import FuncAnimation

class AdvancedMoireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Moire Generator")
        self.root.geometry("1400x900")
        
        # アニメーション用の変数
        self.animation = None
        self.animation_running = False
        
        # モアレパラメータ
        self.pattern_type = "linear"  # linear, circular, radial
        self.freq1 = 8.0
        self.freq2 = 9.0
        self.angle1 = 0.0
        self.angle2 = 45.0
        self.phase1 = 0.0
        self.phase2 = 0.0
        self.animation_speed = 0.05
        self.center_x = 0.0
        self.center_y = 0.0
        self.radius = 3.0
        
        self.setup_ui()
        self.create_moire_pattern()
    
    def setup_ui(self):
        # メインフレーム
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左側のコントロールパネル
        control_frame = ttk.LabelFrame(main_frame, text="コントロール", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # パターンタイプ選択
        ttk.Label(control_frame, text="パターンタイプ:").pack(anchor=tk.W)
        self.pattern_var = tk.StringVar(value=self.pattern_type)
        pattern_combo = ttk.Combobox(control_frame, textvariable=self.pattern_var, 
                                    values=["linear", "circular", "radial", "spiral"])
        pattern_combo.pack(fill=tk.X, pady=(0, 10))
        pattern_combo.bind('<<ComboboxSelected>>', self.update_pattern)
        
        # 周波数制御
        ttk.Label(control_frame, text="第1パターン周波数:").pack(anchor=tk.W)
        self.freq1_var = tk.DoubleVar(value=self.freq1)
        freq1_scale = ttk.Scale(control_frame, from_=1, to=30, variable=self.freq1_var, 
                               orient=tk.HORIZONTAL, command=self.update_pattern)
        freq1_scale.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="第2パターン周波数:").pack(anchor=tk.W)
        self.freq2_var = tk.DoubleVar(value=self.freq2)
        freq2_scale = ttk.Scale(control_frame, from_=1, to=30, variable=self.freq2_var, 
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
        
        # 中心位置制御
        ttk.Label(control_frame, text="中心X位置:").pack(anchor=tk.W)
        self.center_x_var = tk.DoubleVar(value=self.center_x)
        center_x_scale = ttk.Scale(control_frame, from_=-3, to=3, variable=self.center_x_var, 
                                  orient=tk.HORIZONTAL, command=self.update_pattern)
        center_x_scale.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="中心Y位置:").pack(anchor=tk.W)
        self.center_y_var = tk.DoubleVar(value=self.center_y)
        center_y_scale = ttk.Scale(control_frame, from_=-3, to=3, variable=self.center_y_var, 
                                  orient=tk.HORIZONTAL, command=self.update_pattern)
        center_y_scale.pack(fill=tk.X, pady=(0, 10))
        
        # 半径制御
        ttk.Label(control_frame, text="半径:").pack(anchor=tk.W)
        self.radius_var = tk.DoubleVar(value=self.radius)
        radius_scale = ttk.Scale(control_frame, from_=1, to=5, variable=self.radius_var, 
                                orient=tk.HORIZONTAL, command=self.update_pattern)
        radius_scale.pack(fill=tk.X, pady=(0, 10))
        
        # アニメーション速度制御
        ttk.Label(control_frame, text="アニメーション速度:").pack(anchor=tk.W)
        self.speed_var = tk.DoubleVar(value=self.animation_speed)
        speed_scale = ttk.Scale(control_frame, from_=0, to=0.2, variable=self.speed_var, 
                               orient=tk.HORIZONTAL, command=self.update_speed)
        speed_scale.pack(fill=tk.X, pady=(0, 10))
        
        # アニメーション制御ボタン
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.play_button = ttk.Button(button_frame, text="開始", command=self.toggle_animation)
        self.play_button.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="リセット", command=self.reset_parameters).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="プリセット1", command=self.preset1).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="プリセット2", command=self.preset2).pack(side=tk.LEFT)
        
        # 右側の表示エリア
        display_frame = ttk.LabelFrame(main_frame, text="モアレパターン", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # パラメータ表示ラベル
        self.info_label = ttk.Label(control_frame, text="", font=("Arial", 8))
        self.info_label.pack(pady=10)
    
    def create_linear_pattern(self, X, Y):
        # 線形パターン
        angle1_rad = np.radians(self.angle1_var.get())
        angle2_rad = np.radians(self.angle2_var.get())
        
        rotated_x1 = X * np.cos(angle1_rad) + Y * np.sin(angle1_rad)
        rotated_x2 = X * np.cos(angle2_rad) + Y * np.sin(angle2_rad)
        
        pattern1 = np.sin(2 * np.pi * self.freq1_var.get() * rotated_x1 + self.phase1_var.get())
        pattern2 = np.sin(2 * np.pi * self.freq2_var.get() * rotated_x2 + self.phase2_var.get())
        
        return pattern1, pattern2
    
    def create_circular_pattern(self, X, Y):
        # 円形パターン
        center_x = self.center_x_var.get()
        center_y = self.center_y_var.get()
        
        # 中心からの距離
        r1 = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        r2 = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        
        pattern1 = np.sin(2 * np.pi * self.freq1_var.get() * r1 + self.phase1_var.get())
        pattern2 = np.sin(2 * np.pi * self.freq2_var.get() * r2 + self.phase2_var.get())
        
        return pattern1, pattern2
    
    def create_radial_pattern(self, X, Y):
        # ラジアルパターン
        center_x = self.center_x_var.get()
        center_y = self.center_y_var.get()
        
        # 角度
        theta1 = np.arctan2(Y - center_y, X - center_x) + np.radians(self.angle1_var.get())
        theta2 = np.arctan2(Y - center_y, X - center_x) + np.radians(self.angle2_var.get())
        
        pattern1 = np.sin(2 * np.pi * self.freq1_var.get() * theta1 + self.phase1_var.get())
        pattern2 = np.sin(2 * np.pi * self.freq2_var.get() * theta2 + self.phase2_var.get())
        
        return pattern1, pattern2
    
    def create_spiral_pattern(self, X, Y):
        # スパイラルパターン
        center_x = self.center_x_var.get()
        center_y = self.center_y_var.get()
        radius = self.radius_var.get()
        
        # 中心からの距離と角度
        r = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        theta = np.arctan2(Y - center_y, X - center_x)
        
        # スパイラルパラメータ
        spiral1 = r + self.freq1_var.get() * theta + self.phase1_var.get()
        spiral2 = r + self.freq2_var.get() * theta + self.phase2_var.get()
        
        pattern1 = np.sin(2 * np.pi * spiral1)
        pattern2 = np.sin(2 * np.pi * spiral2)
        
        return pattern1, pattern2
    
    def create_moire_pattern(self):
        # グリッド作成
        x = np.linspace(-5, 5, 300)
        y = np.linspace(-5, 5, 300)
        X, Y = np.meshgrid(x, y)
        
        # パターンタイプに応じてパターン生成
        pattern_type = self.pattern_var.get()
        
        if pattern_type == "linear":
            pattern1, pattern2 = self.create_linear_pattern(X, Y)
        elif pattern_type == "circular":
            pattern1, pattern2 = self.create_circular_pattern(X, Y)
        elif pattern_type == "radial":
            pattern1, pattern2 = self.create_radial_pattern(X, Y)
        elif pattern_type == "spiral":
            pattern1, pattern2 = self.create_spiral_pattern(X, Y)
        else:
            pattern1, pattern2 = self.create_linear_pattern(X, Y)
        
        # モアレパターン（積）
        moire_pattern = pattern1 * pattern2
        
        # プロット
        self.ax.clear()
        im = self.ax.imshow(moire_pattern, cmap='viridis', extent=[-5, 5, -5, 5], 
                           aspect='equal', vmin=-1, vmax=1)
        self.ax.set_title(f'Dynamic Moire Pattern - {pattern_type}')
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
        self.update_info()
    
    def update_pattern(self, event=None):
        self.create_moire_pattern()
    
    def update_speed(self, event=None):
        self.animation_speed = self.speed_var.get()
    
    def update_info(self):
        info_text = f"タイプ: {self.pattern_var.get()}\n"
        info_text += f"周波数1: {self.freq1_var.get():.1f}\n"
        info_text += f"周波数2: {self.freq2_var.get():.1f}\n"
        info_text += f"角度1: {self.angle1_var.get():.1f}°\n"
        info_text += f"角度2: {self.angle2_var.get():.1f}°\n"
        info_text += f"位相1: {self.phase1_var.get():.2f}\n"
        info_text += f"位相2: {self.phase2_var.get():.2f}\n"
        info_text += f"中心X: {self.center_x_var.get():.1f}\n"
        info_text += f"中心Y: {self.center_y_var.get():.1f}\n"
        info_text += f"半径: {self.radius_var.get():.1f}\n"
        info_text += f"速度: {self.animation_speed:.3f}"
        self.info_label.config(text=info_text)
    
    def animate(self, frame):
        if self.animation_running:
            # 位相を時間とともに更新
            self.phase1_var.set((self.phase1_var.get() + self.animation_speed) % (2 * np.pi))
            self.phase2_var.set((self.phase2_var.get() + self.animation_speed * 0.8) % (2 * np.pi))
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
        if self.animation_running:
            self.stop_animation()
        else:
            self.start_animation()
    
    def reset_parameters(self):
        self.pattern_var.set("linear")
        self.freq1_var.set(8.0)
        self.freq2_var.set(9.0)
        self.angle1_var.set(0.0)
        self.angle2_var.set(45.0)
        self.phase1_var.set(0.0)
        self.phase2_var.set(0.0)
        self.center_x_var.set(0.0)
        self.center_y_var.set(0.0)
        self.radius_var.set(3.0)
        self.speed_var.set(0.05)
        self.create_moire_pattern()
    
    def preset1(self):
        # 円形モアレのプリセット
        self.pattern_var.set("circular")
        self.freq1_var.set(5.0)
        self.freq2_var.set(6.0)
        self.angle1_var.set(0.0)
        self.angle2_var.set(0.0)
        self.phase1_var.set(0.0)
        self.phase2_var.set(0.0)
        self.center_x_var.set(0.0)
        self.center_y_var.set(0.0)
        self.radius_var.set(3.0)
        self.speed_var.set(0.03)
        self.create_moire_pattern()
    
    def preset2(self):
        # スパイラルモアレのプリセット
        self.pattern_var.set("spiral")
        self.freq1_var.set(2.0)
        self.freq2_var.set(2.5)
        self.angle1_var.set(0.0)
        self.angle2_var.set(0.0)
        self.phase1_var.set(0.0)
        self.phase2_var.set(0.0)
        self.center_x_var.set(0.0)
        self.center_y_var.set(0.0)
        self.radius_var.set(2.0)
        self.speed_var.set(0.02)
        self.create_moire_pattern()

def main():
    root = tk.Tk()
    app = AdvancedMoireApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 