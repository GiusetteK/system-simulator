# System Simulator

A small offline terminal demo that generates synthetic telemetry for fictional systems.

## Description
The project displays fictional system records, including status, operating system, node, signal, ping, uptime, CPU, storage, memory, and demo logs. All values are randomly generated locally.

**This is only a simulation.** It does not scan networks, connect to nearby devices, or access real systems. The "demo entry" is just a text animation and does not access anything.

## Requirements
Choose either implementation:

- **Python version:** Python 3.10 or newer; works on macOS, Linux, and Windows. No third-party packages are needed.
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

To change the delay between telemetry lines, pass `--interval` in seconds, for example:

```bash
python3 scripts/system-simulator.py --interval 0.2
```

## Run the zsh version
On macOS or Linux:

```bash
zsh scripts/system-simulator.zsh
```

## Controls for the Python version
The simulator prints a batch of 15 fictional systems, then waits for a command:

- Enter an ID such as `SYSTEM-003` or its number, such as `3`, to view its synthetic specifications and a theatrical demo-entry animation.
- Press **Enter** to continue with another telemetry batch.
- Enter `R` to generate a fresh batch.
- Enter `Q` to quit; **Ctrl+C** also stops the program.

## License
MIT. See [LICENSE](LICENSE).
