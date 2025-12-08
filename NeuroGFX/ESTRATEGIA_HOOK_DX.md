# ⚔️ ESTRATEGIA: OPCIÓN B (HOOK DIRECTX NATIVO)
# ============================================

## 🎯 EL OBJETIVO
Pasar de **"Mirar la pantalla"** (WGC/MSS) a **"Estar DENTRO del juego"** (Internal Hook).
Esta es la tecnología que usan herramientas como **NVIDIA DLSS**, **ReShade** y **OBS Game Capture**.

## 🧠 ¿POR QUÉ LA OPCIÓN B?
Elegimos la B porque es el **habilitador técnico** para todo lo demás:
1. **Rendimiento Puro**: Al interceptar `IDXGISwapChain::Present`, obtenemos la textura YA renderizada en VRAM. Copia = 0ms.
2. **Latencia Cero**: No esperamos al compositor de Windows (DWM).
3. **Control Total**: Podemos inyectar nuestros propios shaders (Overlay, UI, Filtros IA) *dentro* del juego.
4. **Base para Streaming (C)**: Si tenemos la textura en GPU, podemos enviarla al encoder de video (NVENC) directamente sin pasar por CPU.

---

## 🏗️ ARQUITECTURA "NEURO-HOOK DX"

### 1. El Inyector (Python)
Un script que usa `CreateRemoteThread` para forzar al juego a cargar nuestra DLL.
- Archivo: `NeuroGFX/injector.py`
- Librerías: `pymem` o `ctypes` puro.

### 2. La Carga Útil (C++ DLL)
Una librería dinámica (`neuro_hook.dll`) que el juego carga.
- **Hooking**: Usaremos **MinHook** (estándar de la industria) para interceptar DirectX.
- **Shared Memory**: Crearemos un "buffer circular" en VRAM compartido con nuestra App Python.
- **Inter-Process Communication (IPC)**: Pipes para enviar metadata (resolución, estado input).

### 3. El Cliente (Neuro Viewport)
Nuestra App Qt ya no "captura" pantalla. Simplemente "lee" la textura compartida DirectX que el juego le ofrece voluntariamente (a la fuerza).

---

## 📅 PLAN DE ATAQUE (SEMANA 1)

### DÍA 1: SCAFFOLDING (HOY)
- Definir estructura C++ del Hook.
- Crear script de inyección en Python.

### DÍA 2: COMPILACIÓN
- Configurar entorno de compilación (MSVC o MinGW) para generar la DLL.
- Compilar una "Dummy DLL" que solo haga un `MessageBox` al inyectarse (Prueba de concepto).

### DÍA 3: INTERCEPCIÓN
- Implementar Hook de `D3D11CreateDeviceAndSwapChain`.
- Lograr que el juego corra con nuestra DLL dentro sin crashear.

---

## ⚠️ NOTA TÉCNICA
Esta ruta es **Agresiva**. Muchos Anticheats (BattlEye, VAC) detestan esto.
*Para uso en "PCs Viejos" / Single Player / Emuladores, es PERFECTO.*
*Para juegos competitivos online, usaremos el modo WGC (Pasivo) que ya creamos.*
