#!/usr/bin/env python3
"""Offline console that displays locally generated, fictional telemetry."""

from __future__ import annotations

import argparse
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
    "Handshake generated",
    "Synchronization complete",
    "Routine check passed",
    "Data packet received",
)


class Colors:
    enabled = sys.stdout.isatty()
    GREEN = "\033[32m" if enabled else ""
    CYAN = "\033[36m" if enabled else ""
    YELLOW = "\033[33m" if enabled else ""
    BLUE = "\033[34m" if enabled else ""
    MAGENTA = "\033[35m" if enabled else ""
    RED = "\033[31m" if enabled else ""
    RESET = "\033[0m" if enabled else ""


def make_system(number: int) -> System:
    """Create a fictional record without querying a device or network."""
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
    """Clear an interactive terminal; do not emit escape codes when redirected."""
    if sys.stdout.isatty():
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def print_banner() -> None:
    print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════╗")
    print("║                   SYSTEM CONSOLE                    ║")
    print("║                 TELEMETRY DASHBOARD                 ║")
    print(f"╚══════════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"{Colors.BLUE}OFFLINE CONSOLE // LOCALLY GENERATED DATA{Colors.RESET}")
    print("All records are fictional; no networks or real devices are queried.\n")


def print_help() -> None:
    print(f"{Colors.CYAN}COMMAND GUIDE{Colors.RESET}")
    print("Data is generated locally. Commands do not query networks or devices.")
    print("\n  help  (or ?)\n      Show this guide. Example: help")
    print("\n  scan  (or s)\n      Create a random group of 5 to 15 systems and show their summary.")
    print("      IDs continue sequentially across groups. Example: scan")
    print("\n  list  (or ls)\n      List IDs and summary data for the latest group. Run scan first.")
    print("      Example: list")
    print("\n  access ID  (or a ID)\n      Show a detailed report for a system in the latest group.")
    print("      Use a number or full ID. Examples: access 003, access SYSTEM-003")
    print("\n  status\n      Show status counts and average CPU and signal for the latest group.")
    print("      Example: status")
    print("\n  log\n      Show the latest 20 events from this session. Example: log")
    print("\n  clear\n      Clear the terminal and redraw the header. Example: clear")
    print("\n  exit  (or quit or q)\n      Close the program. Example: exit\n")


def print_scan_batch(systems: list[System], interval: float) -> None:
    print(f"\n{Colors.CYAN}TIME     SYSTEM       STATUS       NODE   SIGNAL  PING   CPU  STORAGE{Colors.RESET}")
    print("─" * 73)
    for system in systems:
        color = Colors.GREEN if system.status == "CONNECTED" else Colors.YELLOW
        print(
            f"{Colors.BLUE}{timestamp()}{Colors.RESET}  "
            f"{Colors.CYAN}{system.system_id:<12}{Colors.RESET} "
            f"{color}{system.status:<12}{Colors.RESET} "
            f"{system.node:<6} {system.signal:>3}%   {system.ping:>3}ms "
            f"{system.cpu:>3}%  {system.storage:>3}%",
            flush=True,
        )
        time.sleep(interval)
    print()


def print_details(system: System, step_delay: float) -> None:
    print(f"\n{Colors.MAGENTA}╭── REPORT: {system.system_id} ──╮{Colors.RESET}")
    for phase in ("Preparing report", "Loading information", "Checking data", "Complete"):
        print(f"\n{Colors.BLUE}{phase}...{Colors.RESET}")
        for percent in range(0, 101, 5):
            filled = percent // 10
            bar = "█" * filled + "░" * (10 - filled)
            sys.stdout.write(f"\r[{bar}] {percent:3d}%")
            sys.stdout.flush()
            time.sleep(step_delay)
        print()

    print(f"{Colors.GREEN}\nREPORT READY{Colors.RESET}\n")
    fields = (
        ("STATUS", system.status),
        ("TYPE", system.device_type),
        ("OPERATING SYSTEM", system.operating_system),
        ("NODE", system.node),
        ("AREA", system.location),
        ("SIGNAL", f"{system.signal}%"),
        ("PING", f"{system.ping}ms"),
        ("UPTIME", system.uptime),
        ("CPU", f"{system.cpu}%"),
        ("STORAGE", f"{system.storage}%"),
        ("MEMORY", system.memory),
        ("CLEARANCE LEVEL", str(system.clearance)),
        ("EVENT", system.log),
    )
    print(f"{Colors.GREEN}╭── DETAILS: {system.system_id} ──╮{Colors.RESET}")
    for label, value in fields:
        print(f"{label + ':':<20}{value}")
    print()


def print_status(systems: list[System]) -> None:
    if not systems:
        print(f"{Colors.RED}No active group. Run 'scan' to create one.{Colors.RESET}")
        return
    counts = {status: sum(system.status == status for system in systems) for status in STATUSES}
    print(f"{Colors.CYAN}GROUP SUMMARY ({len(systems)} systems){Colors.RESET}")
    for status, count in counts.items():
        print(f"  {status:<12} {count}")
    print(f"  {'Average CPU':<16} {sum(s.cpu for s in systems) / len(systems):.1f}%")
    print(f"  {'Average signal':<16} {sum(s.signal for s in systems) / len(systems):.1f}%")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Offline console with locally generated telemetry")
    parser.add_argument("--interval", type=float, default=0.15, help="seconds between displayed scan rows")
    parser.add_argument("--animation-step", type=float, default=0.08, help="duration of each animation step")
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
    print("Type 'help' to see the command guide.\n")

    next_number = 1
    current_batch: list[System] = []
    events: list[str] = []

    while True:
        try:
            command = input(f"{Colors.GREEN}operator@console{Colors.RESET}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
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
            current_batch = [make_system(n) for n in range(next_number, next_number + batch_size)]
            next_number += batch_size
            record_event(events, f"GROUP CREATED: {len(current_batch)} systems")
            print_scan_batch(current_batch, args.interval)
        elif action in ("list", "ls"):
            if not current_batch:
                print(f"{Colors.RED}No active group. Run 'scan'.{Colors.RESET}")
            else:
                print(f"{Colors.CYAN}ACTIVE GROUP ({len(current_batch)} systems){Colors.RESET}")
                for system in current_batch:
                    print(f"  {system.system_id} | {system.status} | {system.node} | {system.signal}%")
        elif action in ("access", "a"):
            if len(parts) != 2:
                print(f"{Colors.RED}Usage: access 003 or access SYSTEM-003{Colors.RESET}")
            elif not current_batch:
                print(f"{Colors.RED}No active group. Run 'scan'.{Colors.RESET}")
            else:
                system = find_system(parts[1], current_batch)
                if system is None:
                    print(f"{Colors.RED}ID not found in the latest group.{Colors.RESET}")
                    record_event(events, f"ID NOT FOUND: {parts[1]}")
                else:
                    record_event(events, f"REPORT DISPLAYED: {system.system_id}")
                    print_details(system, args.animation_step)
        elif action == "status":
            print_status(current_batch)
            if current_batch:
                record_event(events, "GROUP SUMMARY DISPLAYED")
        elif action == "log":
            if not events:
                print("No events recorded. Run 'scan' to begin.")
            else:
                print(f"{Colors.CYAN}RECENT EVENTS{Colors.RESET}")
                for event in events[-20:]:
                    print(f"  {event}")
        elif action == "clear":
            print("Screen cleared. Type 'help' for the command guide.")
        elif action in ("exit", "quit", "q"):
            print("\nConsole closed.")
            break
        else:
            print(f"{Colors.RED}Command not recognized. Type 'help'.{Colors.RESET}")

    print("\nSession ended.")


if __name__ == "__main__":
    main()
