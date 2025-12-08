
# 👁️ RDX Hook™ (Realtime DirectX Hook)
# ------------------------------------
# Modulo de Captura Unificado (WGC + MSS + IPC Shared Memory)

import sys
import numpy as np
import mmap
import os

# Backend 1: WGC (Windows Graphics Capture)
HAS_WGC = False
try:
    import winsdk.windows.graphics.capture
    HAS_WGC = True
except ImportError:
    HAS_WGC = False

# Backend 2: MSS (Memory Screen Scan)
import mss

# Backend 3: SHM (Shared Memory for Hook)
class RDXHookSHM:
    """
    Hook de Memoria Compartida para Modo Inyección (Mode B).
    Lee buffers de video directamente de la RAM/VRAM compartida por la DLL.
    """
    def __init__(self, shm_name="NeuroGFX_FrameBuffer", width=1920, height=1080):
        self.shm_name = shm_name
        self.width = width
        self.height = height
        self.size = width * height * 4 # BGRA
        self.mm = None
        self.connected = False
        
    def connect(self):
        try:
            # En Windows, mmap puede abrir FileMapping por nombre
            # La DLL debe haber creado "Global\NeuroGFX_FrameBuffer" o similar
            self.mm = mmap.mmap(-1, self.size, tagname=self.shm_name, access=mmap.ACCESS_READ)
            self.connected = True
            print(f"RDX-SHM: Connected to {self.shm_name}")
        except FileNotFoundError:
            # La DLL aun no ha creado el buffer (el juego esta cargando)
            pass
        except Exception as e:
            print(f"RDX-SHM Error: {e}")

    def get_snap(self):
        if not self.connected: 
            self.connect()
            return None
            
        try:
            self.mm.seek(0)
            # Leer buffer. Es LENTO en Python puro hacer read() grande cada frame.
            # Idealmente usariamos memoryview.
            buf = self.mm.read(self.size)
            img = np.frombuffer(buf, dtype=np.uint8).reshape((self.height, self.width, 4))
            return img
        except Exception:
            self.connected = False # Lost connection
            return None

class RDXHookMSS:
    # ... (Ya definido anteriormente) ...
    def __init__(self):
        self.sct = mss.mss()
        self.monitor = None
        self.last_frame = None
    
    def set_target_rect(self, x, y, w, h):
        self.monitor = {"top": y, "left": x, "width": w, "height": h}
        
    def get_snap(self):
        if not self.monitor: return None
        try:
            sct_img = self.sct.grab(self.monitor)
            return np.array(sct_img) 
        except Exception: return None

class RDXHookWGC:
    # Stub placehoder
    pass

# Factory
def RDXHook(mode="PASSIVE", w=1920, h=1080):
    if mode == "HOOK":
        return RDXHookSHM(width=w, height=h)
    
    if HAS_WGC and mode == "PASSIVE":
        # WGC Logic Wrapper
        return RDXHookWGC() # Not fully implemented yet
    else:
        # Default Fallback
        return RDXHookMSS()
