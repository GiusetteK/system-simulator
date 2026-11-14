# System Simulator

A small offline terminal demo that generates synthetic telemetry for fictional systems.

## Description
The project displays fictional system records, including status, operating system, node, signal, ping, uptime, CPU, storage, memory, and demo logs. All values are randomly generated locally.

**This is only a simulation.** It does not scan networks, connect to nearby devices, or access real systems. The demo-entry animation is purely text-based and local.

## Requirements
- Python 3.10 or newer
- macOS, Linux, or Windows with Python installed

## Run it
```bash
python3 scripts/system-simulator.py
```

For a faster stream:

```bash
python3 scripts/system-simulator.py --interval 0.2
```

## Controls
- Enter an ID such as `SYSTEM-003` or `3` to view synthetic details and the simulated access animation.
- Press `Enter` to continue with another batch.
- Enter `R` to regenerate the data.
- Enter `Q` or press `Ctrl+C` to quit.

## License
MIT
