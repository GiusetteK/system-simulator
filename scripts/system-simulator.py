#!/usr/bin/env python3
"""Offline terminal demo that generates telemetry for fictional systems.

This program uses synthetic data only. It does not scan networks, connect to,
or access real devices.
"""

from __future__ import annotations

import os
import random
import sys
import time
from dataclasses import dataclass


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
    """ANSI colors, disabled automatically when output is redirected."""

    enabled = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
    GREEN = "\033[32m" if enabled else ""
    CYAN = "\033[36m" if enabled else ""
    YELLOW = "\033[33m" if enabled else ""
    BLUE = "\033[34m" if enabled else ""
    MAGENTA = "\033[35m" if enabled else ""
    RED = "\033[31m" if enabled else ""
    RESET = "\033[0m" if enabled else ""


def make_system(number: int) -> System:
    """Create a fictional system record; no machine or network is queried."""
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


def clear_screen() -> None:
    """Clear the screen on common terminals; avoid escape codes when redirected."""
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    print(f"{Colors.CYAN}SIMULATORE DI TELEMETRIA LOCALE{Colors.RESET}")
    print(f"{Colors.YELLOW}Demo: dati sintetici e totalmente locali.{Colors.RESET}")
    print("Nessuna scansione o connessione di rete viene eseguita.\n")


def print_dashboard(systems: list[System]) -> None:
    print_banner()
    for system in systems:
        print(
            f"{Colors.GREEN}{system.system_id}{Colors.RESET} "
            f"{Colors.YELLOW}{system.status}{Colors.RESET} | "
            f"NODE: {system.node} | SIGNAL: {system.signal}% | "
            f"PING: {system.ping}ms"
        )


def print_details(system: System) -> None:
    print(f"\n{Colors.GREEN}{system.system_id}{Colors.RESET}")
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

    if system.status == "ENCRYPTED":
        print(f"\n{Colors.MAGENTA}ACCESSO DEMO{Colors.RESET}")
        for message in (
            "Inizializzazione ambiente demo...",
            "Analisi simulata del sistema...",
            "Controllo dimostrativo completato.",
        ):
            print(message)
            time.sleep(0.25)
        print(f"{Colors.GREEN}ACCESSO DEMO COMPLETATO{Colors.RESET}")


def find_system(choice: str, systems: list[System]) -> System | None:
    """Accept either SYSTEM-003 or its numeric shorthand, 3."""
    normalized = choice.strip().upper()
    if normalized.isdigit():
        normalized = f"SYSTEM-{int(normalized):03d}"
    return next((system for system in systems if system.system_id == normalized), None)


def main() -> None:
    systems = [make_system(number) for number in range(1, 16)]

    while True:
        clear_screen()
        print_dashboard(systems)
        try:
            choice = input("\nScegli un ID (es. SYSTEM-003 o 3), R per rigenerare, Q per uscire: ")
        except (EOFError, KeyboardInterrupt):
            print("\nSimulazione terminata.")
            return

        if choice.strip().upper() == "Q":
            break
        if choice.strip().upper() == "R":
            systems = [make_system(number) for number in range(1, 16)]
            continue

        system = find_system(choice, systems)
        if system is None:
            print(f"\n{Colors.RED}Sistema non riconosciuto. Scegline uno dalla lista.{Colors.RESET}")
        else:
            print_details(system)

        try:
            input("\nPremi Invio per continuare...")
        except (EOFError, KeyboardInterrupt):
            break

    print("\nSimulazione terminata.")


if __name__ == "__main__":
    main()
