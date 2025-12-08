# 🎮 GUÍA DE PRUEBA: INPUT FORWARDING

## 📋 SISTEMA DE CONTROL REMOTO ACTIVO

El sistema NEURO-OS VGA™ V2.1 ahora incluye **input forwarding completo** que te permite controlar aplicaciones capturadas directamente desde el viewport.

---

## ✅ **CARACTERÍSTICAS ACTIVAS**

### **🖱️ Mouse Forwarding**
- ✅ **Movimiento** - El cursor se mueve en la app capturada
- ✅ **Click izquierdo** - Interacción con elementos
- ✅ **Click derecho** - Menús contextuales
- ✅ **Click medio** - Scroll/acciones especiales
- ✅ **Rueda del mouse** - Scroll vertical

### **⌨️ Keyboard Forwarding**
- ✅ **Letras A-Z** - Escritura de texto
- ✅ **Números 0-9** - Entrada numérica
- ✅ **Teclas especiales** - Enter, Esc, Tab, Backspace
- ✅ **Modificadores** - Shift, Ctrl, Alt
- ✅ **Flechas** - Navegación
- ✅ **Teclas F1-F12** - Funciones (excepto las reservadas del sistema)

### **🎯 Scaling Automático**
- ✅ **Coordenadas mapeadas** - Viewport → Ventana capturada
- ✅ **Precisión ajustada** - Funciona con diferentes resoluciones
- ✅ **Modo híbrido** - SendInput + PostMessage

---

## 🧪 **PRUEBAS SUGERIDAS**

### **Test 1: Control de Paint** 🎨

1. **Lanzar Paint**
   - F2 para reload
   - Click en "🎨 PAINT"
   - Esperar captura

2. **Probar Mouse**
   - Mover cursor sobre viewport
   - Click en herramienta "Pincel"
   - Dibujar en el lienzo
   - Click derecho para menú

3. **Probar Teclado**
   - Seleccionar herramienta "Texto" (A)
   - Click en lienzo
   - Escribir "NEURO-OS VGA"
   - Presionar Enter

4. **Verificar**
   - ✅ El dibujo aparece en Paint
   - ✅ El texto se escribe correctamente
   - ✅ Los menús responden

---

### **Test 2: Control de Notepad** 📝

1. **Lanzar Notepad**
   - F2 para reload
   - Click en "📝 NOTEPAD"

2. **Escribir Texto**
   ```
   NEURO-OS VGA™ V2.1
   Input Forwarding Test
   Mouse + Keyboard Working!
   ```

3. **Usar Atajos**
   - Ctrl+A (Seleccionar todo)
   - Ctrl+C (Copiar)
   - Ctrl+V (Pegar)

4. **Guardar**
   - Ctrl+S
   - Escribir nombre
   - Enter

---

### **Test 3: Control de Calculator** 🔢

1. **Lanzar Calculator**
   - F2 para reload
   - Click en "🔢 CALCULATOR"

2. **Usar Mouse**
   - Click en números
   - Click en operadores
   - Click en "="

3. **Usar Teclado**
   - Escribir: 123 + 456
   - Presionar Enter
   - Verificar resultado: 579

---

## 🎯 **TECLAS RESERVADAS DEL SISTEMA**

**Estas teclas NO se envían a la app (son para el viewport):**

| Tecla | Acción |
|-------|--------|
| **F1** | Toggle métricas |
| **F2** | Reload launcher |
| **F3** | Screenshot |
| **O** | Menú de opciones |
| **ESC** | Cerrar sistema |
| **1-9** | FPS presets |
| **+/-** | Resolución |
| **↑↓** | FPS cycle |

**Todas las demás teclas se envían a la aplicación capturada.**

---

## 🔧 **CÓMO FUNCIONA**

### **Flujo de Input:**

