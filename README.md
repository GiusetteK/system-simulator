# System Simulator

A simple offline terminal demo that generates synthetic telemetry for fictional systems.

## Description
This project is a local simulation of a system dashboard. It creates fake device data such as:
- status
- OS information
- node placement
- signal strength
- ping time
- uptime
- CPU usage
- storage usage
- memory and clearance level
- synthetic log messages

The script is intentionally offline and does not connect to actual devices or networks. It is designed as a playful terminal demo and a good starting point for a first GitHub repository.

## Requirements
- macOS
- zsh
- terminal with color support

## Run it
```bash
chmod +x scripts/system-simulator.zsh
./scripts/system-simulator.zsh
```

## Features
- randomized fictional systems
- dashboard view with real-time-style output
- detailed per-system inspection
- demo access animation for encrypted statuses
- no external dependencies

## Notes
This is a simulator only. It does not scan nearby devices, access real machines, or interact with networks.

## License
MIT
