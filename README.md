#!/usr/bin/env python3
"""System telemetry console for a fictional network-monitoring dashboard."""

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
    "Handshake completed",
    "Sync successful",
    "Routine control passed",
    "Telemetry packet received",
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
    if not sys.stdout.isatty():
        return
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def print_banner() -> None:
    print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════╗")
    print("║              S Y S T E M   C O N S O L E            ║")
    print("║                 T E L E M E T R Y   A C C E S S       ║")
    print(f"╚══════════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"{Colors.BLUE}LIVE NETWORK STATUS // SECURE ACCESS PORTAL{Colors.RESET}\n")


def print_help() -> None:
    print(f"{Colors.CYAN}COMMANDS{Colors.RESET}")
    print("  help        show available commands")
    print("  scan        generate a new batch of 5-15 systems")
    print("  list        list the active batch")
    print("  access ID   open a system record (example: access 003)")
    print("  status      show batch telemetry summary")
    print("  log         show recent system events")
    print("  clear       clear the terminal")
    print("  exit        close the console")


def print_scan_batch(systems: list[System], interval: float) -> None:
    print(f"\n{Colors.CYAN}TIME     SYSTEM       STATUS       NODE   SIGNAL  PING   CPU  STORAGE{Colors.RESET}")
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
    print(f"\n{Colors.MAGENTA}╭── ACCESS PORTAL: {system.system_id} ──╮{Colors.RESET}")
    phases = (
        "Initializing secure channel",
        "Verifying node routing",
        "Checking access authorization",
        "Loading telemetry stream",
        "Session ready",
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
    print(f"{Colors.GREEN}\nACCESS VERIFIED{Colors.RESET}\n")


def print_details(system: System, step_delay: float) -> None:
    print_access_animation(system, step_delay)
    print(f"{Colors.GREEN}╭── SYSTEM REPORT: {system.system_id} ──╮{Colors.RESET}")
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
    print()


def print_status(systems: list[System]) -> None:
    if not systems:
        print(f"{Colors.RED}No active batch. Use 'scan'.{Colors.RESET}")
        return
    counts = {status: sum(s.status == status for s in systems) for status in STATUSES}
    print(f"{Colors.CYAN}BATCH STATUS ({len(systems)} systems){Colors.RESET}")
    for status, count in counts.items():
        print(f"  {status:<12} {count}")
    print(f"  Average CPU   {sum(s.cpu for s in systems) / len(systems):.1f}%")
    print(f"  Average signal {sum(s.signal for s in systems) / len(systems):.1f}%")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="System telemetry console")
    parser.add_argument("--interval", type=float, default=0.15, help="seconds between scan rows")
    parser.add_argument("--animation-step", type=float, default=0.08, help="seconds for each animation step")
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval must be greater than zero")
    if args.animation_step <= 0:
        parser.error("--animation-step must be greater than zero")
    return args


def main() -> None:
    args = parse_args()
    clear_screen()
    print_banner()
    print_help()

    next_number = 1
    current_batch: list[System] = []
    events: list[str] = []

    while True:
        try:
            command = input(f"\n{Colors.GREEN}operator@secure-console{Colors.RESET}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession closed.")
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
            record_event(events, f"BATCH GENERATED: {len(current_batch)} systems")
            print_scan_batch(current_batch, args.interval)
        elif action in ("list", "ls"):
            if not current_batch:
                print(f"{Colors.RED}No active batch. Run 'scan'.{Colors.RESET}")
            else:
                print(f"{Colors.CYAN}ACTIVE BATCH ({len(current_batch)} systems){Colors.RESET}")
                for system in current_batch:
                    print(f"  {system.system_id} | {system.status} | {system.node} | {system.signal}%")
        elif action in ("access", "a"):
            if len(parts) != 2:
                print(f"{Colors.RED}Usage: access 003 or access SYSTEM-003{Colors.RESET}")
                continue
            if not current_batch:
                print(f"{Colors.RED}No active batch. Run 'scan'.{Colors.RESET}")
                continue
            system = find_system(parts[1], current_batch)
            if system is None:
                print(f"{Colors.RED}System not found in the active batch.{Colors.RESET}")
                record_event(events, f"ACCESS FAILED: {parts[1]}")
            else:
                record_event(events, f"SYSTEM REVIEW: {system.system_id}")
                print_details(system, args.animation_step)
        elif action == "status":
            print_status(current_batch)
            if current_batch:
                record_event(events, "ACTIVE BATCH STATUS CHECK")
        elif action == "log":
            if not events:
                print("No events logged yet.")
            else:
                print(f"{Colors.CYAN}RECENT EVENTS{Colors.RESET}")
                for event in events[-20:]:
                    print(f"  {event}")
        elif action == "clear":
            clear_screen()
            print_banner()
            print_help()
        elif action in ("exit", "quit", "q"):
            print("\nConsole closed.")
            break
        else:
            print(f"{Colors.RED}Command not recognized. Use 'help'.{Colors.RESET}")

    print("\nSession closed.")


if __name__ == "__main__":
    main()


























































