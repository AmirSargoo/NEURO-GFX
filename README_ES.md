# 🎮 NEURO-GFX - Adaptador Gráfico Virtual
## Sistema Avanzado de Captura de Ventanas y Control Remoto

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Estado: Desarrollo Activo](https://img.shields.io/badge/estado-desarrollo%20activo-green.svg)]()

> **Un revolucionario sistema de captura de ventanas y control remoto para Windows, construido desde cero en 66 días por un desarrollador solo sin experiencia previa en programación.**

[English Version](README.md) | **Versión en Español**

---

## 🌟 **¿Qué es NEURO-GFX?**

NEURO-GFX es un **Adaptador Gráfico Virtual** de vanguardia que permite:
- **Captura multi-escritorio** - Captura aplicaciones en diferentes escritorios virtuales
- **Control remoto** - Reenvío completo de mouse y teclado a aplicaciones capturadas
- **Streaming en tiempo real** - Captura de 30-240 FPS con controles dinámicos
- **Interfaz profesional** - Cursor personalizado, overlay de métricas y panel de lanzamiento rápido

**Parte del ecosistema [NEURO-OS Genesis](https://github.com/cyberenigma-lgtm/Neuro-Os-public).**

---

## 🚀 **Características Principales**

### **1. Captura Avanzada de Ventanas**
- ✅ Captura directa por HWND (no por coordenadas de pantalla)
- ✅ Funciona entre escritorios virtuales
- ✅ API PrintWindow para máxima compatibilidad
- ✅ Tasa de captura configurable de 30-240 FPS

### **2. Reenvío Completo de Entrada**
- ✅ Mouse: Movimiento, Click, Scroll
- ✅ Teclado: Todas las teclas + modificadores
- ✅ Escalado automático de coordenadas
- ✅ Modo híbrido (SendInput + PostMessage)

### **3. Modo Control Remoto**
- ✅ Captura de mouse con `Ctrl+G`
- ✅ Cursor crosshair personalizado
- ✅ Cursor bloqueado en el viewport
- ✅ Interfaz estilo gaming profesional

### **4. Controles Dinámicos**
- ✅ 9 presets de FPS (15-240 FPS)
- ✅ 6 presets de resolución (VGA a Full HD)
- ✅ Overlay de métricas en tiempo real
- ✅ Screenshots automáticos (F3)

---

## 📸 **Capturas de Pantalla**

*(Las capturas se añadirán pronto)*

**Características mostradas:**
- Captura multi-escritorio en acción
- Control remoto con cursor personalizado
- Overlay de métricas
- Panel de lanzamiento rápido

---

## 🎯 **Casos de Uso**

### **Para Desarrolladores:**
- Testing remoto de aplicaciones
- Gestión de workflow multi-escritorio
- Testing automatizado de UI
- Grabación de pantalla sin OBS

### **Para Gamers:**
- Captura y streaming de juegos
- Gestión multi-monitor
- Monitoreo de rendimiento
- Sesiones de gaming remoto

### **Para Profesionales:**
- Alternativa a escritorio remoto
- Monitoreo de aplicaciones
- Entrenamiento y demostraciones
- Soporte técnico

---

## 🛠️ **Stack Técnico**

**Tecnologías Core:**
- **Python 3.13** - Lenguaje principal
- **PySide6 (Qt)** - Framework de UI
- **Win32 API** - Captura de ventanas (PrintWindow, BitBlt)
- **ctypes** - Integración de bajo nivel con Windows
- **NumPy** - Procesamiento de imágenes

**APIs Clave:**
- `PrintWindow` - Captura de contenido de ventanas
- `SendInput` - Reenvío de entrada
- `GetWindowRect` - Detección de ventanas
- `QImage` - Renderizado de frames

---

## 📦 **Instalación**

### **Requisitos:**
- Windows 10/11
- Python 3.13+
- 4GB RAM mínimo
- GPU compatible con DirectX 11+ (opcional)

### **Inicio Rápido:**

```bash
# Clonar el repositorio
git clone https://github.com/cyberenigma-lgtm/NEURO-GFX.git
cd NEURO-GFX

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar setup
SETUP_NEURO_GFX_ADVANCED.bat

# Lanzar
python NEURO_GFX_LAUNCHER_V2.py
```

### **Dependencias:**
```
PySide6>=6.6.0
numpy>=1.26.0
mss>=9.0.1
Pillow>=10.1.0
```

---

## 🎮 **Uso**

### **Controles Básicos:**

| Tecla | Acción |
|-------|--------|
| `F1` | Toggle overlay de métricas |
| `F2` | Recargar launcher |
| `F3` | Tomar screenshot |
| `Ctrl+G` | Toggle captura de mouse (control remoto) |
| `O` | Menú de opciones |
| `ESC` | Salir |

### **Control de FPS:**
- `1-9` - Selección directa de preset de FPS
- `↑↓` - Ciclar entre presets de FPS

### **Control de Resolución:**
- `+` - Aumentar resolución
- `-` - Disminuir resolución

### **Lanzamiento Rápido:**
- Lanza Paint, Notepad, Calculator o apps personalizadas
- Detección y captura automática de ventanas

---

## 🏗️ **Arquitectura**

```
NEURO-GFX
├── NEURO_GFX_LAUNCHER_V2.py    # Launcher principal (594 líneas)
├── NeuroGFX/
│   ├── window_capture.py        # Captura directa por HWND
│   ├── neuron_input_mapper.py   # Reenvío de entrada
│   └── advanced_capture.py      # Métricas y detección
├── screenshots/                 # Capturas auto-guardadas
└── Documentación/               # 25+ docs
```

### **Flujo de Captura:**
```
Usuario lanza app (F2)
    ↓
Sistema detecta HWND por PID
    ↓
WindowCapture.set_target(hwnd)
    ↓
PrintWindow captura contenido
    ↓
Conversión BGRA → RGBA
    ↓
QImage renderiza en viewport
    ↓
Visualización en tiempo real
```

### **Flujo de Entrada:**
```
Usuario mueve mouse en viewport
    ↓
mouseMoveEvent captura coordenadas
    ↓
Escalado: Viewport → Ventana
    ↓
NeuronInputMapper.forward_mouse()
    ↓
SendInput envía a Windows
    ↓
App capturada recibe entrada
    ↓
WindowCapture captura cambio
    ↓
Viewport muestra resultado
```

---

## 🤝 **Contribuir**

**¡Necesitamos tu ayuda!** Este proyecto fue construido por un desarrollador solo en 66 días sin experiencia previa en programación. Aquí es donde puedes contribuir:

### **Áreas Prioritarias:**

1. **Captura DirectX** 🔴 ALTA PRIORIDAD
   - Actual: Solo apps GDI (Paint, Notepad)
   - Necesario: Soporte DirectX 9/10/11/12
   - Objetivo: Capturar juegos modernos

2. **Captura de Menús** 🟡 PRIORIDAD MEDIA
   - Actual: Menús contextuales no capturados
   - Necesario: Integración BitBlt con multi-escritorio
   - Objetivo: Captura completa de UI

3. **Optimización de Rendimiento** 🟢 PRIORIDAD BAJA
   - Actual: 30-60 FPS promedio
   - Necesario: Aceleración GPU
   - Objetivo: 144+ FPS estable

Lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

---

## 📊 **Estadísticas del Proyecto**

- **Tiempo de Desarrollo:** 66 días
- **Líneas de Código:** ~2,500
- **Archivos:** 30+
- **Documentación:** 25+ archivos
- **Versión:** 2.1 (Control Remoto)
- **Estado:** Desarrollo Activo

---

## 🎓 **Viaje de Aprendizaje**

Este proyecto representa un viaje increíble:

> **"Hace 66 días, no sabía programar. Hoy, tengo un sistema operativo funcional con captura avanzada de ventanas y control remoto."**
> 
> — CyberEnigma, Creador

**Hitos Clave:**
- Día 1-20: Aprendiendo conceptos básicos de Python
- Día 21-40: Entendiendo Win32 API
- Día 41-60: Construyendo sistemas core
- Día 61-66: Puliendo y documentando

**Prueba de que con determinación y asistencia de IA, todo es posible.**

---

## 🌐 **Parte de NEURO-OS Genesis**

NEURO-GFX es un módulo del ecosistema más grande **NEURO-OS Genesis**:

- **NeuroStore** - Marketplace de arte digital generado por IA
- **NEURO-GFX** - Este proyecto (captura de ventanas)
- **DJ-NEURO-AI™** - Producción musical autónoma
- **Y más...**

**Explora el ecosistema completo:** [NEURO-OS Genesis](https://github.com/cyberenigma-lgtm/Neuro-Os-public)

---

## 📝 **Documentación**

**Documentación completa disponible:**
- [Guía de Instalación](docs/INSTALACION.md)
- [Manual de Usuario](NEURO_VGA_README.md)
- [Referencia API](docs/API_REFERENCE.md)
- [Solución de Problemas](docs/TROUBLESHOOTING.md)
- [Registro de Cambios](CHANGELOG_VGA.md)

---

## 🐛 **Problemas Conocidos**

1. **Menús Contextuales No Capturados**
   - Limitación de la API PrintWindow
   - Solución temporal: Usar app en mismo escritorio
   - Fix en progreso: Integración BitBlt

2. **Juegos DirectX No Soportados**
   - Actual: Solo apps GDI
   - Necesario: D3DShot o similar
   - Se busca ayuda: Expertos en DirectX

3. **Alto Uso de CPU a 240 FPS**
   - Comportamiento esperado
   - Recomendación: Usar 60-90 FPS
   - Optimización planeada

---

## 🏆 **Logros**

- ✅ Captura multi-escritorio funcionando
- ✅ Reenvío completo de entrada
- ✅ Modo control remoto
- ✅ Sistema de cursor personalizado
- ✅ Controles dinámicos
- ✅ Documentación profesional
- ✅ 25+ archivos de documentación
- ✅ Construido en 66 días solo

---

## 💬 **Comunidad**

**Involúcrate:**
- **Issues:** Reporta bugs o solicita características
- **Discussions:** Comparte ideas y haz preguntas
- **Pull Requests:** Contribuye código
- **Star:** Muestra tu apoyo ⭐

**Contacto:**
- **GitHub:** [@cyberenigma-lgtm](https://github.com/cyberenigma-lgtm)
- **Proyecto:** [NEURO-OS Genesis](https://github.com/cyberenigma-lgtm/Neuro-Os-public)

---

## 📜 **Licencia**

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## 🙏 **Agradecimientos**

- **Google Gemini (Antigravity AI)** - Asistencia en desarrollo
- **Microsoft Copilot** - Sugerencias de código
- **Comunidad Python** - Librerías increíbles
- **Documentación Win32 API** - Referencia técnica
- **Tú** - ¡Por revisar este proyecto!

---

## 🚀 **Roadmap**

### **v2.2 (Próximo Lanzamiento)**
- [ ] Soporte de captura DirectX
- [ ] Captura de menús con BitBlt
- [ ] Grabación de video
- [ ] Captura de múltiples ventanas

### **v3.0 (Futuro)**
- [ ] Aceleración GPU
- [ ] Modo Picture-in-Picture
- [ ] Servidor de streaming
- [ ] Automatización con IA

### **v4.0 (Visión)**
- [ ] Soporte multiplataforma
- [ ] Integración en la nube
- [ ] App companion móvil
- [ ] Características empresariales

---

## 💡 **Filosofía**

> **"La única limitación es tu imaginación."**

Este proyecto prueba que:
- No necesitas años de experiencia para construir algo increíble
- La IA puede ser un poderoso compañero de aprendizaje y desarrollo
- La determinación vence al talento
- El código abierto acelera la innovación

**Si yo pude hacerlo en 66 días sin experiencia, imagina lo que podemos hacer juntos.**

---

## 📞 **Soporte**

**¿Necesitas ayuda?**
1. Revisa la [Documentación](docs/)
2. Busca en [Issues](https://github.com/cyberenigma-lgtm/NEURO-GFX/issues)
3. Pregunta en [Discussions](https://github.com/cyberenigma-lgtm/NEURO-GFX/discussions)
4. Crea un nuevo [Issue](https://github.com/cyberenigma-lgtm/NEURO-GFX/issues/new)

---

## ⭐ **Historial de Estrellas**

Si encuentras útil este proyecto, ¡considera darle una estrella! ⭐

Ayuda a otros a descubrir el proyecto y motiva el desarrollo continuo.

---

**🎮 Construido con determinación. Impulsado por imaginación. 🎮**

*NEURO-GFX - Donde la visión se encuentra con el código.*

---

**Última Actualización:** 8 de Diciembre de 2025  
**Versión:** 2.1 (Control Remoto)  
**Estado:** 🟢 Desarrollo Activo
