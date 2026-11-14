#!/usr/bin/env python3
"""Offline cyberpunk security console for fictional system telemetry.

This is a pure local demo. It creates synthetic telemetry and simulates a
text-based access flow; it never connects to real devices or networks.
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
    enabled = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
    GREEN = "\033[32m" if enabled else ""
    CYAN = "\033[36m" if enabled else ""
    YELLOW = "\033[33m" if enabled else ""
    BLUE = "\033[34m" if enabled else ""
    MAGENTA = "\033[35m" if enabled else ""
    RED = "\033[31m" if enabled else ""
    RESET = "\033[0m" if enabled else ""


def make_system(number: int) -> System:
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


def normalize_system_id(raw: str) -> str:
    cleaned = raw.strip().upper()
    if cleaned.isdigit():
        return f"SYSTEM-{int(cleaned):03d}"
    return cleaned


def find_system(choice: str, systems: list[System]) -> System | None:
    target = normalize_system_id(choice)
    for system in systems:
        if system.system_id == target:
            return system
    return None


def print_banner() -> None:
    print("\n\n\n")
    print(f"{Colors.CYAN}")
    print("      ____  _                 _      _            __  __")
    print("     / ___|| |__   ___   ___ | | ___| |_   _____  \\ \\/ /")
    print("     \\___ \\| '_ \\ / _ \\ / _ \\| |/ _ \\ __| |_  / _ \\ \\  / ")
    print("      ___) | | | | (_) | (_) | |  __/ |_  / __/ / /\\ \\ ")
    print("     |____/|_| |_|\\___/ \\___/|_|\\___|\\__| \\___|/_/  \\_\\")
    print(f"{Colors.RESET}")
    print(f"{Colors.YELLOW}LOCAL SECURITY CONSOLE // SYNTHETIC DATA ONLY{Colors.RESET}")
    print("Nessun accesso reale a dispositivi o reti. Demo locale e fittizia.\n")


def print_help() -> None:
    print(f"{Colors.CYAN}COMANDI DISPONIBILI{Colors.RESET}")
    print("  help      mostra la lista dei comandi")
    print("  scan      genera e mostra un nuovo batch di sistemi")
    print("  access X  apre un sistema specifico (es. access 003 o access SYSTEM-003)")
    print("  list      mostra i sistemi attualmente in memoria")
    print("  exit      termina la simulazione")


def print_scan_batch(systems: list[System], interval: float) -> None:
    print(f"\n{Colors.CYAN}TIME     SYSTEM       STATUS       NODE   SIGNAL  PING   CPU  STORAGE{Colors.RESET}")
    print("─" * 73)
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
    print("\n")


def print_access_animation(system: System, step_delay: float) -> None:
    print(f"\n{Colors.MAGENTA}╭── ACCESSO SIMULATO: {system.system_id} ──╮{Colors.RESET}")
    print("│ Nessun dispositivo reale è contattato. │")
    phases = (
        "Preparazione ambiente demo",
        "Analisi del sistema fittizio",
        "Verifica delle credenziali simulate",
        "Controllo delle autorizzazioni",
        "Completamento accesso locale",
    )
    for phase in phases:
        print(f"\n{Colors.BLUE}{phase}...{Colors.RESET}")
        for percent in range(0, 101, 5):
            filled = percent // 10
            bar = "█" * filled + "░" * (10 - filled)
            sys.stdout.write(f"\r[{bar}] {percent:3d}%")
            sys.stdout.flush()
            time.sleep(step_delay)
        print()
    print(f"{Colors.GREEN}\nACCESSO DEMO COMPLETATO — MODO FICTIZIO{Colors.RESET}\n")


def print_details(system: System, step_delay: float) -> None:
    print_access_animation(system, step_delay)
    print(f"{Colors.GREEN}╭── SPECIFICHE FITTIZIE: {system.system_id} ──╮{Colors.RESET}")
    print(f"STATUS:          {system.status}")
    print(f"TYPE:            {system.device_type}")
    print(f"OS:              {system.operating_system}")
    print(f"NODE:            {system.node}")
    print(f"LOCATION:        {system.location}")
    print(f"SIGNAL:          {system.signal}%")
    print(f"PING:            {system.ping}ms")
    print(f"UPTIME:          {system.uptime}")
    print(f"CPU:             {system.cpu}%")
    print(f"STORAGE USED:    {system.storage}%")
    print(f"MEMORY:          {system.memory}")
    print(f"CLEARANCE:       LEVEL-{system.clearance}")
    print(f"LOG:             {system.log}")
    print(f"{Colors.YELLOW}Questi valori sono inventati e visualizzati solo in simulazione.{Colors.RESET}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Console cyberpunk per telemetria fittizia")
    parser.add_argument("--interval", type=float, default=0.5, help="secondi tra le righe dello stream")
    parser.add_argument("--animation-step", type=float, default=0.08, help="secondi per ogni passo dell'animazione")
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval deve essere maggiore di zero")
    if args.animation_step <= 0:
        parser.error("--animation-step deve essere maggiore di zero")
    return args


def main() -> None:
    args = parse_args()
    print_banner()
    print_help()

    next_number = 1
    current_batch: list[System] = []

    while True:
        try:
            command = input("\nsecurity-console> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSessione terminata.")
            break

        if not command:
            continue

        parts = command.split()
        action = parts[0].lower()

        if action in ("help", "?"):
            print_help()

        elif action in ("scan", "s"):
            current_batch = [
                make_system(number)
                for number in range(next_number, next_number + 15)
            ]
            next_number += 15
            print_scan_batch(current_batch, args.interval)

        elif action in ("list", "ls"):
            if not current_batch:
                print(f"{Colors.RED}Nessun batch attivo. Digita 'scan' prima.{Colors.RESET}")
            else:
                print(f"{Colors.CYAN}BATCH ATTIVO:{Colors.RESET}")
                for system in current_batch:
                    print(f"  {system.system_id} | {system.status} | {system.node} | {system.signal}%")

        elif action in ("access", "a"):
            if len(parts) < 2:
                print(f"{Colors.RED}Uso: access 003 oppure access SYSTEM-003{Colors.RESET}")
                continue
            if not current_batch:
                print(f"{Colors.RED}Nessun batch attivo. Digita 'scan' prima.{Colors.RESET}")
                continue
            target = " ".join(parts[1:])
            system = find_system(target, current_batch)
            if system is None:
                print(f"{Colors.RED}Sistema non presente nel batch attuale.{Colors.RESET}")
            else:
                print_details(system, args.animation_step)

        elif action in ("exit", "quit", "q"):
            print("\nChiusura simulazione...")
            break

        else:
            print(f"{Colors.RED}Comando non riconosciuto. Digita 'help'.{Colors.RESET}")

    print("\nSimulazione terminata.")


if __name__ == "__main__":
    main()
