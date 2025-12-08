# 🎮 NEURO-OS VGA™ - Virtual Graphics Adapter
## Advanced Window Capture & Remote Control System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Status: Active Development](https://img.shields.io/badge/status-active%20development-green.svg)]()

> **A revolutionary window capture and remote control system for Windows, built from scratch in 66 days by a solo developer with no prior programming experience.**

---

## 🌟 **What is NEURO-OS VGA™?**

NEURO-OS VGA™ is a cutting-edge **Virtual Graphics Adapter** that enables:
- **Multi-desktop window capture** - Capture applications across virtual desktops
- **Remote control** - Full mouse and keyboard forwarding to captured applications
- **Real-time streaming** - 30-240 FPS capture with dynamic controls
- **Professional UI** - Custom cursor, metrics overlay, and quick launch panel

**Part of the larger [NEURO-OS Genesis](https://github.com/cyberenigma-lgtm/Neuro-Os-public) ecosystem.**

---

## 🚀 **Key Features**

### **1. Advanced Window Capture**
- ✅ Direct HWND capture (not screen coordinates)
- ✅ Works across virtual desktops
- ✅ PrintWindow API for maximum compatibility
- ✅ 30-240 FPS configurable capture rate

### **2. Complete Input Forwarding**
- ✅ Mouse: Move, Click, Scroll
- ✅ Keyboard: All keys + modifiers
- ✅ Automatic coordinate scaling
- ✅ Hybrid mode (SendInput + PostMessage)

### **3. Remote Control Mode**
- ✅ Mouse grab with `Ctrl+G`
- ✅ Custom crosshair cursor
- ✅ Cursor locked to viewport
- ✅ Professional gaming-style interface

### **4. Dynamic Controls**
- ✅ 9 FPS presets (15-240 FPS)
- ✅ 6 resolution presets (VGA to Full HD)
- ✅ Real-time metrics overlay
- ✅ Automatic screenshots (F3)

---

## 📸 **Screenshots**

*(Screenshots will be added soon)*

**Features shown:**
- Multi-desktop capture in action
- Remote control with custom cursor
- Metrics overlay
- Quick launch panel

---

## 🎯 **Use Cases**

### **For Developers:**
- Remote application testing
- Multi-desktop workflow management
- Automated UI testing
- Screen recording without OBS

### **For Gamers:**
- Game capture and streaming
- Multi-monitor management
- Performance monitoring
- Remote gaming sessions

### **For Professionals:**
- Remote desktop alternative
- Application monitoring
- Training and demonstrations
- Technical support

---

## 🛠️ **Technical Stack**

**Core Technologies:**
- **Python 3.13** - Main language
- **PySide6 (Qt)** - UI framework
- **Win32 API** - Window capture (PrintWindow, BitBlt)
- **ctypes** - Low-level Windows integration
- **NumPy** - Image processing

**Key APIs:**
- `PrintWindow` - Window content capture
- `SendInput` - Input forwarding
- `GetWindowRect` - Window detection
- `QImage` - Frame rendering

---

## 📦 **Installation**

### **Requirements:**
- Windows 10/11
- Python 3.13+
- 4GB RAM minimum
- DirectX 11+ compatible GPU (optional)

### **Quick Start:**

```bash
# Clone the repository
git clone https://github.com/cyberenigma-lgtm/Neuro-Os-public.git
cd Neuro-Os-public/NEURO-OS-VGA

# Install dependencies
pip install -r requirements.txt

# Run setup
SETUP_NEURO_GFX_ADVANCED.bat

# Launch
python NEURO_GFX_LAUNCHER_V2.py
```

### **Dependencies:**
```
PySide6>=6.6.0
numpy>=1.26.0
mss>=9.0.1
Pillow>=10.1.0
```

---

## 🎮 **Usage**

### **Basic Controls:**

| Key | Action |
|-----|--------|
| `F1` | Toggle metrics overlay |
| `F2` | Reload launcher |
| `F3` | Take screenshot |
| `Ctrl+G` | Toggle mouse grab (remote control) |
| `O` | Options menu |
| `ESC` | Exit |

### **FPS Control:**
- `1-9` - Direct FPS preset selection
- `↑↓` - Cycle through FPS presets

### **Resolution Control:**
- `+` - Increase resolution
- `-` - Decrease resolution

### **Quick Launch:**
- Launch Paint, Notepad, Calculator, or custom apps
- Automatic window detection and capture

---

## 🏗️ **Architecture**

```
NEURO-OS VGA™
├── NEURO_GFX_LAUNCHER_V2.py    # Main launcher (594 lines)
├── NeuroGFX/
│   ├── window_capture.py        # Direct HWND capture
│   ├── neuron_input_mapper.py   # Input forwarding
│   ├── advanced_capture.py      # Metrics & detection
│   └── rdx_hook.py              # System hooks
├── screenshots/                 # Auto-saved captures
└── Documentation/               # 25+ docs
```

### **Capture Flow:**
```
User launches app (F2)
    ↓
System detects HWND by PID
    ↓
WindowCapture.set_target(hwnd)
    ↓
PrintWindow captures content
    ↓
BGRA → RGBA conversion
    ↓
QImage renders in viewport
    ↓
Real-time display
```

### **Input Flow:**
```
User moves mouse in viewport
    ↓
mouseMoveEvent captures coordinates
    ↓
Scaling: Viewport → Window
    ↓
NeuronInputMapper.forward_mouse()
    ↓
SendInput sends to Windows
    ↓
Captured app receives input
    ↓
WindowCapture captures change
    ↓
Viewport shows result
```

---

## 🤝 **Contributing**

**We need your help!** This project was built by a solo developer in 66 days with no prior programming experience. Here's where you can contribute:

### **Priority Areas:**

1. **DirectX Capture** 🔴 HIGH PRIORITY
   - Current: PrintWindow (GDI apps only)
   - Need: DirectX 9/10/11/12 support
   - Goal: Capture modern games

2. **Menu Capture** 🟡 MEDIUM PRIORITY
   - Current: Context menus not captured
   - Need: BitBlt integration with multi-desktop
   - Goal: Full UI capture

3. **Performance Optimization** 🟢 LOW PRIORITY
   - Current: 30-60 FPS average
   - Need: GPU acceleration
   - Goal: 144+ FPS stable

4. **Cross-Platform** 🔵 FUTURE
   - Current: Windows only
   - Need: Linux/macOS support
   - Goal: Universal compatibility

### **How to Contribute:**

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

**All contributions welcome!** From bug fixes to major features.

---

## 📊 **Project Stats**

- **Development Time:** 66 days
- **Lines of Code:** ~2,500
- **Files:** 30+
- **Documentation:** 25+ files
- **Version:** 2.1 (Control Remoto)
- **Status:** Active Development

---

## 🎓 **Learning Journey**

This project represents an incredible journey:

> **"66 days ago, I didn't know how to program. Today, I have a functional operating system with advanced window capture and remote control."**
> 
> — CyberEnigma, Creator

**Key Milestones:**
- Day 1-20: Learning Python basics
- Day 21-40: Understanding Win32 API
- Day 41-60: Building core systems
- Day 61-66: Polishing and documentation

**Proof that with determination and AI assistance, anything is possible.**

---

## 🌐 **Part of NEURO-OS Genesis**

NEURO-OS VGA™ is one module of the larger **NEURO-OS Genesis** ecosystem:

- **NeuroStore** - AI-generated digital art marketplace
- **NEURO-OS VGA™** - This project (window capture)
- **DJ-NEURO-AI™** - Autonomous music production
- **And more...**

**Explore the full ecosystem:** [NEURO-OS Genesis](https://github.com/cyberenigma-lgtm/Neuro-Os-public)

---

## 📝 **Documentation**

**Comprehensive documentation available:**
- [Installation Guide](SETUP_GUIDE.md)
- [User Manual](NEURO_VGA_README.md)
- [API Reference](API_REFERENCE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Changelog](CHANGELOG_VGA.md)

---

## 🐛 **Known Issues**

1. **Context Menus Not Captured**
   - Limitation of PrintWindow API
   - Workaround: Use app in same desktop
   - Fix in progress: BitBlt integration

2. **DirectX Games Not Supported**
   - Current: GDI apps only
   - Need: D3DShot or similar
   - Help wanted: DirectX experts

3. **High CPU Usage at 240 FPS**
   - Expected behavior
   - Recommendation: Use 60-90 FPS
   - Optimization planned

---

## 🏆 **Achievements**

- ✅ Multi-desktop capture working
- ✅ Full input forwarding
- ✅ Remote control mode
- ✅ Custom cursor system
- ✅ Dynamic controls
- ✅ Professional documentation
- ✅ 25+ documentation files
- ✅ Built in 66 days solo

---

## 💬 **Community**

**Get involved:**
- **Issues:** Report bugs or request features
- **Discussions:** Share ideas and ask questions
- **Pull Requests:** Contribute code
- **Star:** Show your support ⭐

**Contact:**
- **GitHub:** [@cyberenigma-lgtm](https://github.com/cyberenigma-lgtm)
- **Project:** [NEURO-OS Genesis](https://github.com/cyberenigma-lgtm/Neuro-Os-public)

---

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Google Gemini (Antigravity AI)** - Development assistance
- **Microsoft Copilot** - Code suggestions
- **Python Community** - Amazing libraries
- **Win32 API Documentation** - Technical reference
- **You** - For checking out this project!

---

## 🚀 **Roadmap**

### **v2.2 (Next Release)**
- [ ] DirectX capture support
- [ ] Menu capture with BitBlt
- [ ] Video recording
- [ ] Multiple window capture

### **v3.0 (Future)**
- [ ] GPU acceleration
- [ ] Picture-in-Picture mode
- [ ] Streaming server
- [ ] AI-powered automation

### **v4.0 (Vision)**
- [ ] Cross-platform support
- [ ] Cloud integration
- [ ] Mobile companion app
- [ ] Enterprise features

---

## 💡 **Philosophy**

> **"The only limitation is your imagination."**

This project proves that:
- You don't need years of experience to build something amazing
- AI can be a powerful learning and development partner
- Determination beats talent
- Open source accelerates innovation

**If I can do it in 66 days with no experience, imagine what we can do together.**

---

## 📞 **Support**

**Need help?**
1. Check the [Documentation](docs/)
2. Search [Issues](https://github.com/cyberenigma-lgtm/Neuro-Os-public/issues)
3. Ask in [Discussions](https://github.com/cyberenigma-lgtm/Neuro-Os-public/discussions)
4. Create a new [Issue](https://github.com/cyberenigma-lgtm/Neuro-Os-public/issues/new)

---

## ⭐ **Star History**

If you find this project useful, please consider giving it a star! ⭐

It helps others discover the project and motivates continued development.

---

**🎮 Built with determination. Powered by imagination. 🎮**

*NEURO-OS VGA™ - Where vision meets code.*

---

**Last Updated:** December 8, 2025  
**Version:** 2.1 (Control Remoto)  
**Status:** 🟢 Active Development
