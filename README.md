# 🖥️ SysMonitor — Podman

Dashboard web en tiempo real para monitorear los recursos del sistema, construido con **FastAPI**, **Nginx** y **Podman**.

---

## 📸 Vista previa

> Dashboard con métricas de CPU, RAM, Disco, Red por interfaz, Protocolos y Temperatura actualizándose cada 2 segundos.

---

## 🧱 Arquitectura

```
sysmonitor-podman/
├── backend/
│   ├── Containerfile       # Imagen Python + FastAPI
│   ├── requirements.txt    # Dependencias Python
│   └── main.py             # API REST con métricas del sistema
├── frontend/
│   ├── Containerfile       # Imagen Nginx
│   └── index.html          # Dashboard HTML/JS con Chart.js
├── podman-compose.yml      # Orquestación de contenedores
└── README.md
```

```
┌─────────────────────────────────────┐
│           Podman (rootless)         │
│                                     │
│  ┌─────────────┐  ┌──────────────┐  │
│  │   Backend   │  │   Frontend   │  │
│  │  FastAPI    │◄─│  Nginx       │  │
│  │  :8000      │  │  :8080       │  │
│  └──────┬──────┘  └──────────────┘  │
│         │                           │
└─────────┼───────────────────────────┘
          │ psutil lee métricas
          ▼
    🖥️ Sistema Host
```

---

## 🚀 Requisitos

| Herramienta | Versión mínima | Instalación |
|---|---|---|
| Podman | 4.0+ | `sudo apt install podman` |
| podman-compose | 1.0+ | `sudo apt install podman-compose` |

> ✅ No requiere Docker ni permisos root para correr los contenedores.

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/PatCard/sysmonitor-podman.git
cd sysmonitor-podman
```

### 2. Construir y levantar los contenedores

```bash
podman-compose up --build -d
```

### 3. Abrir el dashboard

Abre tu navegador en:

```
http://localhost:8080
```

---

## 📊 Métricas disponibles

### 🔵 CPU
- Porcentaje de uso en tiempo real
- Gráfica histórica de los últimos 20 puntos
- Color de alerta: 🟡 >70% / 🔴 >90%

### 🟢 RAM
- Porcentaje de uso
- GB usados vs total disponible
- Color de alerta: 🟡 >70% / 🔴 >90%

### 💾 Disco
- Porcentaje de uso de la partición raíz `/`
- GB usados vs total disponible
- Color de alerta: 🟡 >70% / 🔴 >90%

### 🌐 Red — por interfaz
- Estado UP/DOWN de cada interfaz
- Velocidad en tiempo real ⬆️ ⬇️ (B/s, KB/s, MB/s automático)
- Total de bytes enviados y recibidos (B, KB, MB, GB automático)
- Paquetes enviados y recibidos
- Errores y paquetes descartados (solo si existen)

### 📡 Protocolos activos
- Conteo de conexiones activas agrupadas por tipo (TCP, UDP, etc.)

### 🌡️ Temperatura
- Lectura de todos los sensores disponibles (`acpitz`, `coretemp`, etc.)
- Temperatura por núcleo
- Color de alerta: 🟡 >85% del umbral alto / 🔴 temperatura crítica

---

## 🛠️ Comandos útiles

```bash
# Ver contenedores corriendo
podman ps

# Ver logs del backend
podman logs sysmonitor-backend

# Ver logs del frontend
podman logs sysmonitor-frontend

# Ver logs en tiempo real
podman logs -f sysmonitor-backend

# Detener los contenedores
podman-compose down

# Reiniciar
podman-compose restart

# Reconstruir después de cambios
podman-compose up --build -d
```

---

## 🔌 API REST

El backend expone un único endpoint:

### `GET /metrics`

```
http://localhost:8000/metrics
```

**Respuesta de ejemplo:**

```json
{
  "cpu": 12.5,
  "ram": {
    "total": 8268513280,
    "used": 1821696000,
    "percent": 22.7
  },
  "disk": {
    "total": 115966787584,
    "used": 51432693760,
    "percent": 46.6
  },
  "net": {
    "eth0": {
      "is_up": true,
      "bytes_sent": 1024,
      "bytes_recv": 3400,
      "packets_sent": 13,
      "packets_recv": 43,
      "speed_up": 512.0,
      "speed_down": 1024.0,
      "errin": 0,
      "errout": 0,
      "dropin": 0,
      "dropout": 0
    }
  },
  "temps": {
    "coretemp": [
      { "label": "Core 0", "current": 39.0, "high": 80.0, "critical": 100.0 }
    ]
  },
  "protocols": {
    "SOCK_STREAM": 6
  }
}
```

---

## 🐳 ¿Por qué Podman y no Docker?

| | Podman | Docker |
|---|---|---|
| Daemon | ❌ No necesita | ✅ Requiere `dockerd` |
| Rootless | ✅ Nativo | ⚠️ Limitado |
| Pods nativos | ✅ Sí | ❌ No |
| Seguridad | ✅ Mayor aislamiento | ⚠️ Root por defecto |
| Compatible OCI | ✅ Sí | ✅ Sí |

---

## 📁 Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3.11, FastAPI, psutil, uvicorn |
| Frontend | HTML5, CSS3, JavaScript, Chart.js |
| Servidor web | Nginx Alpine |
| Contenedores | Podman (rootless) |
| Orquestación | podman-compose |

---

## 👤 Autor

**Patricio** — [@PatCard](https://github.com/PatCard)

---

## 📄 Licencia

MIT — libre para usar, modificar y distribuir.