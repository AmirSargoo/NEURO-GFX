#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 NEURO-GFX WINDOW CAPTURE FIX
-------------------------------
Captura directa de ventana usando PrintWindow de Win32 API.
Esto captura el contenido de la ventana sin importar dónde esté ubicada.
"""

import ctypes
from ctypes import wintypes
import numpy as np
from PIL import Image

class WindowCapture:
    """Captura el contenido de una ventana específica usando PrintWindow"""
    
    def __init__(self):
        self.hwnd = None
        self.last_frame = None
        
    def set_target(self, hwnd):
        """Establece la ventana objetivo"""
        self.hwnd = hwnd
        
    def capture(self):
        """Captura el contenido de la ventana usando PrintWindow"""
        if not self.hwnd:
            return None
            
        try:
            # Obtener dimensiones de la ventana
            rect = wintypes.RECT()
            ctypes.windll.user32.GetClientRect(self.hwnd, ctypes.byref(rect))
            w = rect.right - rect.left
            h = rect.bottom - rect.top
            
            if w <= 0 or h <= 0:
                return None
            
            # Crear contexto de dispositivo
            hwndDC = ctypes.windll.user32.GetDC(self.hwnd)
            mfcDC = ctypes.windll.gdi32.CreateCompatibleDC(hwndDC)
            saveBitMap = ctypes.windll.gdi32.CreateCompatibleBitmap(hwndDC, w, h)
            ctypes.windll.gdi32.SelectObject(mfcDC, saveBitMap)
            
            # Usar PrintWindow (funciona siempre)
            result = ctypes.windll.user32.PrintWindow(self.hwnd, mfcDC, 2)
            if result == 0:
                result = ctypes.windll.user32.PrintWindow(self.hwnd, mfcDC, 0)
            
            # Crear estructura BITMAPINFO
            bmpinfo = ctypes.create_string_buffer(40)
            ctypes.memmove(bmpinfo, ctypes.byref(ctypes.c_long(40)), 4)
            ctypes.memmove(ctypes.byref(bmpinfo, 4), ctypes.byref(ctypes.c_long(w)), 4)
            ctypes.memmove(ctypes.byref(bmpinfo, 8), ctypes.byref(ctypes.c_long(-h)), 4)
            ctypes.memmove(ctypes.byref(bmpinfo, 12), ctypes.byref(ctypes.c_short(1)), 2)
            ctypes.memmove(ctypes.byref(bmpinfo, 14), ctypes.byref(ctypes.c_short(32)), 2)
            
            # Obtener bits del bitmap
            bmpstr = ctypes.create_string_buffer(w * h * 4)
            ctypes.windll.gdi32.GetDIBits(
                mfcDC, saveBitMap, 0, h, bmpstr, bmpinfo, 0
            )
            
            # Limpiar
            ctypes.windll.gdi32.DeleteObject(saveBitMap)
            ctypes.windll.gdi32.DeleteDC(mfcDC)
            ctypes.windll.user32.ReleaseDC(self.hwnd, hwndDC)
            
            # Convertir a numpy array
            img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((h, w, 4))
            img = img[:, :, [2, 1, 0, 3]]  # BGRA -> RGBA
            
            self.last_frame = img
            return img
            
        except Exception as e:
            print(f"❌ Error capturando ventana: {e}")
            return self.last_frame
    
    def get_snap(self):
        """Alias para compatibilidad"""
        return self.capture()


if __name__ == "__main__":
    print("🔧 Window Capture Module - Test")
    print("Este módulo captura ventanas directamente sin importar su posición")
