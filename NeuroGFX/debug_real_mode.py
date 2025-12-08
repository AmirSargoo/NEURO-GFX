import psutil
import sys
import ctypes
from ctypes import wintypes
import time
import subprocess

def get_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        return [pid] + [p.pid for p in children]
    except psutil.NoSuchProcess:
        return [pid]

def diagnose_pid(target_pid):
    print(f"--- DIAGNOSING PID: {target_pid} ---")
    
    # 1. Get all related PIDs (Parent + Children)
    all_pids = get_process_tree(target_pid)
    print(f"Process Tree: {all_pids}")
    
    user32 = ctypes.windll.user32

    EnumWindows = user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    GetWindowTextW = user32.GetWindowTextW
    GetWindowTextLengthW = user32.GetWindowTextLengthW
    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    IsWindowVisible = user32.IsWindowVisible

    windows = []

    def callback(hwnd, _):
        _pid = wintypes.DWORD()
        GetWindowThreadProcessId(hwnd, ctypes.byref(_pid))

        # Check against ANY pid in the tree
        if _pid.value in all_pids:
            length = GetWindowTextLengthW(hwnd)
            title = ctypes.create_unicode_buffer(length + 1)
            GetWindowTextW(hwnd, title, length + 1)
            
            is_visible = IsWindowVisible(hwnd)
            
            # Get Window Rect
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            w = rect.right - rect.left
            h = rect.bottom - rect.top
            
            # Get Style
            style = user32.GetWindowLongW(hwnd, -16) # GWL_STYLE
            
            windows.append({
                "hwnd": hwnd,
                "pid": _pid.value,
                "title": title.value,
                "visible": is_visible,
                "size": (w, h),
                "style": hex(style)
            })
        return True

    EnumWindows(EnumWindowsProc(callback), 0)

    print(f"Found {len(windows)} windows in tree:")
    for win in windows:
        v_str = "[VISIBLE]" if win['visible'] else "[HIDDEN]"
        print(f"- PID: {win['pid']} | HWND: {win['hwnd']} | {v_str} | Size: {win['size']} | Style: {win['style']} | Title: '{win['title']}'")

    if not windows:
        print("[!] NO WINDOWS DETECTED FOR THIS PID TREE.")
    else:
        # Recommendation logic
        visible_wins = [w for w in windows if w['visible'] and w['size'][0]>0]
        if visible_wins:
            # Sort by area
            visible_wins.sort(key=lambda x: x['size'][0]*x['size'][1], reverse=True)
            best = visible_wins[0]
            print(f"[OK] Best candidate: HWND {best['hwnd']} (PID {best['pid']}) - '{best['title']}'")
        else:
            print("[!] Only found HIDDEN windows. Needs wait-loop or force-show.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pid = int(sys.argv[1])
        diagnose_pid(pid)
    else:
        # Test Mode: Launch Notepad
        print("Launching Notepad for diagnosis...")
        proc = subprocess.Popen("notepad.exe")
        time.sleep(1.5) # Wait for creation
        diagnose_pid(proc.pid)
