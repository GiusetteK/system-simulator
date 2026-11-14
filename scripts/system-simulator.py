#!/usr/bin/env python3
"""Offline terminal demo with a continuous stream of fictional telemetry.

All records and the simulated system-entry animation are fictional. This
program does not scan networks, connect to, or access real devices.
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
    MAGENTA = "\033[35m" if enabled else ""
    RED = "\033[31m" if enabled else ""
    RESET = "\033[0m" if enabled else ""


def make_system(number: int) -> System:
    """Create fictional telemetry; no machine or network is queried."""
    return System(
        system_id=f"SYSTEM-{number:03d}",
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
    # A little breathing room makes the launch clearer in the terminal.
    print("\n\n")
    print(f"{Colors.CYAN}SIMULATORE DI TELEMETRIA LOCALE{Colors.RESET}")
    print(f"{Colors.YELLOW}Flusso continuo di dati sintetici e locali.{Colors.RESET}")
    print("Nessuna scansione o connessione di rete viene eseguita.")
    print(f"Intervallo: {interval:g} s | Ctrl+C interrompe il programma.\n")


def print_batch(systems: list[System], interval: float) -> None:
    print("TIME     SYSTEM       STATUS       NODE   SIGNAL  PING   CPU  STORAGE")
    print("-" * 73)
    for system in systems:
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_color = Colors.GREEN if system.status == "CONNECTED" else Colors.YELLOW
        print(
            f"{Colors.BLUE}{timestamp}{Colors.RESET}  "
            f"{Colors.CYAN}{system.system_id:<12}{Colors.RESET} "
            f"{status_color}{system.status:<12}{Colors.RESET} "
            f"{system.node:<6} {system.signal:>3}%   {system.ping:>3}ms "
            f"{system.cpu:>3}%  {system.storage:>3}%",
            flush=True,
        )
        time.sleep(interval)
    print()


def simulate_demo_entry(system: System) -> None:
    """Show a theatrical, local-only animation; it performs no access."""
    print(f"\n{Colors.MAGENTA}INGRESSO SIMULATO — SOLO DEMO{Colors.RESET}")
    print(f"Avvio ambiente fittizio per {system.system_id}...")
    for percent in range(0, 101, 10):
        bar = "#" * (percent // 10) + "." * (10 - percent // 10)
        sys.stdout.write(f"\rPreparazione demo [{bar}] {percent:3d}%")
        sys.stdout.flush()
        time.sleep(0.08)
    print("\nSessione dimostrativa avviata. Nessun sistema reale è stato contattato.\n")


def print_details(system: System) -> None:
    simulate_demo_entry(system)
    print(f"{Colors.GREEN}SPECIFICHE FITTIZIE: {system.system_id}{Colors.RESET}")
    print(f"STATUS: {system.status}")
    print(f"TYPE: {system.device_type}")
    print(f"OS: {system.operating_system}")
    print(f"NODE: {system.node}")
    print(f"LOCATION: {system.location}")
    print(f"SIGNAL: {system.signal}%")
    print(f"PING: {system.ping}ms")
    print(f"UPTIME: {system.uptime}")
    print(f"CPU: {system.cpu}%")
    print(f"STORAGE USED: {system.storage}%")
    print(f"MEMORY: {system.memory}")
    print(f"CLEARANCE DEMO: LEVEL-{system.clearance}")
    print(f"LOG DEMO: {system.log}")


def find_system(choice: str, systems: list[System]) -> System | None:
    """Accept SYSTEM-003 or its numeric shorthand, 3."""
    normalized = choice.strip().upper()
    if normalized.isdigit():
        normalized = f"SYSTEM-{int(normalized):03d}"
    return next((system for system in systems if system.system_id == normalized), None)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Flusso continuo di telemetria fittizia con dettagli interattivi."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="secondi tra le righe del flusso (default: 0.5)",
    )
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval deve essere maggiore di zero")
    return args


def main() -> None:
    args = parse_args()
    print_banner(args.interval)

    try:
        while True:
            # Each batch contains 15 fictional systems, then offers interaction.
            systems = [make_system(number) for number in range(1, 16)]
            print_batch(systems, args.interval)
            choice = input(
                "ID/numero per specifiche e ingresso demo, Invio per continuare, "
                "R per nuovi dati, Q per uscire: "
            ).strip()

            if choice.upper() == "Q":
                break
            if choice.upper() == "R" or not choice:
                continue

            system = find_system(choice, systems)
            if system is None:
                print(f"\n{Colors.RED}Sistema non riconosciuto.{Colors.RESET}")
            else:
                print_details(system)
            input("\nPremi Invio per riprendere il flusso...")
            print("\n")
    except (KeyboardInterrupt, EOFError, BrokenPipeError):
        pass

    print("\nSimulazione terminata.")


if __name__ == "__main__":
    main()
