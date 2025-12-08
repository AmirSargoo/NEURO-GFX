import sys
import ctypes
import time
from ctypes import wintypes
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QTimer, Qt

# ============================================================================
# 📦 NTR SAFEBOX™ - Módulo de Aislamiento
# ============================================================================
class SafeBox(QWidget):
    """
    Contenedor invisible que 'traga' las ventanas de los juegos.
    Actúa como un 'Black Hole' en el escritorio para el usuario,
    pero mantiene el juego vivo para el RDX Hook.
    """
    def __init__(self):
        super().__init__()
        # Configuración de ventana invisible pero existente
        self.setWindowTitle("NTR SafeBox Container")
        self.resize(100, 100) # Tamaño irrelevante, se ajustará
        # Flags para que no moleste en la barra de tareas ni se vea
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # API Nativa
        self.user32 = ctypes.windll.user32
        self.target_hwnd = None
        self.original_parent = None
        self.original_style = None

    def capture_process(self, pid: int):
        """Busca la ventana principal del PID y la incrusta."""
        hwnd = self._find_window_by_pid(pid)
        if not hwnd:
            return False
            
        self.target_hwnd = hwnd
        
        # 1. Guardar estado original
        self.original_parent = self.user32.GetParent(hwnd)
        self.original_style = self.user32.GetWindowLongW(hwnd, -16) # GWL_STYLE
        
        # 2. Preparar el contenedor (Jail)
        # Hacemos que la SafeBox sea visible pero fuera de pantalla o detrás
        # IMPORTANTE: Para que WGC capture, la ventana NO debe estar minimizada.
        # Pero podemos ponerla "off-screen" o cubierta.
        self.move(-32000, -32000) # Mover al limbo
        self.show()
        
        # 3. Secuestrar (SetParent)
        # Al ponerla como hija de SafeBox, desaparece del escritorio principal
        self.user32.SetParent(hwnd, int(self.winId()))
        
        # 4. Modificar Estilo (Quitar bordes para render limpio)
        # WS_POPUP (0x80000000) | WS_VISIBLE (0x10000000)
        new_style = 0x80000000 | 0x10000000 
        self.user32.SetWindowLongW(hwnd, -16, new_style)
        
        # 5. Ajustar tamaño y posición relativa al contenedor (0,0)
        self.user32.SetWindowPos(hwnd, 0, 0, 0, 1920, 1080, 0x0040) # SWP_SHOWWINDOW
        
        return True

    def release(self):
        """Libera al rehén."""
        if self.target_hwnd:
            # Restaurar padre (Escritorio = 0)
            self.user32.SetParent(self.target_hwnd, 0)
            # Restaurar estilo
            if self.original_style:
                self.user32.SetWindowLongW(self.target_hwnd, -16, self.original_style)
            
            # Traer al frente
            self.user32.SetWindowPos(self.target_hwnd, 0, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0040)
            self.target_hwnd = None
            
        self.close()

    def _find_window_by_pid(self, pid):
        # ... (Lógica de búsqueda existente que funciona bien) ...
        result = None
        def callback(hwnd, _):
            nonlocal result
            curr_pid = wintypes.DWORD()
            self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(curr_pid))
            if curr_pid.value == pid and self.user32.IsWindowVisible(hwnd):
                result = hwnd
                return False # Stop enum
            return True
        
        self.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)(callback), 0)
        return result
