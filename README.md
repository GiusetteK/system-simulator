# System Simulator

A small offline terminal demo that generates synthetic telemetry for fictional systems.

## Description
The project displays fictional system records, including status, operating system, node, signal, ping, uptime, CPU, storage, memory, and demo logs. All values are randomly generated locally.

**This is only a simulation.** It does not scan networks, connect to nearby devices, or access real systems.

## Requirements
Choose either implementation:

- **Python version:** Python 3.9 or newer; works on macOS, Linux, and Windows. No third-party packages are needed.
- **zsh version:** zsh; works on macOS and Linux. Windows users can run it through WSL with zsh installed.

## Run the Python version (recommended for cross-platform use)
From the repository root:

```bash
python3 scripts/system-simulator.py
```

On Windows, use:

```powershell
py scripts/system-simulator.py
```

If `python3` or `py` is not recognized, install Python 3 from [python.org](https://www.python.org/downloads/) and enable the option to add Python to PATH during installation.

## Run the zsh version
On macOS or Linux:

```bash
zsh scripts/system-simulator.zsh
```

You can also make it executable and run it directly:

```bash
chmod +x scripts/system-simulator.zsh
./scripts/system-simulator.zsh
```

## Controls
- Enter an ID such as `SYSTEM-003` or its number, such as `3`, to show details.
- Enter `R` to generate a new set of fictional systems.
- Enter `Q` to quit.

## License
MIT. See [LICENSE](LICENSE).