```
1. Usuario mueve mouse en viewport
   ↓
2. Evento capturado por Qt (mouseMoveEvent)
   ↓
3. Coordenadas convertidas: Viewport → Ventana
   ↓
4. NeuronInputMapper.forward_mouse()
   ↓
5. SendInput() envía evento a Windows
   ↓
6. Aplicación capturada recibe el evento
   ↓
7. Aplicación responde (dibujo, texto, etc.)
   ↓
8. WindowCapture captura el resultado
   ↓
9. Viewport muestra el cambio
```

### **Scaling de Coordenadas:**

```python
# Ejemplo: Viewport 1280x720 → Paint 800x600
viewport_x = 640  # Centro del viewport
viewport_y = 360

# Conversión automática:
paint_x = 640 * (800 / 1280) = 400  # Centro de Paint
paint_y = 360 * (600 / 720) = 300
```

---

## 📊 **MODOS DE INPUT**

El sistema usa **modo HYBRID** por defecto:

### **SendInput (Hardware Level)**
- ✅ Máxima compatibilidad
- ✅ Funciona con juegos DirectX
- ✅ Eventos a nivel de sistema
- ⚠️ Mueve el cursor real

### **PostMessage (Software Level)**
- ✅ No mueve cursor real
- ✅ Más rápido
- ⚠️ Algunas apps lo ignoran

### **HYBRID (Recomendado)**
- ✅ Usa SendInput para máxima compatibilidad
- ✅ Fallback a PostMessage si es necesario
- ✅ Mejor de ambos mundos

---

## 🐛 **SOLUCIÓN DE PROBLEMAS**

### **Problema: Mouse no responde**

**Solución:**
1. Verificar que la ventana está capturada (HWND visible)
2. Verificar mensaje de scaling en consola
3. Probar con otra aplicación
4. Verificar que no estás en el menú de opciones (O)

### **Problema: Coordenadas incorrectas**

**Solución:**
1. Verificar dimensiones en consola:
   ```
   📐 Input scaling: Viewport 1280x720 → Window 800x600
   ```
2. Si están mal, relanzar la app (F2)
3. Verificar que la ventana no cambió de tamaño

### **Problema: Teclado no escribe**

**Solución:**
1. Verificar que no estás usando teclas reservadas
2. Probar con Notepad (más simple)
3. Verificar que la app tiene foco

### **Problema: Clicks no funcionan**

**Solución:**
1. Verificar que el cursor está sobre el viewport
2. Probar con click derecho también
3. Verificar que la app no está minimizada

---

## 🎮 **CASOS DE USO AVANZADOS**

### **1. Control Remoto Multi-Escritorio**
```
Escritorio 1: Viewport + Control
Escritorio 2: Paint trabajando
→ Dibujas desde Escritorio 1
→ Paint en Escritorio 2 responde
```

### **2. Automatización**
```
→ Captura app en background
→ Script envía inputs automáticos
→ App responde sin intervención
```

### **3. Testing de UI**
```
→ Captura app a testear
→ Simula interacciones de usuario
→ Toma screenshots de cada estado
```

---

## 📸 **DOCUMENTAR TUS PRUEBAS**

1. **Captura estado inicial** - F3
2. **Realiza interacción** - Mouse/Teclado
3. **Captura resultado** - F3
4. **Compara screenshots** - Verifica cambios

---

## ✅ **CHECKLIST DE VALIDACIÓN**

- [ ] Mouse se mueve en la app
- [ ] Click izquierdo funciona
- [ ] Click derecho funciona
- [ ] Teclado escribe texto
- [ ] Atajos de teclado funcionan
- [ ] Coordenadas son precisas
- [ ] Funciona en otro escritorio
- [ ] Screenshots capturan cambios

---

## 🏆 **ESTADO ACTUAL**

```
✅ Input Forwarding: ACTIVO
✅ Mouse Events: CONFIGURADO
✅ Keyboard Events: CONFIGURADO
✅ Scaling: AUTOMÁTICO
✅ Modo: HYBRID (SendInput + PostMessage)
✅ Listo para usar
```

---

**🎮 El sistema está listo para control completo de aplicaciones capturadas 🎮**

*Guía de Input Forwarding - NEURO-OS VGA™ V2.1*
