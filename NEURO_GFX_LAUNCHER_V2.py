#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 NEURO-OS VGA™ | ADVANCED LAUNCHER (V2.1)
-------------------------------------------
✔ Advanced capture engine with GPU support
✔ FPS counter and performance metrics
✔ Graphics API detection
✔ Full input forwarding (mouse + keyboard)
✔ Screenshot system (F3)
✔ Professional overlay system
"""

import sys
import os
import ctypes
from ctypes import wintypes
import subprocess
from datetime import datetime
import numpy as np

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QFrame, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPainter, QColor, QFont

# Import Advanced Capture System
from NeuroGFX.advanced_capture import AdvancedCaptureEngine
from NeuroGFX.neuron_input_mapper import NeuronInputMapper
from NeuroGFX.window_capture import WindowCapture  # Captura directa de ventana

# Crear carpeta de screenshots
SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


class NeuroVGAAdvanced(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎮 NEURO-OS VGA™ | ADVANCED DISPLAY v2.1")
        self.resize(1280, 720)
        self.move(150, 80)
        self.setStyleSheet("background-color: #0a0a0a;")

        self.pid = None
        self.hwnd = None
        self.current_frame = None
        self.show_metrics = True  # Mostrar overlay de métricas
        self.show_options = False  # Mostrar menú de opciones

        # Configuración dinámica
        self.target_fps = 60
        self.fps_presets = [15, 30, 45, 60, 75, 90, 120, 144, 240]
        self.current_fps_index = 3  # 60 FPS por defecto
        
        self.resolution_presets = [
            (640, 480),   # VGA
            (800, 600),   # SVGA
            (1024, 576),  # HD-
            (1280, 720),  # HD
            (1600, 900),  # HD+
            (1920, 1080), # Full HD
        ]
        self.current_res_index = 3  # 1280x720 por defecto

        # Window Capture (captura directa de ventana)
        self.window_capture = WindowCapture()
        
        # Advanced Capture Engine (para métricas)
        self.capture = AdvancedCaptureEngine()
        self.input_mapper = NeuronInputMapper()
        
        # Métricas manuales
        self.frames_captured = 0
        self.frames_dropped = 0
        
        # Mouse grab (captura de cursor para control remoto)
        self.mouse_grabbed = False  # Ctrl+G para activar/desactivar
        self.mouse_pos = (0, 0)  # Posición del cursor para dibujar

        # UI Elements
        self.status = QLabel("🎮 READY - SELECT APPLICATION", self)
        self.status.setStyleSheet(
            "color:#00FFCC; font-size:16px; font-weight:bold; "
            "background:rgba(0,0,0,180); padding:8px; border-radius:4px;"
        )
        self.status.adjustSize()
        self.status.move(10, 10)

        # Metrics Overlay (top-right)
        self.metrics_label = QLabel("", self)
        self.metrics_label.setStyleSheet(
            "color:#00FF00; font-size:12px; font-family:Consolas; "
            "background:rgba(0,0,0,180); padding:8px; border-radius:4px;"
        )
        self.metrics_label.move(self.width() - 250, 10)
        self.metrics_label.resize(240, 120)

        # Timer for rendering loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.core_loop)
        self.timer.start(16)  # 60 FPS target

        # Configurar viewport para capturar input
        self.setMouseTracking(True)  # Capturar movimiento de mouse
        self.setFocusPolicy(Qt.StrongFocus)  # Capturar teclado
        self.setFocus()  # Dar foco al viewport

        self.build_launcher()

    def build_launcher(self):
        """Construye el panel de lanzamiento"""
        self.panel = QFrame(self)
        self.panel.setStyleSheet(
            "background:rgba(20,20,30,220); border:2px solid #00FFCC; border-radius:8px;"
        )
        self.panel.setGeometry(self.width()//2-180, self.height()//2-140, 360, 280)

        layout = QVBoxLayout(self.panel)
        
        # Título del panel
        title = QLabel("🎮 QUICK LAUNCH")
        title.setStyleSheet("color:#00FFCC; font-size:18px; font-weight:bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Aplicaciones predefinidas
        apps = [
            ("📝 NOTEPAD", "notepad.exe"),
            ("🎨 PAINT", "mspaint.exe"),
            ("🔢 CALCULATOR", "calc.exe"),
            ("📊 TASK MANAGER", "taskmgr.exe")
        ]
        
        for name, exe in apps:
            btn = QPushButton(name)
            btn.setStyleSheet(
                "QPushButton { background:#1a1a2e; color:#00FFCC; font-size:14px; "
                "padding:10px; border:1px solid #00FFCC; border-radius:4px; }"
                "QPushButton:hover { background:#00FFCC; color:#000; }"
            )
            btn.clicked.connect(lambda _, p=exe: self.launch(p))
            layout.addWidget(btn)

        # Botón para cargar ejecutable personalizado
        browse = QPushButton("📂 LOAD CUSTOM EXE...")
        browse.setStyleSheet(
            "QPushButton { background:#2a2a3e; color:#FFD700; font-size:14px; "
            "padding:10px; border:1px solid #FFD700; border-radius:4px; }"
            "QPushButton:hover { background:#FFD700; color:#000; }"
        )
        browse.clicked.connect(self.browse)
        layout.addWidget(browse)
        
        # Mostrar el panel
        self.panel.show()

    def browse(self):
        """Abre diálogo para seleccionar ejecutable"""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Executable", "C:/", "Executables (*.exe)"
        )
        if path:
            self.launch(path)

    def launch(self, path):
        """Lanza una aplicación"""
        self.panel.hide()
        self.status.setText(f"🚀 Launching: {os.path.basename(path)}")
        self.status.adjustSize()
        
        try:
            proc = subprocess.Popen(path)
            self.pid = proc.pid
            self.status.setText(f"🔍 PID {self.pid} - Searching window...")
            self.status.adjustSize()
        except Exception as e:
            self.status.setText(f"❌ ERROR: {e}")
            self.status.adjustSize()

    def find_window(self):
        """Busca la ventana del proceso (modo agresivo)"""
        if not self.pid:
            return None

        user32 = ctypes.windll.user32
        found = None

        @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        def enum_cb(hwnd, _):
            nonlocal found
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

            style = user32.GetWindowLongW(hwnd, -16)

            # Aceptamos ventanas con estilo WS_VISIBLE
            if pid.value == self.pid and style & 0x10000000:
                found = hwnd
                return False

            return True

        user32.EnumWindows(enum_cb, 0)
        return found

    def core_loop(self):
        """Loop principal de captura y renderizado"""
        # Buscar ventana si no está capturada
        if not self.hwnd:
            hwnd = self.find_window()
            if hwnd:
                self.hwnd = hwnd
                print(f"✔ Captured HWND: {self.hwnd} (PID: {self.pid})")
                
                # Obtener dimensiones de la ventana capturada
                rect = wintypes.RECT()
                ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(rect))
                game_w = rect.right - rect.left
                game_h = rect.bottom - rect.top
                
                # Configurar window capture (captura directa por HWND)
                self.window_capture.set_target(hwnd)
                
                # Configurar input mapper con dimensiones correctas
                self.input_mapper.set_target(hwnd)
                # Usar HYBRID: funciona mejor que POSTMESSAGE para apps en background
                self.input_mapper.mode = "HYBRID"
                view_w, view_h = self.width(), self.height()
                self.input_mapper.update_scaling(view_w, view_h, game_w, game_h)
                print(f"📐 Input scaling: Viewport {view_w}x{view_h} → Window {game_w}x{game_h}")
                print(f"🎮 Input mode: HYBRID (SendInput para compatibilidad)")
                
                # Configurar capture engine para métricas
                self.capture.set_target_hwnd(hwnd)
                
                self.status.setText("✅ Window Captured - Streaming...")
                self.status.adjustSize()
            return

        # Capturar frame directamente de la ventana (sin coordenadas de pantalla)
        frame = self.window_capture.get_snap()

        if frame is not None:
            self.frames_captured += 1
            
            # Asegurar que el array sea contiguo en memoria
            frame = np.ascontiguousarray(frame)
            
            h_img, w_img, ch = frame.shape
            bytes_per_line = w_img * ch
            
            self.current_frame = QImage(
                frame.data, w_img, h_img, bytes_per_line, QImage.Format_RGBA8888
            ).copy()
        else:
            self.frames_dropped += 1

        # Actualizar overlay de métricas
        if self.show_metrics:
            self.update_metrics_overlay()

        self.update()

    def update_metrics_overlay(self):
        """Actualiza el overlay de métricas"""
        metrics_text = f"""
