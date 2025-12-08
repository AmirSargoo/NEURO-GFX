
import sys
import os
import ctypes
from ctypes import wintypes
import time

# Constantes Win32
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
MEM_COMMIT  = 0x1000
MEM_RESERVE = 0x2000
PAGE_READWRITE = 0x04

kernel32 = ctypes.windll.kernel32

def inject_dll(pid, dll_path):
    """
    Inyecta una DLL en el proceso remoto usando CreateRemoteThread.
    """
    dll_path_bytes = os.path.abspath(dll_path).encode('utf-16le') # Wide char for Windows
    dll_len = len(dll_path_bytes) + 2 # null terminator

    print(f"💉 INJECTOR: Target PID {pid} | Payload: {os.path.basename(dll_path)}")

    # 1. Abrir Proceso
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not h_process:
        print(f"❌ ERROR: Could not open process {pid}. (Access Denied?)")
        return False

    # 2. Reservar memoria en el proceso remoto para el path
    arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
    if not arg_address:
        print("❌ ERROR: VirtualAllocEx failed.")
        return False

    # 3. Escribir ruta de la DLL
    written = ctypes.c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, dll_path_bytes, dll_len, ctypes.byref(written))

    # 4. Obtener dirección de LoadLibraryW
    h_kernel32 = kernel32.GetModuleHandleW("kernel32.dll")
    h_loadlib = kernel32.GetProcAddress(h_kernel32, b"LoadLibraryW")

    # 5. Lanzar hilo remoto
    thread_id = ctypes.c_ulong(0)
    h_thread = kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, ctypes.byref(thread_id))
    
    if not h_thread:
        print("❌ ERROR: CreateRemoteThread failed. (Anti-Cheat blocked?)")
        success = False
    else:
        print(f"✅ SUCCESS: Remote Thread created (ID: {thread_id.value}). DLL should load.")
        kernel32.WaitForSingleObject(h_thread, -1) # Wait for init
        success = True

    # 6. Limpieza
    kernel32.VirtualFreeEx(h_process, arg_address, 0, 0x8000) # MEM_RELEASE
    kernel32.CloseHandle(h_process)
    
    return success

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: injector.py <PID> <DLL_PATH>")
    else:
        pid = int(sys.argv[1])
        dll = sys.argv[2]
        inject_dll(pid, dll)
