from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psutil
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Para calcular velocidad en tiempo real
_last_net = {}
_last_time = {}

def get_temperatures():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        result = {}
        for name, entries in temps.items():
            result[name] = [
                {"label": e.label or "core", "current": e.current, "high": e.high, "critical": e.critical}
                for e in entries
            ]
        return result
    except Exception:
        return None

def get_network():
    global _last_net, _last_time
    now = time.time()
    interfaces = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)
    result = {}

    for iface, stats in interfaces.items():
        if iface not in io_counters:
            continue

        io = io_counters[iface]
        speed_up = 0.0
        speed_down = 0.0

        if iface in _last_net and iface in _last_time:
            elapsed = now - _last_time[iface]
            if elapsed > 0:
                speed_up   = (io.bytes_sent - _last_net[iface]["bytes_sent"]) / elapsed
                speed_down = (io.bytes_recv - _last_net[iface]["bytes_recv"]) / elapsed

        _last_net[iface] = {
            "bytes_sent": io.bytes_sent,
            "bytes_recv": io.bytes_recv,
        }
        _last_time[iface] = now

        result[iface] = {
            "is_up":        stats.isup,
            "speed_mbps":   stats.speed,
            "bytes_sent":   io.bytes_sent,
            "bytes_recv":   io.bytes_recv,
            "packets_sent": io.packets_sent,
            "packets_recv": io.packets_recv,
            "errin":        io.errin,
            "errout":       io.errout,
            "dropin":       io.dropin,
            "dropout":      io.dropout,
            "speed_up":     max(0, speed_up),
            "speed_down":   max(0, speed_down),
        }

    return result

def get_connections_summary():
    try:
        conns = psutil.net_connections(kind="all")
        summary = {}
        for c in conns:
            kind = c.type.name if hasattr(c.type, 'name') else str(c.type)
            summary[kind] = summary.get(kind, 0) + 1
        return summary
    except Exception:
        return {}

@app.get("/metrics")
def get_metrics():
    return {
        "cpu":   psutil.cpu_percent(interval=1),
        "ram":   psutil.virtual_memory()._asdict(),
        "disk":  psutil.disk_usage("/")._asdict(),
        "net":   get_network(),
        "temps": get_temperatures(),
        "protocols": get_connections_summary(),
    }