
# 🎮 NEURON INPUTMAPPER™ V2 (HYBRID ENGINE)
# -----------------------------------------
# Soporte Híbrido: PostMessage (Segundo Plano) + SendInput (Inyección Directa)
# Compatible con DX9/10/11/12, Vulkan y OpenGL.

import ctypes
from ctypes import wintypes
from PySide6.QtCore import Qt
import time

# --- ESTRUCTURAS WIN32 PARA SENDINPUT ---
PUL = ctypes.POINTER(ctypes.c_ulong)

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_ulonglong)
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    ]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_ulonglong)
    ]

class INPUT_I(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("mi", MOUSEINPUT),
        ("hi", HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("ii", INPUT_I)
    ]

class NeuronInputMapper:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        
        # Constantes Win32 - PostMessage
        self.WM_MOUSEMOVE    = 0x0200
        self.WM_LBUTTONDOWN  = 0x0201
        self.WM_LBUTTONUP    = 0x0202
        self.WM_LBUTTONDBLCLK= 0x0203
        self.WM_RBUTTONDOWN  = 0x0204
        self.WM_RBUTTONUP    = 0x0205
        self.WM_RBUTTONDBLCLK= 0x0206
        self.WM_MBUTTONDOWN  = 0x0207
        self.WM_MBUTTONUP    = 0x0208
        self.WM_MOUSEWHEEL   = 0x020A
        
        self.WM_KEYDOWN     = 0x0100
        self.WM_KEYUP       = 0x0101
        self.WM_SYSKEYDOWN  = 0x0104 # Alt key
        self.WM_SYSKEYUP    = 0x0105
        
        self.MK_LBUTTON     = 0x0001
        self.MK_RBUTTON     = 0x0002
        self.MK_SHIFT       = 0x0004
        self.MK_CONTROL     = 0x0008
        self.MK_MBUTTON     = 0x0010
        
        # Constantes SendInput
        self.INPUT_MOUSE    = 0
        self.INPUT_KEYBOARD = 1
        
        self.MOUSEEVENTF_MOVE       = 0x0001
        self.MOUSEEVENTF_LEFTDOWN   = 0x0002
        self.MOUSEEVENTF_LEFTUP     = 0x0004
        self.MOUSEEVENTF_RIGHTDOWN  = 0x0008
        self.MOUSEEVENTF_RIGHTUP    = 0x0010
        self.MOUSEEVENTF_MIDDLEDOWN = 0x0020
        self.MOUSEEVENTF_MIDDLEUP   = 0x0040
        self.MOUSEEVENTF_WHEEL      = 0x0800
        self.MOUSEEVENTF_ABSOLUTE   = 0x8000
        
        self.KEYEVENTF_EXTENDEDKEY = 0x0001
        self.KEYEVENTF_KEYUP       = 0x0002
        self.KEYEVENTF_SCANCODE    = 0x0008
        
        # MAPEO DE SCANCODES (Para compatibilidad DX/Games)
        # Esto es vital para juegos que leen scancodes directos y no VirtualKeys
        self.sc_map = self._build_scan_map()
        
        self.target_hwnd = None
        self.mode = "HYBRID" # "POSTMESSAGE" | "SENDINPUT" | "HYBRID"
        self.screen_width = self.user32.GetSystemMetrics(0)
        self.screen_height = self.user32.GetSystemMetrics(1)
        
        # Scaling
        self.game_w = 1920
        self.game_h = 1080
        self.view_w = 1920
        self.view_h = 1080

    def set_target(self, hwnd):
        self.target_hwnd = hwnd

    def update_scaling(self, view_w, view_h, game_w, game_h):
        self.view_w, self.view_h = view_w, view_h
        self.game_w, self.game_h = game_w, game_h

    # =========================================================================
    # 🖱️ MOUSE HANDLER
    # =========================================================================
    def forward_mouse(self, event_type, local_x, local_y, buttons, delta=0):
        if not self.target_hwnd: return

        # 1. Calcular coordenadas absolutas de pantalla reales (Para SendInput)
        # Convertir coord vista -> coord juego -> coord pantalla
        # Simplificación: si el juego ocupa toda la pantalla, mapeamos a coords absolutas [0..65535]
        
        # A) Coordenadas para PostMessage (Relativas al Client Area del Juego)
        pm_x = int(local_x * (self.game_w / self.view_w))
        pm_y = int(local_y * (self.game_h / self.view_h))
        
        # B) Coordenadas para SendInput (Absolutas normalizadas 0-65535)
        # Las coordenadas target dependen de donde este la Ventana REAL.
        # Si esta en modo SafeBox (oculta o offscreen), SendInput MOVERÁ EL MOUSE REAL ALLI.
        # Esto puede ser molesto, pero es la única forma "Hardware" real.
        rect = wintypes.RECT()
        self.user32.GetWindowRect(self.target_hwnd, ctypes.byref(rect))
        win_x, win_y = rect.left, rect.top
        
        abs_x = win_x + pm_x
        abs_y = win_y + pm_y
        
        norm_x = int((abs_x / self.screen_width) * 65535)
        norm_y = int((abs_y / self.screen_height) * 65535)

        # 🚀 HYBRID LOGIC
        # Intentamos PostMessage primero si el modo lo permite, pero SendInput es más compatible para Clicks.
        
        if self.mode == "HYBRID" or self.mode == "SENDINPUT":
            self._send_input_mouse(event_type, norm_x, norm_y, buttons, delta)
        else:
            self._post_message_mouse(event_type, pm_x, pm_y, buttons, delta)

    def _send_input_mouse(self, event_type, x, y, buttons, delta):
        flags = self.MOUSEEVENTF_ABSOLUTE | self.MOUSEEVENTF_MOVE
        data = 0
        
        if event_type == "move":
            pass # Solo move
            
        elif event_type == "press":
            if buttons & Qt.LeftButton: flags |= self.MOUSEEVENTF_LEFTDOWN
            if buttons & Qt.RightButton: flags |= self.MOUSEEVENTF_RIGHTDOWN
            if buttons & Qt.MiddleButton: flags |= self.MOUSEEVENTF_MIDDLEDOWN
            
        elif event_type == "release":
            if buttons & Qt.LeftButton: flags |= self.MOUSEEVENTF_LEFTUP
            if buttons & Qt.RightButton: flags |= self.MOUSEEVENTF_RIGHTUP
            if buttons & Qt.MiddleButton: flags |= self.MOUSEEVENTF_MIDDLEUP

        elif event_type == "wheel":
            flags = self.MOUSEEVENTF_WHEEL
            data = delta # Winsdk espera multiplos de 120 normalmente

        # Ejecutar Input Injection
        extra = ctypes.c_ulonglong(0)
        ii_ = INPUT_I()
        ii_.mi = MOUSEINPUT(x, y, data, flags, 0, extra)
        cmd = INPUT(self.INPUT_MOUSE, ii_)
        self.user32.SendInput(1, ctypes.pointer(cmd), ctypes.sizeof(cmd))

    def _post_message_mouse(self, event_type, x, y, buttons, delta):
        lparam = (y << 16) | (x & 0xFFFF)
        wparam = 0
        if buttons & Qt.LeftButton: wparam |= self.MK_LBUTTON
        if buttons & Qt.RightButton: wparam |= self.MK_RBUTTON
        
        if event_type == "move":
            self.user32.PostMessageW(self.target_hwnd, self.WM_MOUSEMOVE, wparam, lparam)
        elif event_type == "press":
            if buttons & Qt.LeftButton: self.user32.PostMessageW(self.target_hwnd, self.WM_LBUTTONDOWN, wparam, lparam)
            if buttons & Qt.RightButton: self.user32.PostMessageW(self.target_hwnd, self.WM_RBUTTONDOWN, wparam, lparam)
        elif event_type == "release":
            if buttons & Qt.LeftButton: self.user32.PostMessageW(self.target_hwnd, self.WM_LBUTTONUP, wparam, lparam)
            if buttons & Qt.RightButton: self.user32.PostMessageW(self.target_hwnd, self.WM_RBUTTONUP, wparam, lparam)
        elif event_type == "wheel":
            # Wheel en PostMessage es tricky, wparam highword es delta
            wparam = (delta << 16)
            self.user32.PostMessageW(self.target_hwnd, self.WM_MOUSEWHEEL, wparam, lparam)

    # =========================================================================
    # ⌨️ KEYBOARD HANDLER
    # =========================================================================
    def forward_key(self, key_code, is_press):
        if not self.target_hwnd: return
        
        # Mapeo a ScanCode (Vital para DirectX)
        scan_code, vk_code = self._map_key(key_code)
        
        if self.mode == "HYBRID" or self.mode == "SENDINPUT":
            self._send_input_key(scan_code, vk_code, is_press)
        else:
            self._post_message_key(vk_code, is_press)

    def _send_input_key(self, scan_code, vk_code, is_press):
        flags = self.KEYEVENTF_SCANCODE
        if not is_press: flags |= self.KEYEVENTF_KEYUP
        
        # Handle Extended keys (Arrows, Home, End, etc)
        # if vk_code in [list of extended]: flags |= self.KEYEVENTF_EXTENDEDKEY (Simplificado)
        
        extra = ctypes.c_ulonglong(0)
        ii_ = INPUT_I()
        ii_.ki = KEYBDINPUT(0, scan_code, flags, 0, extra) # Hardware via ScanCode
        cmd = INPUT(self.INPUT_KEYBOARD, ii_)
        self.user32.SendInput(1, ctypes.pointer(cmd), ctypes.sizeof(cmd))

    def _post_message_key(self, vk_code, is_press):
        msg = self.WM_KEYDOWN if is_press else self.WM_KEYUP
        self.user32.PostMessageW(self.target_hwnd, msg, vk_code, 0)

    # =========================================================================
    # 🗺️ MAPPING UTILS
    # =========================================================================
    def _map_key(self, qt_key):
        # Retorna (ScanCode, VirtualKey)
        # ScanCodes Set 1 (Standard US)
        # Fallback simple
        sc = 0
        vk = 0
        
        # 1. Letras A-Z
        if Qt.Key_A <= qt_key <= Qt.Key_Z:
            offset = qt_key - Qt.Key_A
            vk = 0x41 + offset
            # Scan codes A=0x1E ...
            # Esto es tedioso hardcodear todo, usamos MapVirtualKey si es posible
            sc = self.user32.MapVirtualKeyW(vk, 0) 
            return sc, vk
            
        # 2. Numeros 0-9
        if Qt.Key_0 <= qt_key <= Qt.Key_9:
            offset = qt_key - Qt.Key_0
            vk = 0x30 + offset
            sc = self.user32.MapVirtualKeyW(vk, 0)
            return sc, vk
            
        # 3. Especiales (Quick Lookup)
        manual_map = {
            Qt.Key_Space: (0x39, 0x20),
            Qt.Key_Return: (0x1C, 0x0D),
            Qt.Key_Escape: (0x01, 0x1B),
            Qt.Key_Shift: (0x2A, 0x10),
            Qt.Key_Control: (0x1D, 0x11),
            Qt.Key_Alt: (0x38, 0x12),
            Qt.Key_Tab: (0x0F, 0x09),
            Qt.Key_Backspace: (0x0E, 0x08),
            
            Qt.Key_Left: (0x4B, 0x25),
            Qt.Key_Right: (0x4D, 0x27),
            Qt.Key_Up: (0x48, 0x26),
            Qt.Key_Down: (0x50, 0x28),
            
            Qt.Key_F1: (0x3B, 0x70),
            Qt.Key_F2: (0x3C, 0x71),
            Qt.Key_F3: (0x3D, 0x72),
            Qt.Key_F4: (0x3E, 0x73),
            Qt.Key_F5: (0x3F, 0x74),
            Qt.Key_F6: (0x40, 0x75),
            Qt.Key_F7: (0x41, 0x76),
            Qt.Key_F8: (0x42, 0x77),
            Qt.Key_F9: (0x43, 0x78),
            Qt.Key_F10: (0x44, 0x79),
            Qt.Key_F11: (0x57, 0x7A),
            Qt.Key_F12: (0x58, 0x7B),
        }
        
        if qt_key in manual_map:
            return manual_map[qt_key]
            
        # Generic Fallback
        return (0, 0)

    def _build_scan_map(self):
        # Placeholder, used in future expansions
        return {}
