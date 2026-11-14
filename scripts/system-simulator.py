#!/usr/bin/env python3
"""Offline terminal demo that continuously prints fictional system telemetry.

This program uses synthetic data only. It does not scan networks, connect to,
or access real devices. Press Ctrl+C to stop the stream.
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import time
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class System:
    system_id: str
    status: str
    device_type: str
    operating_system: str
    node: str
    location: str
    signal: int
    ping: int
    uptime: str
    cpu: int
    storage: int
    memory: str
    clearance: int
    log: str


STATUSES = ("CONNECTED", "SCANNING", "ENCRYPTED")
DEVICE_TYPES = ("LAPTOP", "WORKSTATION", "SERVER")
OPERATING_SYSTEMS = ("OS-ALPHA", "OS-BETA", "OS-GAMMA")
NODES = ("NORTH", "EAST", "WEST", "SOUTH")
MEMORIES = ("8 GB", "16 GB", "32 GB")
LOGS = (
    "Handshake simulato",
    "Sincronizzazione completata",
    "Controllo di routine superato",
    "Pacchetto demo ricevuto",
)


class Colors:
    """ANSI colors, disabled when output is redirected or NO_COLOR is set."""

    enabled = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
    GREEN = "\033[32m" if enabled else ""
    CYAN = "\033[36m" if enabled else ""
    YELLOW = "\033[33m" if enabled else ""
    BLUE = "\033[34m" if enabled else ""
    RESET = "\033[0m" if enabled else ""


def make_system(number: int) -> System:
    """Create a fictional system record; no machine or network is queried."""
    return System(
        system_id=f"SYSTEM-{number:06d}",
        status=random.choice(STATUSES),
        device_type=random.choice(DEVICE_TYPES),
        operating_system=random.choice(OPERATING_SYSTEMS),
        node=random.choice(NODES),
        location=f"SECTOR-{random.randint(1, 12):02d}",
        signal=random.randint(55, 99),
        ping=random.randint(12, 180),
        uptime=f"{random.randint(1, 240)}h {random.randint(0, 59)}m",
        cpu=random.randint(5, 95),
        storage=random.randint(10, 90),
        memory=random.choice(MEMORIES),
        clearance=random.randint(1, 5),
        log=random.choice(LOGS),
    )


def print_banner(interval: float) -> None:
    print(f"{Colors.CYAN}SIMULATORE DI TELEMETRIA LOCALE{Colors.RESET}")
    print(f"{Colors.YELLOW}Flusso continuo di dati sintetici e locali.{Colors.RESET}")
    print("Nessuna scansione o connessione di rete viene eseguita.")
    print(f"Intervallo: {interval:g} s | Premi Ctrl+C per uscire.\n")
    print("TIME     SYSTEM         STATUS      NODE   SIGNAL  PING   CPU  STORAGE")
    print("-" * 76)


def print_system(system: System) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_color = Colors.GREEN if system.status == "CONNECTED" else Colors.YELLOW
    print(
        f"{Colors.BLUE}{timestamp}{Colors.RESET}  "
        f"{Colors.CYAN}{system.system_id:<14}{Colors.RESET} "
        f"{status_color}{system.status:<11}{Colors.RESET} "
        f"{system.node:<6} {system.signal:>3}%   {system.ping:>3}ms "
        f"{system.cpu:>3}%  {system.storage:>3}%",
        flush=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mostra un flusso continuo di telemetria fittizia."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="secondi tra una riga e la successiva (default: 0.5)",
    )
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval deve essere maggiore di zero")
    return args


def main() -> None:
    args = parse_args()
    print_banner(args.interval)

    number = 1
    try:
        while True:
            print_system(make_system(number))
            number += 1
            time.sleep(args.interval)
    except (KeyboardInterrupt, BrokenPipeError):
        print("\nSimulazione terminata.")


if __name__ == "__main__":
    main()