📊 METRICS
━━━━━━━━━━━━━━━
FPS: {self.target_fps}
Mode: Direct Window
Backend: PrintWindow
━━━━━━━━━━━━━━━
HWND: {self.hwnd}
PID: {self.pid}
━━━━━━━━━━━━━━━
Captured: {self.frames_captured}
Dropped: {self.frames_dropped}
        """.strip()
        
        self.metrics_label.setText(metrics_text)

    def take_screenshot(self):
        """Captura un screenshot del frame actual"""
        if not self.current_frame:
            print("⚠️ No hay frame para capturar")
            return
        
        # Generar nombre con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        
        # Guardar imagen
        if self.current_frame.save(filepath):
            print(f"📸 Screenshot guardado: {filepath}")
            self.status.setText(f"📸 Screenshot saved: {filename}")
            self.status.adjustSize()
            
            # Restaurar status después de 2 segundos
            QTimer.singleShot(2000, lambda: self.status.setText("✅ Window Captured - Streaming..."))
        else:
            print(f"❌ Error guardando screenshot")

    def change_fps(self, fps_value):
        """Cambia el FPS target del sistema"""
        self.target_fps = fps_value
        frame_time = int(1000 / fps_value)
        self.timer.setInterval(frame_time)
        print(f"⚡ FPS cambiado a: {fps_value} ({frame_time}ms por frame)")
        self.status.setText(f"⚡ FPS: {fps_value}")
        self.status.adjustSize()
        QTimer.singleShot(2000, lambda: self.status.setText("✅ Window Captured - Streaming..."))

    def cycle_fps_preset(self, direction=1):
        """Cicla entre los presets de FPS"""
        self.current_fps_index = (self.current_fps_index + direction) % len(self.fps_presets)
        new_fps = self.fps_presets[self.current_fps_index]
        self.change_fps(new_fps)

    def change_resolution(self, width, height):
        """Cambia la resolución del viewport"""
        self.resize(width, height)
        print(f"📐 Resolución cambiada a: {width}x{height}")
        self.status.setText(f"📐 Resolution: {width}x{height}")
        self.status.adjustSize()
        QTimer.singleShot(2000, lambda: self.status.setText("✅ Window Captured - Streaming..."))

    def cycle_resolution(self, direction=1):
        """Cicla entre los presets de resolución"""
        self.current_res_index = (self.current_res_index + direction) % len(self.resolution_presets)
        width, height = self.resolution_presets[self.current_res_index]
        self.change_resolution(width, height)

    def toggle_options_menu(self):
        """Muestra/oculta el menú de opciones"""
        self.show_options = not self.show_options
        print(f"⚙️ Options menu: {'ON' if self.show_options else 'OFF'}")
        self.update()

    def paintEvent(self, e):
        """Renderiza el viewport"""
        p = QPainter(self)
        
        # Fondo
        p.fillRect(self.rect(), QColor(10, 10, 10))

        if self.current_frame:
            # Renderizar frame capturado
            p.drawImage(self.rect(), self.current_frame)
        else:
            # Mensaje de espera
            p.setPen(QColor(0, 255, 200))
            font = QFont("Consolas", 16)
            p.setFont(font)
            p.drawText(self.rect(), Qt.AlignCenter, "⏳ WAITING FOR SIGNAL...")

        # Overlay de opciones
        if self.show_options:
            self.draw_options_overlay(p)
        
        # Dibujar cursor personalizado cuando mouse está grabbed
        if self.mouse_grabbed:
            self.draw_custom_cursor(p)

    def draw_custom_cursor(self, p):
        """Dibuja un cursor personalizado (crosshair) en la posición del mouse"""
        x, y = self.mouse_pos
        
        # Configurar color y grosor
        p.setPen(QColor(0, 255, 200, 200))  # Verde cyan semi-transparente
        p.setBrush(Qt.NoBrush)
        
        # Dibujar crosshair (cruz)
        size = 15
        # Línea horizontal
        p.drawLine(int(x - size), int(y), int(x + size), int(y))
        # Línea vertical
        p.drawLine(int(x), int(y - size), int(x), int(y + size))
        
        # Círculo exterior
        p.drawEllipse(int(x - 8), int(y - 8), 16, 16)
        
        # Punto central
        p.setPen(QColor(255, 255, 255, 255))  # Blanco opaco
        p.drawEllipse(int(x - 2), int(y - 2), 4, 4)

    def draw_options_overlay(self, p):
        """Dibuja el overlay de opciones en el centro de la pantalla"""
        # Fondo semi-transparente
        overlay_rect = self.rect().adjusted(self.width()//4, self.height()//4, 
                                            -self.width()//4, -self.height()//4)
        p.fillRect(overlay_rect, QColor(20, 20, 30, 220))
        
        # Borde
        p.setPen(QColor(0, 255, 200))
        p.drawRect(overlay_rect)
        
        # Título
        font_title = QFont("Consolas", 18, QFont.Bold)
        p.setFont(font_title)
        p.setPen(QColor(0, 255, 200))
        title_rect = overlay_rect.adjusted(0, 10, 0, 0)
        p.drawText(title_rect, Qt.AlignTop | Qt.AlignHCenter, "⚙️ OPCIONES / OPTIONS")
        
        # Contenido
        font_content = QFont("Consolas", 12)
        p.setFont(font_content)
        p.setPen(QColor(255, 255, 255))
        
        current_fps = self.fps_presets[self.current_fps_index]
        current_res = self.resolution_presets[self.current_res_index]
        
        options_text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 FPS CONTROL
  Current: {current_fps} FPS
  Presets: {', '.join(map(str, self.fps_presets))}
  
  [1-9] - Set FPS preset directly
  [↑][↓] - Cycle FPS presets

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📐 RESOLUTION CONTROL
  Current: {current_res[0]}x{current_res[1]}
  Presets: 640x480, 800x600, 1024x576, 
           1280x720, 1600x900, 1920x1080
  
  [+] - Increase resolution
  [-] - Decrease resolution

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⌨️  HOTKEYS
  [F1] - Toggle metrics
  [F2] - Reload launcher
  [F3] - Take screenshot
  [O]  - Toggle this menu
  [ESC] - Exit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Press [O] to close this menu
        """.strip()
        
        text_rect = overlay_rect.adjusted(20, 60, -20, -20)
        p.drawText(text_rect, Qt.AlignLeft | Qt.AlignTop, options_text)

    def toggle_mouse_grab(self):
        """Activa/desactiva la captura del cursor (modo control remoto)"""
        # Solo permitir grab si hay una aplicación capturada
        if not self.hwnd:
            print("⚠️ No hay aplicación capturada. Lanza una app primero.")
            return
        
        self.mouse_grabbed = not self.mouse_grabbed
        
        if self.mouse_grabbed:
            # Ocultar panel de lanzamiento si está visible
            if self.panel.isVisible():
                self.panel.hide()
            
            self.grabMouse()  # Capturar cursor dentro del viewport
            self.setCursor(Qt.BlankCursor)  # Ocultar cursor del sistema
            print("🖱️ Mouse GRABBED - Modo control remoto activo (Ctrl+G para liberar)")
            self.status.setText("🖱️ REMOTE CONTROL MODE - Ctrl+G to release")
        else:
            self.releaseMouse()  # Liberar cursor
            self.unsetCursor()  # Restaurar cursor normal
            print("🖱️ Mouse RELEASED - Modo normal")
            self.status.setText("✅ Window Captured - Streaming...")
        
        self.status.adjustSize()

    def keyPressEvent(self, e):
        """Manejo de teclas"""
        # Ctrl+G: Toggle mouse grab (modo control remoto)
        if e.key() == Qt.Key_G and (e.modifiers() & Qt.ControlModifier):
            self.toggle_mouse_grab()
            return
        
        # F1: Toggle metrics overlay
        if e.key() == Qt.Key_F1:
            self.show_metrics = not self.show_metrics
            self.metrics_label.setVisible(self.show_metrics)
            print(f"📊 Metrics overlay: {'ON' if self.show_metrics else 'OFF'}")
        
        # F2: Reload launcher
        elif e.key() == Qt.Key_F2:
            self.hwnd = None
            self.pid = None
            self.panel.show()
            self.status.setText("🎮 READY - SELECT APPLICATION")
            self.status.adjustSize()
            print("🔄 Launcher reloaded")
        
        # F3: Take screenshot
        elif e.key() == Qt.Key_F3:
            self.take_screenshot()
        
        # O: Toggle options menu
        elif e.key() == Qt.Key_O:
            self.toggle_options_menu()
        
        # Números 1-9: FPS presets directos
        elif Qt.Key_1 <= e.key() <= Qt.Key_9:
            preset_index = e.key() - Qt.Key_1  # 0-8
            if preset_index < len(self.fps_presets):
                self.current_fps_index = preset_index
                new_fps = self.fps_presets[preset_index]
                self.change_fps(new_fps)
        
        # +: Aumentar resolución
        elif e.key() == Qt.Key_Plus or e.key() == Qt.Key_Equal:
            self.cycle_resolution(1)
        
        # -: Disminuir resolución
        elif e.key() == Qt.Key_Minus:
            self.cycle_resolution(-1)
        
        # Flechas arriba/abajo: Ciclar FPS
        elif e.key() == Qt.Key_Up:
            self.cycle_fps_preset(1)
        elif e.key() == Qt.Key_Down:
            self.cycle_fps_preset(-1)
        
        # ESC: Cerrar
        elif e.key() == Qt.Key_Escape:
            print("👋 Closing NEURO-OS VGA™")
            self.close()
        
        # Forward to target (si hay ventana capturada y no es una hotkey del sistema)
        elif self.hwnd and not self.show_options:
            self.input_mapper.forward_key(e.key(), True)

    def keyReleaseEvent(self, e):
        """Manejo de liberación de teclas"""
        if self.hwnd:
            self.input_mapper.forward_key(e.key(), False)

    def mouseMoveEvent(self, e):
        """Manejo de movimiento de mouse"""
        # Guardar posición para dibujar cursor personalizado
        self.mouse_pos = (e.position().x(), e.position().y())
        
        if self.hwnd:
            self.input_mapper.forward_mouse("move", e.position().x(), e.position().y(), e.buttons())
        
        # Redibujar si el mouse está grabbed (para actualizar cursor)
        if self.mouse_grabbed:
            self.update()

    def mousePressEvent(self, e):
        """Manejo de click de mouse"""
        if self.hwnd:
            self.input_mapper.forward_mouse("press", e.position().x(), e.position().y(), e.buttons())

    def mouseReleaseEvent(self, e):
        """Manejo de liberación de mouse"""
        if self.hwnd:
            self.input_mapper.forward_mouse("release", e.position().x(), e.position().y(), e.buttons())


if __name__ == "__main__":
    print("🎮 NEURO-OS VGA™ Advanced Launcher v2.1")
    print("=" * 70)
    print("CONTROLS:")
    print("  F1      - Toggle metrics overlay")
    print("  F2      - Reload launcher")
    print("  F3      - Take screenshot")
    print("  O       - Toggle options menu")
    print("  Ctrl+G  - Toggle mouse grab (REMOTE CONTROL MODE)")
    print("  ESC     - Exit")
    print()
    print("FPS CONTROL:")
    print("  1-9     - Set FPS preset (15, 30, 45, 60, 75, 90, 120, 144, 240)")
    print("  ↑/↓     - Cycle FPS presets")
    print()
    print("RESOLUTION CONTROL:")
    print("  +       - Increase resolution")
    print("  -       - Decrease resolution")
    print("=" * 70)
    print(f"📸 Screenshots will be saved to: {SCREENSHOTS_DIR}/")
    print("=" * 70)
    print()
    print("💡 TIP: Press Ctrl+G to grab mouse for remote control")
    print("=" * 70)
    
    app = QApplication(sys.argv)
    win = NeuroVGAAdvanced()
    win.show()
    sys.exit(app.exec())
