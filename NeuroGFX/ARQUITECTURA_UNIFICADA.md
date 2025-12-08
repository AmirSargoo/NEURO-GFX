# 🎛️ NEURO-GFX UNIFIED ARCHITECTURE
# ====================================

## 🧠 CONCEPTO CENTRAL
Neuro-OS GFX evoluciona de ser una herramienta de captura a una **Plataforma Híbrida**.
El usuario elige el "Motor de Ejecución" según sus necesidades (Estabilidad, Rendimiento o Movilidad).

---

## 🚀 LOS 3 MOTORES (MODOS DE OPERACIÓN)

### 🛡️ MODO A: STABILITY CORE (Passive Capture)
*Tecnología actual (WGC/MSS + InputMapper)*
- **Ideal para**: Demos, Inversores, Compatibilidad 100%, Anti-Cheat safe.
- **Funcionamiento**: Captura "desde fuera" (OS Level). No toca la memoria del juego.
- **Estado**: ✅ FUNCIONAL.

### ⚡ MODO B: NEURO HOOK (Internal Injection)
*Tecnología agresiva (DLL Injection + Shared Texture)*
- **Ideal para**: Rendimiento extremo, PCs Viejos (0% CPU impact), Modding.
- **Funcionamiento**: Inyección de código en el proceso. Renderizado nativo.
- **Estado**: 🏗️ EN CONSTRUCCIÓN (Requiere DLL C++).

### 📡 MODO C: QUANTUM LINK (Local Streaming)
*Tecnología de Red (Video over UDP/TCP)*
- **Ideal para**: Jugar en Laptop vieja usando la potencia del PC principal, o Coop local.
- **Funcionamiento**: El frame capturado (por A o B) se comprime (JPEG/H264) y se envía por LAN.
- **Estado**: 📝 DISEÑO (Stub de Socket).

---

## 🛠️ ESTRUCTURA DE ARCHIVOS ACTUALIZADA

- `NEURO_GFX_PANEL.py`: **NUEVO**. Interfaz Selectora de Modos.
- `NEURO_GFX_LAUNCHER.py`: Motor de ejecución (recibe config).
- `NeuroGFX/`
    - `engines/`
        - `engine_passive.py` (Wrapper de lo que ya tenemos)
        - `engine_hook.py` (Lógica de inyección)
        - `engine_stream.py` (Lógica de red)
    - `ntr_safebox.py`
    - `neuron_input.py`
    - `rdx_hook.py`
