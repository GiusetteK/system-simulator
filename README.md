# System Simulator

An offline terminal console that displays locally generated telemetry records for fictional systems. It does not scan networks or connect to real devices.

## Requirements
- Python 3.10 or later
- No external dependencies

## Run
From the repository root:

```bash
python3 scripts/system-simulator.py
```

The interface is in English. There is no language prompt or language-switch command.

To adjust scan and animation speed:

```bash
python3 scripts/system-simulator.py --interval 0.2 --animation-step 0.08
```

## Commands
Type `help` in the console for detailed descriptions and examples.

| Command | Description |
| --- | --- |
| `scan` | Generates a random group of 5 to 15 records. |
| `list` | Lists the latest group. |
| `access 003` | Displays a report for a record in the latest group. |
| `status` | Summarizes statuses, average CPU and signal. |
| `log` | Shows recent events from the current session. |
| `clear` | Clears and redraws the console. |
| `exit` | Closes the program. |

## License
MIT. See [LICENSE](LICENSE).
