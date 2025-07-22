#!/usr/bin/env python3
"""
PyQt Moire Pattern Generator
"""

import sys
import numpy as np
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QSlider, QPushButton, QFrame,
                           QSizePolicy, QComboBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # バックエンドをAggに設定

# GPUアクセラレーション用のライブラリを試行
try:
    import cupy as cp
    CUPY_AVAILABLE = True
    print("CuPy detected - GPU acceleration enabled")
except ImportError:
    CUPY_AVAILABLE = False
    print("CuPy not available")

try:
    import numba
    from numba import jit, cuda
    NUMBA_AVAILABLE = True
    print("Numba detected - JIT compilation enabled")
except ImportError:
    NUMBA_AVAILABLE = False
    print("Numba not available")

try:
    import pyopencl as cl
    OPENCL_AVAILABLE = True
    print("OpenCL detected - GPU acceleration enabled")
except ImportError:
    OPENCL_AVAILABLE = False
    print("OpenCL not available")

# GPU利用可能かどうかの判定
GPU_AVAILABLE = CUPY_AVAILABLE or NUMBA_AVAILABLE or OPENCL_AVAILABLE

class MoirePatternWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # GPU描画用（UI初期化前に設定）
        print(f"=== GPU Initialization ===")
        print(f"OpenCL: {OPENCL_AVAILABLE}")
        print(f"CuPy: {CUPY_AVAILABLE}")
        print(f"Numba: {NUMBA_AVAILABLE}")
        print(f"GPU_AVAILABLE: {GPU_AVAILABLE}")
        
        # デフォルトでGPUモードを有効にする（利用可能な場合）
        self.use_gpu = GPU_AVAILABLE
        print(f"Initial GPU mode: {self.use_gpu}")
        
        self.gpu_label = None
        
        # FPS計測用
        self.frame_times = []
        self.last_frame_time = time.time()
        
        # アニメーション用タイマー
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate)
        self.animation_running = False
        
        # アニメーション設定（より動的）
        self.phase1_step = 150  # フェーズ1の変化量（さらに大きく）
        self.phase2_step = 120  # フェーズ2の変化量（さらに大きく）
        
        self.setup_ui()
        self.create_pattern()
        
    def setup_ui(self):
        # メインレイアウト
        main_layout = QHBoxLayout()
        
        # 左側のコントロール
        control_widget = QWidget()
        control_layout = QVBoxLayout()
        
        # 周波数1
        control_layout.addWidget(QLabel("Frequency 1:"))
        self.freq1_slider = QSlider(Qt.Horizontal)
        self.freq1_slider.setRange(10, 200)
        self.freq1_slider.setValue(80)
        self.freq1_slider.valueChanged.connect(self.create_pattern)
        control_layout.addWidget(self.freq1_slider)
        
        # 周波数2
        control_layout.addWidget(QLabel("Frequency 2:"))
        self.freq2_slider = QSlider(Qt.Horizontal)
        self.freq2_slider.setRange(10, 200)
        self.freq2_slider.setValue(90)
        self.freq2_slider.valueChanged.connect(self.create_pattern)
        control_layout.addWidget(self.freq2_slider)
        
        # 角度1
        control_layout.addWidget(QLabel("Angle 1 (degrees):"))
        self.angle1_slider = QSlider(Qt.Horizontal)
        self.angle1_slider.setRange(0, 180)
        self.angle1_slider.setValue(0)
        self.angle1_slider.valueChanged.connect(self.create_pattern)
        control_layout.addWidget(self.angle1_slider)
        
        # 角度2
        control_layout.addWidget(QLabel("Angle 2 (degrees):"))
        self.angle2_slider = QSlider(Qt.Horizontal)
        self.angle2_slider.setRange(0, 180)
        self.angle2_slider.setValue(45)
        self.angle2_slider.valueChanged.connect(self.create_pattern)
        control_layout.addWidget(self.angle2_slider)
        
        # 位相1
        control_layout.addWidget(QLabel("Phase 1:"))
        self.phase1_slider = QSlider(Qt.Horizontal)
        self.phase1_slider.setRange(0, 628)  # 0 to 2π * 100
        self.phase1_slider.setValue(0)
        self.phase1_slider.valueChanged.connect(self.create_pattern)
        control_layout.addWidget(self.phase1_slider)
        
        # 位相2
        control_layout.addWidget(QLabel("Phase 2:"))
        self.phase2_slider = QSlider(Qt.Horizontal)
        self.phase2_slider.setRange(0, 628)  # 0 to 2π * 100
        self.phase2_slider.setValue(0)
        self.phase2_slider.valueChanged.connect(self.create_pattern)
        control_layout.addWidget(self.phase2_slider)
        
        # パターンタイプ選択
        control_layout.addWidget(QLabel("Pattern Type:"))
        self.pattern_type_combo = QComboBox()
        self.pattern_type_combo.addItems(["Standard", "Wave", "Tree Rings"])
        self.pattern_type_combo.currentTextChanged.connect(self.on_pattern_type_changed)
        control_layout.addWidget(self.pattern_type_combo)
        
        # 波模様用追加パラメーター
        self.wave_complexity_label = QLabel("Wave Complexity:")
        self.wave_complexity_slider = QSlider(Qt.Horizontal)
        self.wave_complexity_slider.setRange(10, 100)
        self.wave_complexity_slider.setValue(50)
        self.wave_complexity_slider.valueChanged.connect(self.create_pattern)
        
        self.wave_distortion_label = QLabel("Wave Distortion:")
        self.wave_distortion_slider = QSlider(Qt.Horizontal)
        self.wave_distortion_slider.setRange(0, 100)
        self.wave_distortion_slider.setValue(30)
        self.wave_distortion_slider.valueChanged.connect(self.create_pattern)
        
        # 木の年輪用追加パラメーター
        self.tree_rings_distortion_label = QLabel("Rings Distortion:")
        self.tree_rings_distortion_slider = QSlider(Qt.Horizontal)
        self.tree_rings_distortion_slider.setRange(0, 100)
        self.tree_rings_distortion_slider.setValue(20)
        self.tree_rings_distortion_slider.valueChanged.connect(self.create_pattern)
        
        self.tree_rings_complexity_label = QLabel("Rings Complexity:")
        self.tree_rings_complexity_slider = QSlider(Qt.Horizontal)
        self.tree_rings_complexity_slider.setRange(10, 100)
        self.tree_rings_complexity_slider.setValue(40)
        self.tree_rings_complexity_slider.valueChanged.connect(self.create_pattern)
        
        # 初期状態では非表示
        self.wave_complexity_label.setVisible(False)
        self.wave_complexity_slider.setVisible(False)
        self.wave_distortion_label.setVisible(False)
        self.wave_distortion_slider.setVisible(False)
        self.tree_rings_distortion_label.setVisible(False)
        self.tree_rings_distortion_slider.setVisible(False)
        self.tree_rings_complexity_label.setVisible(False)
        self.tree_rings_complexity_slider.setVisible(False)
        
        # 追加パラメーターをレイアウトに追加
        control_layout.addWidget(self.wave_complexity_label)
        control_layout.addWidget(self.wave_complexity_slider)
        control_layout.addWidget(self.wave_distortion_label)
        control_layout.addWidget(self.wave_distortion_slider)
        control_layout.addWidget(self.tree_rings_distortion_label)
        control_layout.addWidget(self.tree_rings_distortion_slider)
        control_layout.addWidget(self.tree_rings_complexity_label)
        control_layout.addWidget(self.tree_rings_complexity_slider)
        
        # ボタン
        button_layout = QHBoxLayout()
        self.animate_button = QPushButton("Start Animation")
        self.animate_button.clicked.connect(self.toggle_animation)
        button_layout.addWidget(self.animate_button)
        
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)
        button_layout.addWidget(reset_button)
        
        control_layout.addLayout(button_layout)
        
        # 情報表示
        self.info_label = QLabel("")
        control_layout.addWidget(self.info_label)
        
        # FPS表示
        self.fps_label = QLabel("FPS: --")
        self.fps_label.setStyleSheet("color: red; font-weight: bold;")
        control_layout.addWidget(self.fps_label)
        
        # GPU状態表示と切り替えボタン
        gpu_layout = QHBoxLayout()
        
        # 利用可能なGPU技術を表示
        if self.use_gpu:
            if OPENCL_AVAILABLE:
                gpu_text = "GPU: OpenCL"
                gpu_color = "green"
            elif CUPY_AVAILABLE:
                gpu_text = "GPU: CuPy"
                gpu_color = "blue"
            elif NUMBA_AVAILABLE:
                gpu_text = "GPU: Numba"
                gpu_color = "purple"
            else:
                gpu_text = "GPU: None"
                gpu_color = "red"
        else:
            gpu_text = "GPU: Disabled"
            gpu_color = "red"
        
        self.gpu_label = QLabel(gpu_text)
        self.gpu_label.setStyleSheet(f"color: {gpu_color}; font-weight: bold;")
        gpu_layout.addWidget(self.gpu_label)
        
        self.gpu_toggle_button = QPushButton("Switch to CPU")
        self.gpu_toggle_button.clicked.connect(self.toggle_gpu_mode)
        gpu_layout.addWidget(self.gpu_toggle_button)
        
        control_layout.addLayout(gpu_layout)
        
        control_layout.addStretch()
        control_widget.setLayout(control_layout)
        control_widget.setFixedWidth(250)
        
        # 右側の表示エリア
        self.display_label = QLabel()
        self.display_label.setMinimumSize(400, 400)
        self.display_label.setFrameStyle(QFrame.Box)
        self.display_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        main_layout.addWidget(control_widget)
        main_layout.addWidget(self.display_label, 1)  # 表示エリアを拡張可能に
        
        self.setLayout(main_layout)
        
        # リサイズイベントを監視
        self.display_label.resizeEvent = self.on_display_resize
        
    def create_pattern(self):
        try:
            # FPS計測開始
            start_time = time.time()
            
            # 解像度を表示サイズに比例させる
            print("Creating moire pattern...")
            # 表示サイズに応じて解像度を比例的に増加
            resolution_x = max(300, min(1200, self.display_label.width() // 2))
            resolution_y = max(300, min(1200, self.display_label.height() // 2))
            
            # GPU描画かCPU描画かを選択
            if self.use_gpu:
                print(f"=== GPU MODE ENABLED ===")
                print(f"OpenCL: {OPENCL_AVAILABLE}, CuPy: {CUPY_AVAILABLE}, Numba: {NUMBA_AVAILABLE}")
                self.create_pattern_gpu(resolution_x, resolution_y)
            else:
                print(f"=== CPU MODE ENABLED ===")
                self.create_pattern_cpu(resolution_x, resolution_y)
            
            # FPS計測終了と更新
            end_time = time.time()
            frame_time = end_time - start_time
            self.update_fps(frame_time)
            
            print("Pattern created and displayed successfully!")
            
        except Exception as e:
            print(f"Error creating pattern: {e}")
            
    def create_pattern_gpu(self, resolution_x, resolution_y):
        """GPUを使用したモアレパターン生成"""
        try:
            # パラメータ取得
            freq1 = self.freq1_slider.value() / 10.0
            freq2 = self.freq2_slider.value() / 10.0
            angle1 = self.angle1_slider.value()
            angle2 = self.angle2_slider.value()
            phase1 = self.phase1_slider.value() / 100.0
            phase2 = self.phase2_slider.value() / 100.0
            
            print(f"GPU Parameters: freq1={freq1:.1f}, freq2={freq2:.1f}, angle1={angle1}°, angle2={angle2}°, phase1={phase1:.2f}, phase2={phase2:.2f}")
            
            # 表示エリアのサイズを取得
            display_width = self.display_label.width()
            display_height = self.display_label.height()
            if display_width <= 0 or display_height <= 0:
                display_width = display_height = 400
            
            print(f"GPU Display size: {display_width}x{display_height}, Resolution: {resolution_x}x{resolution_y}")
            
            # GPU描画用のQImageを作成
            image = QImage(display_width, display_height, QImage.Format_RGB32)
            image.fill(QColor(255, 255, 255))  # 白で初期化
            
            # GPU計算でモアレパターンを生成（優先順位: OpenCL > CuPy > Numba）
            if OPENCL_AVAILABLE:
                moire_pattern = self.calculate_moire_gpu_opencl(resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2)
            elif CUPY_AVAILABLE:
                moire_pattern = self.calculate_moire_gpu_cupy(resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2)
            elif NUMBA_AVAILABLE:
                moire_pattern = self.calculate_moire_gpu_numba(resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2)
            else:
                raise Exception("No GPU acceleration available")
            
            # QImageに描画
            self.draw_pattern_to_image(image, moire_pattern, display_width, display_height)
            
            # QPixmapに変換して表示
            pixmap = QPixmap.fromImage(image)
            self.display_label.setPixmap(pixmap)
            
            # 情報更新
            self.update_info()
            
        except Exception as e:
            print(f"GPU rendering failed, falling back to CPU: {e}")
            self.use_gpu = False
            self.gpu_label.setText("GPU: Disabled (fallback)")
            self.gpu_label.setStyleSheet("color: red; font-weight: bold;")
            self.create_pattern_cpu(resolution_x, resolution_y)
            
    def create_pattern_cpu(self, resolution_x, resolution_y):
        """CPUを使用したモアレパターン生成（従来のmatplotlib方式）"""
        # パラメータ取得
        freq1 = self.freq1_slider.value() / 10.0
        freq2 = self.freq2_slider.value() / 10.0
        angle1 = self.angle1_slider.value()
        angle2 = self.angle2_slider.value()
        phase1 = self.phase1_slider.value() / 100.0
        phase2 = self.phase2_slider.value() / 100.0
        pattern_type = self.pattern_type_combo.currentText()
        
        # 追加パラメーターのログ出力
        if pattern_type == "Wave":
            complexity = self.wave_complexity_slider.value() / 100.0
            distortion = self.wave_distortion_slider.value() / 100.0
            print(f"CPU Parameters: freq1={freq1:.1f}, freq2={freq2:.1f}, angle1={angle1}°, angle2={angle2}°, phase1={phase1:.2f}, phase2={phase2:.2f}, type={pattern_type}, complexity={complexity:.2f}, distortion={distortion:.2f}")
        elif pattern_type == "Tree Rings":
            distortion = self.tree_rings_distortion_slider.value() / 100.0
            complexity = self.tree_rings_complexity_slider.value() / 100.0
            print(f"CPU Parameters: freq1={freq1:.1f}, freq2={freq2:.1f}, angle1={angle1}°, angle2={angle2}°, phase1={phase1:.2f}, phase2={phase2:.2f}, type={pattern_type}, distortion={distortion:.2f}, complexity={complexity:.2f}")
        else:
            print(f"CPU Parameters: freq1={freq1:.1f}, freq2={freq2:.1f}, angle1={angle1}°, angle2={angle2}°, phase1={phase1:.2f}, phase2={phase2:.2f}, type={pattern_type}")
        
        # 表示エリアのサイズを取得
        display_width = self.display_label.width()
        display_height = self.display_label.height()
        if display_width <= 0 or display_height <= 0:
            display_width = display_height = 400  # デフォルトサイズ
        
        # 解像度を表示サイズに比例させる（統一処理）
        display_size = max(display_width, display_height)
        resolution_x = max(300, min(1200, display_width // 2))
        resolution_y = max(300, min(1200, display_height // 2))
        print(f"CPU Display size: {display_width}x{display_height}, Resolution: {resolution_x}x{resolution_y}")
        
        # パターンタイプに応じて計算メソッドを選択
        if pattern_type == "Wave":
            moire_pattern = self.calculate_wave_pattern(resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2)
        elif pattern_type == "Tree Rings":
            moire_pattern = self.calculate_tree_rings_pattern(resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2)
        else:  # Standard
            moire_pattern = self.calculate_moire_cpu_fallback(resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2)
        
        # matplotlibでプロット（横と縦の比率を保持）
        fig_width = max(4, display_width / 100)
        fig_height = max(4, display_height / 100)
        fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)
        im = ax.imshow(moire_pattern, cmap='gray', extent=[-2, 2, -2, 2], 
                      aspect='auto', vmin=-1, vmax=1)
        ax.set_title(f'Moire Pattern - {pattern_type}')
        ax.axis('off')
        
        # 画像をQPixmapに変換
        fig.canvas.draw()
        buf = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        buf = buf.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        
        height, width, channel = buf.shape
        bytes_per_line = 3 * width
        q_image = QImage(buf.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        
        # 表示エリアに合わせてスケール（横と縦を最大限活用）
        scaled_pixmap = pixmap.scaled(self.display_label.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.display_label.setPixmap(scaled_pixmap)
        plt.close(fig)
        
        # 情報更新
        self.update_info()
    
    def on_pattern_type_changed(self):
        """パターンタイプ変更時の処理"""
        pattern_type = self.pattern_type_combo.currentText()
        
        # 波模様パターンの場合
        if pattern_type == "Wave":
            self.wave_complexity_label.setVisible(True)
            self.wave_complexity_slider.setVisible(True)
            self.wave_distortion_label.setVisible(True)
            self.wave_distortion_slider.setVisible(True)
            self.tree_rings_distortion_label.setVisible(False)
            self.tree_rings_distortion_slider.setVisible(False)
            self.tree_rings_complexity_label.setVisible(False)
            self.tree_rings_complexity_slider.setVisible(False)
        # 木の年輪パターンの場合
        elif pattern_type == "Tree Rings":
            self.wave_complexity_label.setVisible(False)
            self.wave_complexity_slider.setVisible(False)
            self.wave_distortion_label.setVisible(False)
            self.wave_distortion_slider.setVisible(False)
            self.tree_rings_distortion_label.setVisible(True)
            self.tree_rings_distortion_slider.setVisible(True)
            self.tree_rings_complexity_label.setVisible(True)
            self.tree_rings_complexity_slider.setVisible(True)
        # 標準パターンの場合
        else:
            self.wave_complexity_label.setVisible(False)
            self.wave_complexity_slider.setVisible(False)
            self.wave_distortion_label.setVisible(False)
            self.wave_distortion_slider.setVisible(False)
            self.tree_rings_distortion_label.setVisible(False)
            self.tree_rings_distortion_slider.setVisible(False)
            self.tree_rings_complexity_label.setVisible(False)
            self.tree_rings_complexity_slider.setVisible(False)
        
        # パターンを再生成
        self.create_pattern()
        
    def calculate_moire_gpu_cupy(self, resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2):
        """CuPyを使用したGPU計算"""
        # グリッド作成
        x = cp.linspace(-2, 2, resolution_x)
        y = cp.linspace(-2, 2, resolution_y)
        X, Y = cp.meshgrid(x, y)
        
        # 第1パターン
        angle1_rad = cp.radians(angle1)
        rotated_x1 = X * cp.cos(angle1_rad) + Y * cp.sin(angle1_rad)
        pattern1 = cp.sin(2 * cp.pi * freq1 * rotated_x1 + phase1)
        
        # 第2パターン
        angle2_rad = cp.radians(angle2)
        rotated_x2 = X * cp.cos(angle2_rad) + Y * cp.sin(angle2_rad)
        pattern2 = cp.sin(2 * cp.pi * freq2 * rotated_x2 + phase2)
        
        # モアレパターン
        moire_pattern = pattern1 * pattern2
        
        # CPUに戻す
        return cp.asnumpy(moire_pattern)
        
    def calculate_moire_gpu_numba(self, resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2):
        """Numbaを使用したGPU計算"""
        @jit(nopython=True, parallel=True)
        def calculate_pattern(x, y, freq, angle, phase):
            result = np.zeros((len(y), len(x)))
            angle_rad = np.radians(angle)
            cos_a = np.cos(angle_rad)
            sin_a = np.sin(angle_rad)
            
            for i in range(len(y)):
                for j in range(len(x)):
                    rotated_x = x[j] * cos_a + y[i] * sin_a
                    result[i, j] = np.sin(2 * np.pi * freq * rotated_x + phase)
            return result
        
        # グリッド作成
        x = np.linspace(-2, 2, resolution_x)
        y = np.linspace(-2, 2, resolution_y)
        
        # パターン計算
        pattern1 = calculate_pattern(x, y, freq1, angle1, phase1)
        pattern2 = calculate_pattern(x, y, freq2, angle2, phase2)
        
        # モアレパターン
        return pattern1 * pattern2
        
    def calculate_moire_gpu_opencl(self, resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2):
        """OpenCLを使用したGPU計算"""
        try:
            # OpenCLコンテキストとキューの初期化
            if not hasattr(self, 'cl_ctx'):
                print("=== OpenCL Initialization ===")
                # プラットフォームとデバイスを自動選択
                platforms = cl.get_platforms()
                print(f"Found {len(platforms)} OpenCL platforms:")
                for i, p in enumerate(platforms):
                    print(f"  [{i}] {p.name}")
                
                if not platforms:
                    raise Exception("No OpenCL platforms found")
                
                # Appleプラットフォームを優先
                platform = None
                for p in platforms:
                    if 'Apple' in p.name:
                        platform = p
                        break
                if not platform:
                    platform = platforms[0]  # 最初のプラットフォームを使用
                
                print(f"Selected platform: {platform.name}")
                
                # GPUデバイスを優先
                devices = platform.get_devices(cl.device_type.GPU)
                if not devices:
                    devices = platform.get_devices(cl.device_type.ALL)
                
                print(f"Found {len(devices)} OpenCL devices:")
                for i, d in enumerate(devices):
                    print(f"  [{i}] {d.name} ({d.type})")
                
                if not devices:
                    raise Exception("No OpenCL devices found")
                
                self.cl_ctx = cl.Context(devices)
                self.cl_queue = cl.CommandQueue(self.cl_ctx)
                print(f"OpenCL context created with {len(devices)} device(s)")
                print("=== OpenCL Ready ===")
                
                # OpenCLカーネルコード
                kernel_code = """
                __kernel void calculate_moire(
                    __global const float* x_coords,
                    __global const float* y_coords,
                    __global float* result,
                    const float freq1, const float freq2,
                    const float angle1, const float angle2,
                    const float phase1, const float phase2,
                    const int width, const int height
                ) {
                    int gid = get_global_id(0);
                    int x = gid % width;
                    int y = gid / width;
                    
                    if (y >= height) return;
                    
                    float x_val = x_coords[x];
                    float y_val = y_coords[y];
                    
                    // 第1パターン
                    float angle1_rad = angle1 * 0.0174533f; // degrees to radians
                    float rotated_x1 = x_val * cos(angle1_rad) + y_val * sin(angle1_rad);
                    float pattern1 = sin(2.0f * 3.14159f * freq1 * rotated_x1 + phase1);
                    
                    // 第2パターン
                    float angle2_rad = angle2 * 0.0174533f; // degrees to radians
                    float rotated_x2 = x_val * cos(angle2_rad) + y_val * sin(angle2_rad);
                    float pattern2 = sin(2.0f * 3.14159f * freq2 * rotated_x2 + phase2);
                    
                    // モアレパターン
                    result[gid] = pattern1 * pattern2;
                }
                """
                
                # カーネルをコンパイル
                self.cl_program = cl.Program(self.cl_ctx, kernel_code).build()
            
            # グリッド作成
            x = np.linspace(-2, 2, resolution_x, dtype=np.float32)
            y = np.linspace(-2, 2, resolution_y, dtype=np.float32)
            
            # GPUバッファを作成
            x_buf = cl.Buffer(self.cl_ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=x)
            y_buf = cl.Buffer(self.cl_ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=y)
            result_buf = cl.Buffer(self.cl_ctx, cl.mem_flags.WRITE_ONLY, size=resolution_x * resolution_y * 4)
            
            # カーネルを実行
            global_size = (resolution_x * resolution_y,)
            print(f"Executing OpenCL kernel with {global_size[0]} work items...")
            
            self.cl_program.calculate_moire(
                self.cl_queue, global_size, None,
                x_buf, y_buf, result_buf,
                np.float32(freq1), np.float32(freq2),
                np.float32(angle1), np.float32(angle2),
                np.float32(phase1), np.float32(phase2),
                np.int32(resolution_x), np.int32(resolution_y)
            )
            
            # 結果を取得
            result = np.empty((resolution_y, resolution_x), dtype=np.float32)
            cl.enqueue_copy(self.cl_queue, result, result_buf)
            
            print(f"OpenCL calculation completed: {result.shape}")
            return result
            
        except Exception as e:
            print(f"OpenCL calculation failed: {e}")
            # フォールバック: CPU計算
            return self.calculate_moire_cpu_fallback(resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2)
    
    def calculate_moire_cpu_fallback(self, resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2):
        """CPUフォールバック計算"""
        # グリッド作成
        x = np.linspace(-2, 2, resolution_x)
        y = np.linspace(-2, 2, resolution_y)
        X, Y = np.meshgrid(x, y)
        
        # 第1パターン
        angle1_rad = np.radians(angle1)
        rotated_x1 = X * np.cos(angle1_rad) + Y * np.sin(angle1_rad)
        pattern1 = np.sin(2 * np.pi * freq1 * rotated_x1 + phase1)
        
        # 第2パターン
        angle2_rad = np.radians(angle2)
        rotated_x2 = X * np.cos(angle2_rad) + Y * np.sin(angle2_rad)
        pattern2 = np.sin(2 * np.pi * freq2 * rotated_x2 + phase2)
        
        # モアレパターン
        return pattern1 * pattern2
    
    def calculate_wave_pattern(self, resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2):
        """波模様パターン生成（拡張版）"""
        # 追加パラメーターを取得
        complexity = self.wave_complexity_slider.value() / 100.0
        distortion = self.wave_distortion_slider.value() / 100.0
        
        # グリッド作成
        x = np.linspace(-3, 3, resolution_x)
        y = np.linspace(-3, 3, resolution_y)
        X, Y = np.meshgrid(x, y)
        
        # 角度をラジアンに変換
        angle1_rad = np.radians(angle1)
        angle2_rad = np.radians(angle2)
        
        # 回転した座標
        X1 = X * np.cos(angle1_rad) + Y * np.sin(angle1_rad)
        Y1 = -X * np.sin(angle1_rad) + Y * np.cos(angle1_rad)
        X2 = X * np.cos(angle2_rad) + Y * np.sin(angle2_rad)
        Y2 = -X * np.sin(angle2_rad) + Y * np.cos(angle2_rad)
        
        # 歪み効果を追加
        distortion_factor = 1.0 + distortion * np.sin(X * Y * 0.5)
        X1 *= distortion_factor
        Y1 *= distortion_factor
        X2 *= distortion_factor
        Y2 *= distortion_factor
        
        # 複雑さに基づいて波の数を調整
        complexity_factor = 1.0 + complexity * 2.0
        
        # 波模様パターン（複雑さと歪みを考慮）
        pattern1 = (np.sin(2 * np.pi * freq1 * X1 + phase1) + 
                   np.sin(2 * np.pi * freq1 * 0.5 * Y1 + phase1 * 0.7) +
                   complexity * np.sin(2 * np.pi * freq1 * complexity_factor * (X1 + Y1) + phase1 * 1.5))
        
        pattern2 = (np.sin(2 * np.pi * freq2 * X2 + phase2) + 
                   np.sin(2 * np.pi * freq2 * 0.7 * Y2 + phase2 * 1.3) +
                   complexity * np.sin(2 * np.pi * freq2 * complexity_factor * (X2 - Y2) + phase2 * 0.8))
        
        # 波模様のモアレパターン
        return pattern1 * pattern2
    
    def calculate_tree_rings_pattern(self, resolution_x, resolution_y, freq1, freq2, angle1, angle2, phase1, phase2):
        """木の年輪パターン生成（拡張版）"""
        # 追加パラメーターを取得
        distortion = self.tree_rings_distortion_slider.value() / 100.0
        complexity = self.tree_rings_complexity_slider.value() / 100.0
        
        # グリッド作成
        x = np.linspace(-2, 2, resolution_x)
        y = np.linspace(-2, 2, resolution_y)
        X, Y = np.meshgrid(x, y)
        
        # 中心からの距離を計算（歪み効果を追加）
        R = np.sqrt(X**2 + Y**2)
        
        # 歪み効果：年輪を楕円形や不規則な形にする
        distortion_factor = 1.0 + distortion * np.sin(X * 2.0) * np.cos(Y * 2.0)
        R_distorted = R * distortion_factor
        
        # 角度をラジアンに変換
        angle1_rad = np.radians(angle1)
        angle2_rad = np.radians(angle2)
        
        # 回転した座標
        X1 = X * np.cos(angle1_rad) + Y * np.sin(angle1_rad)
        Y1 = -X * np.sin(angle1_rad) + Y * np.cos(angle1_rad)
        X2 = X * np.cos(angle2_rad) + Y * np.sin(angle2_rad)
        Y2 = -X * np.sin(angle2_rad) + Y * np.cos(angle2_rad)
        
        # 複雑さに基づいて追加の波を生成
        complexity_factor = 1.0 + complexity * 3.0
        
        # 年輪パターン（歪みと複雑さを考慮）
        pattern1 = (np.sin(2 * np.pi * freq1 * R_distorted + phase1) * 
                   np.sin(2 * np.pi * freq1 * 0.3 * X1 + phase1 * 0.5) +
                   complexity * np.sin(2 * np.pi * freq1 * complexity_factor * R_distorted + phase1 * 1.2))
        
        pattern2 = (np.sin(2 * np.pi * freq2 * R_distorted + phase2) * 
                   np.sin(2 * np.pi * freq2 * 0.4 * Y2 + phase2 * 0.8) +
                   complexity * np.sin(2 * np.pi * freq2 * complexity_factor * R_distorted + phase2 * 0.6))
        
        # 年輪のモアレパターン
        return pattern1 * pattern2
        
    def draw_pattern_to_image(self, image, moire_pattern, display_width, display_height):
        """モアレパターンをQImageに描画（最適化版）"""
        # パターンのサイズ
        pattern_height, pattern_width = moire_pattern.shape
        
        # スケール計算
        scale_x = display_width / pattern_width
        scale_y = display_height / pattern_height
        
        # バイト配列に直接書き込み（高速化）
        bits = image.bits()
        bits.setsize(display_width * display_height * 4)  # 32bit = 4 bytes
        
        # モアレパターンをグレースケールに変換
        gray_pattern = ((moire_pattern + 1) / 2 * 255).astype(np.uint8)
        
        # 各ピクセルを描画（最適化）
        for y in range(pattern_height):
            for x in range(pattern_width):
                # グレースケール値
                gray_value = gray_pattern[y, x]
                
                # 描画位置
                draw_x = int(x * scale_x)
                draw_y = int(y * scale_y)
                draw_width = max(1, int(scale_x))
                draw_height = max(1, int(scale_y))
                
                # ピクセルブロックを描画
                for dy in range(draw_height):
                    for dx in range(draw_width):
                        pixel_x = draw_x + dx
                        pixel_y = draw_y + dy
                        
                        if 0 <= pixel_x < display_width and 0 <= pixel_y < display_height:
                            # 32bit RGBA形式で書き込み
                            offset = (pixel_y * display_width + pixel_x) * 4
                            bits[offset] = gray_value     # Blue
                            bits[offset + 1] = gray_value # Green
                            bits[offset + 2] = gray_value # Red
                            bits[offset + 3] = 255        # Alpha
              
    def toggle_gpu_mode(self):
        """GPU/CPUモードを切り替え"""
        self.use_gpu = not self.use_gpu
        if self.use_gpu:
            # 利用可能なGPU技術を表示
            if OPENCL_AVAILABLE:
                gpu_text = "GPU: OpenCL"
                gpu_color = "green"
            elif CUPY_AVAILABLE:
                gpu_text = "GPU: CuPy"
                gpu_color = "blue"
            elif NUMBA_AVAILABLE:
                gpu_text = "GPU: Numba"
                gpu_color = "purple"
            else:
                gpu_text = "GPU: None"
                gpu_color = "red"
            
            self.gpu_label.setText(gpu_text)
            self.gpu_label.setStyleSheet(f"color: {gpu_color}; font-weight: bold;")
            self.gpu_toggle_button.setText("Switch to CPU")
        else:
            self.gpu_label.setText("GPU: Disabled")
            self.gpu_label.setStyleSheet("color: red; font-weight: bold;")
            self.gpu_toggle_button.setText("Switch to GPU")
        
        # パターンを再生成
        self.create_pattern()
            
    def update_fps(self, frame_time):
        """FPSを計算して表示を更新"""
        # フレーム時間を記録（最大30フレーム分）
        self.frame_times.append(frame_time)
        if len(self.frame_times) > 30:
            self.frame_times.pop(0)
        
        # 平均FPSを計算
        if len(self.frame_times) > 0:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
            self.fps_label.setText(f"FPS: {fps:.1f}")
            
            # 色を変更（FPSに応じて）
            if fps >= 50:
                color = "green"
            elif fps >= 30:
                color = "orange"
            else:
                color = "red"
            self.fps_label.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def update_info(self):
        info_text = f"Freq1: {self.freq1_slider.value() / 10.0:.1f}\n"
        info_text += f"Freq2: {self.freq2_slider.value() / 10.0:.1f}\n"
        info_text += f"Angle1: {self.angle1_slider.value():.1f}°\n"
        info_text += f"Angle2: {self.angle2_slider.value():.1f}°\n"
        info_text += f"Phase1: {self.phase1_slider.value() / 100.0:.2f}\n"
        info_text += f"Phase2: {self.phase2_slider.value() / 100.0:.2f}"
        self.info_label.setText(info_text)
    
    def reset(self):
        print("Resetting parameters to default values...")
        self.freq1_slider.setValue(80)
        self.freq2_slider.setValue(90)
        self.angle1_slider.setValue(0)
        self.angle2_slider.setValue(45)
        self.phase1_slider.setValue(0)
        self.phase2_slider.setValue(0)
        self.create_pattern()
        print("Reset completed!")
    
    def animate(self):
        if self.animation_running:
            try:
                # 位相を更新（設定可能な変化量）
                phase1 = (self.phase1_slider.value() + self.phase1_step) % 628
                phase2 = (self.phase2_slider.value() + self.phase2_step) % 628
                self.phase1_slider.setValue(phase1)
                self.phase2_slider.setValue(phase2)
            except Exception as e:
                print(f"Animation error: {e}")
                self.animation_running = False
                self.animate_button.setText("Start Animation")
                self.animation_timer.stop()
    
    def toggle_animation(self):
        if not self.animation_running:
            print("Starting animation...")
            self.animation_running = True
            self.animate_button.setText("Stop Animation")
            # 60fpsでスムーズなアニメーション
            self.animation_timer.start(17)  # 約60fps (1000ms/60 ≈ 16.7ms)
        else:
            print("Stopping animation...")
            self.animation_running = False
            self.animate_button.setText("Start Animation")
            self.animation_timer.stop()
    
    def on_display_resize(self, event):
        """表示エリアがリサイズされた時の処理"""
        print(f"Display resized to: {self.display_label.width()}x{self.display_label.height()}")
        # パターンを再生成
        self.create_pattern()
        # 元のリサイズイベントを呼び出し
        QLabel.resizeEvent(self.display_label, event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Moire Pattern Generator")
        self.setGeometry(100, 100, 900, 700)
        
        self.moire_widget = MoirePatternWidget()
        self.setCentralWidget(self.moire_widget)

def main():
    print("=== Application Starting ===")
    print(f"OpenCL: {OPENCL_AVAILABLE}")
    print(f"CuPy: {CUPY_AVAILABLE}")
    print(f"Numba: {NUMBA_AVAILABLE}")
    print(f"GPU_AVAILABLE: {GPU_AVAILABLE}")
    
    app = QApplication(sys.argv)
    
    # デバッグモードをオン
    print("=== PyQt Moire Pattern Generator ===")
    print("Debug mode: ON")
    print("Starting application...")
    
    window = MainWindow()
    window.show()
    
    print("Application window displayed successfully!")
    print("Ready for user interaction...")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 