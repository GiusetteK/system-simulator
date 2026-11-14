#!/usr/bin/env python3
"""Console offline con dati sintetici per sistemi immaginari."""

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
    "Handshake generato",
    "Sincronizzazione completata",
    "Controllo di routine superato",
    "Pacchetto dati ricevuto",
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
    """Crea un record casuale; non interroga reti o dispositivi."""
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


def timestamp() -> str:
    return datetime.now().strftime("%H:%M:%S")


def record_event(events: list[str], message: str) -> None:
    events.append(f"[{timestamp()}] {message}")


def normalize_system_id(raw: str) -> str:
    value = raw.strip().upper()
    return f"SYSTEM-{int(value):03d}" if value.isdigit() else value


def find_system(choice: str, systems: list[System]) -> System | None:
    target = normalize_system_id(choice)
    return next((system for system in systems if system.system_id == target), None)


def clear_screen() -> None:
    """Pulisce il terminale interattivo, senza emettere codici in output reindirizzato."""
    if sys.stdout.isatty():
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def print_banner() -> None:
    print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════╗")
    print("║                 SYSTEM CONSOLE                      ║")
    print("║                TELEMETRY DASHBOARD                  ║")
    print(f"╚══════════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"{Colors.BLUE}OFFLINE CONSOLE // DATI GENERATI LOCALMENTE{Colors.RESET}")
    print("Digita 'help' per la guida ai comandi e gli esempi.\n")


def print_help() -> None:
    print(f"{Colors.CYAN}GUIDA AI COMANDI{Colors.RESET}")
    print("I dati mostrati sono generati localmente: i comandi non interrogano reti o dispositivi.\n")
    print("  help  (o ?)\n      Mostra questa guida. Esempio: help")
    print("\n  scan  (o s)\n      Crea un nuovo gruppo casuale da 5 a 15 sistemi e ne mostra i dati principali.")
    print("      Ogni gruppo riceve nuovi ID in sequenza; ad esempio, dopo SYSTEM-015\n      il gruppo successivo riparte da SYSTEM-016. Esempio: scan")
    print("\n  list  (o ls)\n      Elenca gli ID e le informazioni sintetiche del gruppo creato con l'ultimo scan.\n      Se non hai ancora eseguito scan, prima usa quel comando. Esempio: list")
    print("\n  access ID  (o a ID)\n      Mostra il report completo di un sistema presente nell'ultimo gruppo.\n      Puoi indicare il numero o l'ID: access 003 oppure access SYSTEM-003.\n      L'animazione è solo visiva e non apre connessioni.")
    print("\n  status\n      Riassume quanti sistemi del gruppo sono CONNECTED, SCANNING o ENCRYPTED,\n      e calcola le medie di CPU e segnale. Esempio: status")
    print("\n  log\n      Mostra gli ultimi 20 eventi registrati durante questa sessione, ad esempio\n      la creazione di un gruppo o la visualizzazione di un report. Esempio: log")
    print("\n  clear\n      Pulisce il terminale e mostra nuovamente l'intestazione. Esempio: clear")
    print("\n  exit  (oppure quit o q)\n      Termina il programma. Esempio: exit\n")


def print_scan_batch(systems: list[System], interval: float) -> None:
    print(f"\n{Colors.CYAN}ORA      SYSTEM       STATUS       NODE   SIGNAL  PING   CPU  STORAGE{Colors.RESET}")
    print("─" * 73)
    for system in systems:
        status_color = Colors.GREEN if system.status == "CONNECTED" else Colors.YELLOW
        print(
            f"{Colors.BLUE}{timestamp()}{Colors.RESET}  "
            f"{Colors.CYAN}{system.system_id:<12}{Colors.RESET} "
            f"{status_color}{system.status:<12}{Colors.RESET} "
            f"{system.node:<6} {system.signal:>3}%   {system.ping:>3}ms "
            f"{system.cpu:>3}%  {system.storage:>3}%",
            flush=True,
        )
        time.sleep(interval)
    print()


def print_access_animation(system: System, step_delay: float) -> None:
    print(f"\n{Colors.MAGENTA}╭── REPORT: {system.system_id} ──╮{Colors.RESET}")
    phases = (
        "Preparazione report",
        "Caricamento informazioni",
        "Verifica dei dati visualizzati",
        "Completamento",
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
    print(f"{Colors.GREEN}\nREPORT PRONTO{Colors.RESET}\n")


def print_details(system: System, step_delay: float) -> None:
    print_access_animation(system, step_delay)
    print(f"{Colors.GREEN}╭── DETTAGLI: {system.system_id} ──╮{Colors.RESET}")
    print(f"STATO:           {system.status}")
    print(f"TIPO:            {system.device_type}")
    print(f"SISTEMA:         {system.operating_system}")
    print(f"NODO:            {system.node}")
    print(f"AREA:            {system.location}")
    print(f"SEGNALE:         {system.signal}%")
    print(f"PING:            {system.ping}ms")
    print(f"ATTIVO DA:       {system.uptime}")
    print(f"CPU:             {system.cpu}%")
    print(f"ARCHIVIAZIONE:   {system.storage}%")
    print(f"MEMORIA:         {system.memory}")
    print(f"LIVELLO:         {system.clearance}")
    print(f"EVENTO:          {system.log}\n")


def print_status(systems: list[System]) -> None:
    if not systems:
        print(f"{Colors.RED}Nessun gruppo attivo. Esegui 'scan' per crearne uno.{Colors.RESET}")
        return
    counts = {status: sum(system.status == status for system in systems) for status in STATUSES}
    print(f"{Colors.CYAN}RIEPILOGO GRUPPO ({len(systems)} sistemi){Colors.RESET}")
    for status, count in counts.items():
        print(f"  {status:<12} {count}")
    print(f"  CPU media       {sum(s.cpu for s in systems) / len(systems):.1f}%")
    print(f"  Segnale medio   {sum(s.signal for s in systems) / len(systems):.1f}%")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Console offline con dati sintetici")
    parser.add_argument("--interval", type=float, default=0.15, help="secondi tra le righe mostrate da scan")
    parser.add_argument("--animation-step", type=float, default=0.08, help="durata di ogni passo dell'animazione")
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval deve essere maggiore di zero")
    if args.animation_step <= 0:
        parser.error("--animation-step deve essere maggiore di zero")
    return args


def main() -> None:
    args = parse_args()
    clear_screen()
    print_banner()

    next_number = 1
    current_batch: list[System] = []
    events: list[str] = []

    while True:
        try:
            command = input(f"\n{Colors.GREEN}operatore@console{Colors.RESET}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSessione terminata.")
            break
        if not command:
            continue

        parts = command.split()
        action = parts[0].lower()
        clear_screen()
        print_banner()

        if action in ("help", "?"):
            print_help()
        elif action in ("scan", "s"):
            batch_size = random.randint(5, 15)
            current_batch = [
                make_system(number)
                for number in range(next_number, next_number + batch_size)
            ]
            next_number += batch_size
            record_event(events, f"GRUPPO CREATO: {len(current_batch)} sistemi")
            print_scan_batch(current_batch, args.interval)
        elif action in ("list", "ls"):
            if not current_batch:
                print(f"{Colors.RED}Nessun gruppo attivo. Esegui 'scan'.{Colors.RESET}")
            else:
                print(f"{Colors.CYAN}GRUPPO ATTIVO ({len(current_batch)} sistemi){Colors.RESET}")
                for system in current_batch:
                    print(f"  {system.system_id} | {system.status} | {system.node} | {system.signal}%")
        elif action in ("access", "a"):
            if len(parts) != 2:
                print(f"{Colors.RED}Uso: access 003 oppure access SYSTEM-003{Colors.RESET}")
                continue
            if not current_batch:
                print(f"{Colors.RED}Nessun gruppo attivo. Esegui 'scan'.{Colors.RESET}")
                continue
            system = find_system(parts[1], current_batch)
            if system is None:
                print(f"{Colors.RED}ID non presente nell'ultimo gruppo.{Colors.RESET}")
                record_event(events, f"ID NON TROVATO: {parts[1]}")
            else:
                record_event(events, f"REPORT VISUALIZZATO: {system.system_id}")
                print_details(system, args.animation_step)
        elif action == "status":
            print_status(current_batch)
            if current_batch:
                record_event(events, "RIEPILOGO VISUALIZZATO")
        elif action == "log":
            if not events:
                print("Nessun evento registrato. Esegui 'scan' per iniziare.")
            else:
                print(f"{Colors.CYAN}CRONOLOGIA RECENTE{Colors.RESET}")
                for event in events[-20:]:
                    print(f"  {event}")
        elif action == "clear":
            print("Schermata pulita. Digita 'help' per la guida ai comandi.")
        elif action in ("exit", "quit", "q"):
            print("\nConsole chiusa.")
            break
        else:
            print(f"{Colors.RED}Comando non riconosciuto. Digita 'help'.{Colors.RESET}")

    print("\nSessione terminata.")


if __name__ == "__main__":
    main()
