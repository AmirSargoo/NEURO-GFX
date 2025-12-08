# 🤝 Contributing to NEURO-OS VGA™

Thank you for your interest in contributing to NEURO-OS VGA™! This project was built by a solo developer in 66 days with no prior programming experience, and we welcome all contributions from the community.

---

## 🌟 **Why Contribute?**

- **Learn:** Work with Win32 API, Qt, and advanced Python
- **Impact:** Help build a revolutionary window capture system
- **Community:** Join a project that proves determination beats experience
- **Recognition:** All contributors will be acknowledged

---

## 🎯 **Priority Areas**

### **🔴 HIGH PRIORITY**

#### **1. DirectX Capture Support**
**Current State:** Only GDI applications supported (Paint, Notepad, etc.)  
**Goal:** Capture DirectX 9/10/11/12 games and applications  
**Skills Needed:** DirectX, C++, Python ctypes  
**Impact:** CRITICAL - Enables gaming and modern app capture  

**What we need:**
- Integration with D3DShot or similar
- DirectX hook implementation
- GPU-accelerated capture
- Frame buffer reading

**Resources:**
- [D3DShot Documentation](https://github.com/brunk23/d3dshot)
- [DirectX SDK](https://docs.microsoft.com/en-us/windows/win32/directx)

---

#### **2. Context Menu Capture**
**Current State:** Menus and popups not captured  
**Goal:** Full UI capture including overlays  
**Skills Needed:** Win32 API, BitBlt  
**Impact:** HIGH - Complete visual fidelity  

**What we need:**
- BitBlt integration with multi-desktop detection
- Window hierarchy traversal
- Overlay composition
- Real-time menu detection

**Technical Challenge:**
- PrintWindow doesn't capture child windows
- BitBlt only works on visible windows
- Need hybrid approach

---

### **🟡 MEDIUM PRIORITY**

#### **3. Performance Optimization**
**Current State:** 30-60 FPS average, high CPU usage at 240 FPS  
**Goal:** 144+ FPS stable with low CPU usage  
**Skills Needed:** Python optimization, GPU programming  
**Impact:** MEDIUM - Better user experience  

**What we need:**
- GPU-accelerated image processing
- Multi-threading optimization
- Memory management improvements
- Frame skipping intelligence

---

#### **4. Video Recording**
**Current State:** Only screenshots (F3)  
**Goal:** Full video recording with audio  
**Skills Needed:** FFmpeg, Python  
**Impact:** MEDIUM - New feature  

**What we need:**
- FFmpeg integration
- Audio capture from system
- Codec selection
- Real-time encoding

---

### **🟢 LOW PRIORITY**

#### **5. Multiple Window Capture**
**Current State:** One window at a time  
**Goal:** Picture-in-Picture, multiple viewports  
**Skills Needed:** Qt, UI design  
**Impact:** LOW - Nice to have  

---

#### **6. Streaming Server**
**Current State:** Local only  
**Goal:** Remote access via web browser  
**Skills Needed:** WebRTC, Flask/FastAPI  
**Impact:** LOW - Advanced feature  

---

## 📋 **How to Contribute**

### **Step 1: Choose an Issue**

1. Browse [Issues](https://github.com/cyberenigma-lgtm/Neuro-Os-public/issues)
2. Look for `good first issue` or `help wanted` labels
3. Comment on the issue to claim it
4. Wait for maintainer approval

### **Step 2: Set Up Development Environment**

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/Neuro-Os-public.git
cd Neuro-Os-public/NEURO-OS-VGA

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements_vga.txt

# Install dev dependencies
pip install pytest black flake8 mypy

# Test the system
python NEURO_GFX_LAUNCHER_V2.py
```

### **Step 3: Create a Branch**

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or bug fix branch
git checkout -b fix/bug-description
```

**Branch naming:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Tests

### **Step 4: Make Changes**

**Code Style:**
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Comment complex logic

**Example:**
```python
def capture_window(hwnd: int, use_bitblt: bool = False) -> np.ndarray:
    """
    Capture window content by HWND.
    
    Args:
        hwnd: Window handle to capture
        use_bitblt: Use BitBlt instead of PrintWindow
        
    Returns:
        numpy array with RGBA image data
        
    Raises:
        ValueError: If hwnd is invalid
        RuntimeError: If capture fails
    """
    # Implementation...
```

### **Step 5: Test**

```bash
# Run tests
pytest tests/

# Check code style
black .
flake8 .

# Type checking
mypy .

# Manual testing
python NEURO_GFX_LAUNCHER_V2.py
```

### **Step 6: Commit**

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add DirectX capture support

- Integrate D3DShot library
- Add GPU detection
- Implement frame buffer reading
- Update documentation

Closes #123"
```

**Commit message format:**
```
type: Short description

- Detailed change 1
- Detailed change 2
- Detailed change 3

Closes #issue_number
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code restructuring
- `test:` - Tests
- `chore:` - Maintenance

### **Step 7: Push and PR**

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Fill in the PR template
# Wait for review
```

---

## 📝 **Pull Request Guidelines**

### **PR Title:**
```
[Type] Short description (#issue)
```

**Examples:**
- `[Feature] Add DirectX capture support (#123)`
- `[Fix] Resolve mouse coordinate scaling bug (#456)`
- `[Docs] Update installation guide (#789)`

### **PR Description Template:**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tested on Windows 10
- [ ] Tested on Windows 11
- [ ] Tested with Paint
- [ ] Tested with DirectX app
- [ ] All tests pass

## Screenshots
(if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated
```

---

## 🧪 **Testing Guidelines**

### **Unit Tests:**
```python
# tests/test_window_capture.py
import pytest
from NeuroGFX.window_capture import WindowCapture

def test_capture_valid_hwnd():
    """Test capture with valid HWND"""
    capture = WindowCapture()
    capture.set_target(12345)  # Mock HWND
    frame = capture.capture()
    assert frame is not None
    assert frame.shape[2] == 4  # RGBA

def test_capture_invalid_hwnd():
    """Test capture with invalid HWND"""
    capture = WindowCapture()
    capture.set_target(0)
    frame = capture.capture()
    assert frame is None
```

### **Integration Tests:**
```python
# tests/test_integration.py
def test_full_capture_flow():
    """Test complete capture workflow"""
    # Launch test app
    # Capture window
    # Verify frame
    # Test input forwarding
    # Cleanup
```

### **Manual Testing Checklist:**
- [ ] Launch Paint
- [ ] Verify capture works
- [ ] Test mouse forwarding
- [ ] Test keyboard forwarding
- [ ] Test Ctrl+G mouse grab
- [ ] Test F3 screenshot
- [ ] Test FPS controls
- [ ] Test resolution controls
- [ ] Move to different desktop
- [ ] Verify multi-desktop works

---

## 📚 **Documentation Guidelines**

### **Code Documentation:**
- Add docstrings to all public functions
- Use Google-style docstrings
- Include type hints
- Comment complex algorithms

### **User Documentation:**
- Update README if adding features
- Add to user manual if needed
- Include screenshots/GIFs
- Write clear, concise instructions

### **Technical Documentation:**
- Document architecture changes
- Update API reference
- Add diagrams if helpful
- Explain design decisions

---

## 🎨 **Code Style**

### **Python:**
```python
# Good
def capture_window(hwnd: int) -> Optional[np.ndarray]:
    """Capture window content."""
    if not hwnd:
        return None
    return self._do_capture(hwnd)

# Bad
def captureWindow(hwnd):
    if hwnd == 0: return None
    return self._doCapture(hwnd)
```

### **Naming Conventions:**
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Descriptive names (no `x`, `y`, `temp`)

### **File Organization:**
```
NeuroGFX/
├── __init__.py
├── window_capture.py      # Window capture logic
├── input_mapper.py        # Input forwarding
├── advanced_capture.py    # Metrics
└── utils.py               # Utilities
```

---

## 🐛 **Bug Reports**

### **Good Bug Report:**
```markdown
**Title:** Mouse coordinates incorrect on 4K display

**Description:**
When using a 4K monitor (3840x2160), mouse clicks are offset by approximately 50% from the actual click position.

**Steps to Reproduce:**
1. Launch NEURO_GFX_LAUNCHER_V2.py on 4K monitor
2. Capture Paint
3. Click on a specific point
4. Observe click registers elsewhere

**Expected Behavior:**
Click should register at cursor position

**Actual Behavior:**
Click registers ~50% offset

**Environment:**
- OS: Windows 11 Pro
- Python: 3.13.0
- Display: 3840x2160 @ 150% scaling
- Version: 2.1

**Screenshots:**
(attached)

**Additional Context:**
Seems related to DPI scaling
```

---

## 💡 **Feature Requests**

### **Good Feature Request:**
```markdown
**Title:** Add support for multiple monitor capture

**Problem:**
Currently can only capture windows on primary monitor

**Proposed Solution:**
Detect all monitors and allow selection of which monitor to capture from

**Alternatives Considered:**
- Capture all monitors simultaneously
- Auto-detect monitor with active window

**Use Case:**
Users with multi-monitor setups want to capture windows on secondary displays

**Priority:**
Medium

**Willing to Contribute:**
Yes, I can help implement this
```

---

## 🏆 **Recognition**

All contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation
- Thanked in README

**Top contributors may receive:**
- Maintainer status
- Direct collaboration opportunities
- Special recognition badges

---

## 📞 **Getting Help**

**Stuck? Need guidance?**

1. **Check Documentation:**
   - [README](README_VGA_GITHUB.md)
   - [User Manual](NEURO_VGA_README.md)
   - [API Reference](API_REFERENCE.md)

2. **Ask in Discussions:**
   - [GitHub Discussions](https://github.com/cyberenigma-lgtm/Neuro-Os-public/discussions)
   - Tag with `question` or `help wanted`

3. **Join the Community:**
   - Comment on issues
   - Participate in discussions
   - Share your ideas

---

## 🌍 **Code of Conduct**

### **Our Pledge:**
We are committed to providing a welcoming and inspiring community for all.

### **Our Standards:**
- ✅ Be respectful and inclusive
- ✅ Accept constructive criticism
- ✅ Focus on what's best for the community
- ✅ Show empathy towards others

### **Unacceptable Behavior:**
- ❌ Harassment or discrimination
- ❌ Trolling or insulting comments
- ❌ Personal or political attacks
- ❌ Publishing others' private information

### **Enforcement:**
Violations may result in temporary or permanent ban from the project.

---

## 📜 **License**

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 **Thank You!**

Every contribution, no matter how small, makes a difference. Whether you:
- Fix a typo
- Report a bug
- Add a feature
- Improve documentation
- Share the project

**You're helping build something amazing.**

**Together, we can create the best window capture system ever made.**

---

**🎮 Built by the community. For the community. 🎮**

*NEURO-OS VGA™ - Where collaboration meets innovation.*

---

**Questions?** Open a [Discussion](https://github.com/cyberenigma-lgtm/Neuro-Os-public/discussions)  
**Ready to contribute?** Check [Issues](https://github.com/cyberenigma-lgtm/Neuro-Os-public/issues)  
**Want to chat?** Comment on any issue or PR  

**Let's build the future together!** 🚀
