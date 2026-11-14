#!/usr/bin/env python3
"""Console offline with locally generated telemetry records."""

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

TEXT = {
    "it": {
        "title": "CONSOLE DI SISTEMA", "subtitle": "DASHBOARD TELEMETRIA",
        "notice": "Dati generati localmente; nessuna scansione di rete o accesso a dispositivi reali.",
        "hint": "Digita 'help' per la guida ai comandi.", "prompt": "operatore@console",
        "help_title": "GUIDA AI COMANDI", "help_note": "I dati sono generati localmente; i comandi non interrogano reti o dispositivi.",
        "help_help": "Mostra questa guida.",
        "help_scan": "Crea un gruppo casuale da 5 a 15 sistemi e ne mostra i dati principali. Gli ID proseguono in sequenza.",
        "help_list": "Elenca gli ID e i dati sintetici dell'ultimo gruppo creato. Prima esegui scan.",
        "help_access": "Mostra il report di un sistema dell'ultimo gruppo. Usa un numero o un ID completo.",
        "help_status": "Mostra il conteggio per stato e le medie di CPU e segnale dell'ultimo gruppo.",
        "help_log": "Mostra gli ultimi 20 eventi di questa sessione.",
        "help_clear": "Pulisce lo schermo e ridisegna l'intestazione.",
        "help_lang": "Mostra le lingue disponibili o cambia lingua: lang it, lang en, lang es.",
        "help_exit": "Termina il programma.", "example": "Esempio:",
        "table_time": "ORA", "table_system": "SISTEMA", "table_status": "STATO", "table_node": "NODO",
        "table_signal": "SEGNALE", "table_ping": "PING", "table_cpu": "CPU", "table_storage": "DISCO",
        "report": "REPORT", "preparing": "Preparazione report", "loading": "Caricamento informazioni",
        "checking": "Controllo dei dati", "complete": "Completamento", "ready": "REPORT PRONTO",
        "details": "DETTAGLI", "field_status": "STATO", "field_type": "TIPO", "field_os": "SISTEMA OPERATIVO",
        "field_node": "NODO", "field_location": "AREA", "field_signal": "SEGNALE", "field_ping": "PING",
        "field_uptime": "ATTIVO DA", "field_cpu": "CPU", "field_storage": "ARCHIVIAZIONE",
        "field_memory": "MEMORIA", "field_clearance": "LIVELLO", "field_log": "EVENTO",
        "no_batch": "Nessun gruppo attivo. Esegui 'scan' per crearne uno.",
        "batch_status": "RIEPILOGO GRUPPO", "avg_cpu": "CPU media", "avg_signal": "Segnale medio",
        "active_batch": "GRUPPO ATTIVO", "usage_access": "Uso: access 003 oppure access SYSTEM-003",
        "not_found": "ID non presente nell'ultimo gruppo.", "events_title": "CRONOLOGIA RECENTE",
        "no_events": "Nessun evento registrato. Esegui 'scan' per iniziare.",
        "event_batch": "GRUPPO CREATO", "event_report": "REPORT VISUALIZZATO",
        "event_missing": "ID NON TROVATO", "event_status": "RIEPILOGO VISUALIZZATO",
        "unknown": "Comando non riconosciuto. Digita 'help'.", "cleared": "Schermata pulita.",
        "closed": "Console chiusa.", "ended": "Sessione terminata.", "lang_prompt": "Lingua (it/en/es) [it]: ",
        "lang_changed": "Lingua impostata su Italiano.", "lang_usage": "Lingue: it (Italiano), en (English), es (Español). Uso: lang it|en|es",
    },
    "en": {
        "title": "SYSTEM CONSOLE", "subtitle": "TELEMETRY DASHBOARD",
        "notice": "Locally generated data; no network scanning or access to real devices.",
        "hint": "Type 'help' for the command guide.", "prompt": "operator@console",
        "help_title": "COMMAND GUIDE", "help_note": "Data is generated locally; commands do not query networks or devices.",
        "help_help": "Show this guide.",
        "help_scan": "Create a random group of 5 to 15 systems and show their summary. IDs continue sequentially.",
        "help_list": "List IDs and summary data for the most recently created group. Run scan first.",
        "help_access": "Show a report for a system in the latest group. Use a number or full ID.",
        "help_status": "Show status counts and average CPU and signal for the latest group.",
        "help_log": "Show the latest 20 events from this session.",
        "help_clear": "Clear the screen and redraw the header.",
        "help_lang": "List available languages or change language: lang it, lang en, lang es.",
        "help_exit": "Exit the program.", "example": "Example:",
        "table_time": "TIME", "table_system": "SYSTEM", "table_status": "STATUS", "table_node": "NODE",
        "table_signal": "SIGNAL", "table_ping": "PING", "table_cpu": "CPU", "table_storage": "STORAGE",
        "report": "REPORT", "preparing": "Preparing report", "loading": "Loading information",
        "checking": "Checking data", "complete": "Completing", "ready": "REPORT READY",
        "details": "DETAILS", "field_status": "STATUS", "field_type": "TYPE", "field_os": "OPERATING SYSTEM",
        "field_node": "NODE", "field_location": "AREA", "field_signal": "SIGNAL", "field_ping": "PING",
        "field_uptime": "UPTIME", "field_cpu": "CPU", "field_storage": "STORAGE",
        "field_memory": "MEMORY", "field_clearance": "LEVEL", "field_log": "EVENT",
        "no_batch": "No active group. Run 'scan' to create one.",
        "batch_status": "GROUP SUMMARY", "avg_cpu": "Average CPU", "avg_signal": "Average signal",
        "active_batch": "ACTIVE GROUP", "usage_access": "Usage: access 003 or access SYSTEM-003",
        "not_found": "ID not found in the latest group.", "events_title": "RECENT EVENTS",
        "no_events": "No events recorded. Run 'scan' to begin.",
        "event_batch": "GROUP CREATED", "event_report": "REPORT DISPLAYED",
        "event_missing": "ID NOT FOUND", "event_status": "SUMMARY DISPLAYED",
        "unknown": "Command not recognized. Type 'help'.", "cleared": "Screen cleared.",
        "closed": "Console closed.", "ended": "Session ended.", "lang_prompt": "Language (it/en/es) [en]: ",
        "lang_changed": "Language set to English.", "lang_usage": "Languages: it (Italiano), en (English), es (Español). Usage: lang it|en|es",
    },
    "es": {
        "title": "CONSOLA DEL SISTEMA", "subtitle": "PANEL DE TELEMETRÍA",
        "notice": "Datos generados localmente; no se escanean redes ni se accede a dispositivos reales.",
        "hint": "Escribe 'help' para ver la guía de comandos.", "prompt": "operador@consola",
        "help_title": "GUÍA DE COMANDOS", "help_note": "Los datos se generan localmente; los comandos no consultan redes ni dispositivos.",
        "help_help": "Muestra esta guía.",
        "help_scan": "Crea un grupo aleatorio de 5 a 15 sistemas y muestra sus datos principales. Los ID siguen en secuencia.",
        "help_list": "Enumera los ID y datos resumidos del último grupo creado. Ejecuta scan primero.",
        "help_access": "Muestra el informe de un sistema del último grupo. Usa un número o el ID completo.",
        "help_status": "Muestra el recuento por estado y las medias de CPU y señal del último grupo.",
        "help_log": "Muestra los últimos 20 eventos de esta sesión.",
        "help_clear": "Limpia la pantalla y vuelve a mostrar el encabezado.",
        "help_lang": "Muestra los idiomas disponibles o cambia el idioma: lang it, lang en, lang es.",
        "help_exit": "Cierra el programa.", "example": "Ejemplo:",
        "table_time": "HORA", "table_system": "SISTEMA", "table_status": "ESTADO", "table_node": "NODO",
        "table_signal": "SEÑAL", "table_ping": "PING", "table_cpu": "CPU", "table_storage": "DISCO",
        "report": "INFORME", "preparing": "Preparando informe", "loading": "Cargando información",
        "checking": "Comprobando datos", "complete": "Finalizando", "ready": "INFORME LISTO",
        "details": "DETALLES", "field_status": "ESTADO", "field_type": "TIPO", "field_os": "SISTEMA OPERATIVO",
        "field_node": "NODO", "field_location": "ÁREA", "field_signal": "SEÑAL", "field_ping": "PING",
        "field_uptime": "TIEMPO ACTIVO", "field_cpu": "CPU", "field_storage": "ALMACENAMIENTO",
        "field_memory": "MEMORIA", "field_clearance": "NIVEL", "field_log": "EVENTO",
        "no_batch": "No hay ningún grupo activo. Ejecuta 'scan' para crear uno.",
        "batch_status": "RESUMEN DEL GRUPO", "avg_cpu": "CPU media", "avg_signal": "Señal media",
        "active_batch": "GRUPO ACTIVO", "usage_access": "Uso: access 003 o access SYSTEM-003",
        "not_found": "ID no encontrado en el último grupo.", "events_title": "EVENTOS RECIENTES",
        "no_events": "No hay eventos registrados. Ejecuta 'scan' para comenzar.",
        "event_batch": "GRUPO CREADO", "event_report": "INFORME MOSTRADO",
        "event_missing": "ID NO ENCONTRADO", "event_status": "RESUMEN MOSTRADO",
        "unknown": "Comando desconocido. Escribe 'help'.", "cleared": "Pantalla limpia.",
        "closed": "Consola cerrada.", "ended": "Sesión finalizada.", "lang_prompt": "Idioma (it/en/es) [es]: ",
        "lang_changed": "Idioma configurado en Español.", "lang_usage": "Idiomas: it (Italiano), en (English), es (Español). Uso: lang it|en|es",
    },
}


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
    if sys.stdout.isatty():
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def choose_language() -> str:
    print("Lingua / Language / Idioma")
    print("  it - Italiano   en - English   es - Español")
    try:
        choice = input("Language (it/en/es) [it]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return "it"
    return choice if choice in TEXT else "it"


def print_banner(language: str) -> None:
    t = TEXT[language]
    print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════╗")
    print(f"║{t['title']:^54}║")
    print(f"║{t['subtitle']:^54}║")
    print(f"╚══════════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"{Colors.BLUE}{t['notice']}{Colors.RESET}")
    print(f"{t['hint']}\n")


def print_help(language: str) -> None:
    t = TEXT[language]
    print(f"{Colors.CYAN}{t['help_title']}{Colors.RESET}")
    print(t["help_note"])
    entries = (
        ("help", t["help_help"], "help"),
        ("scan", t["help_scan"], "scan"),
        ("list", t["help_list"], "list"),
        ("access ID", t["help_access"], "access 003  /  access SYSTEM-003"),
        ("status", t["help_status"], "status"),
        ("log", t["help_log"], "log"),
        ("clear", t["help_clear"], "clear"),
        ("lang [it|en|es]", t["help_lang"], "lang en"),
        ("exit", t["help_exit"], "exit"),
    )
    for command, description, example in entries:
        print(f"\n  {Colors.GREEN}{command}{Colors.RESET}\n      {description}\n      {t['example']} {example}")
    print()


def print_scan_batch(systems: list[System], interval: float, language: str) -> None:
    t = TEXT[language]
    print(
        f"\n{Colors.CYAN}{t['table_time']:<8} {t['table_system']:<12} {t['table_status']:<12} "
        f"{t['table_node']:<6} {t['table_signal']:<7} {t['table_ping']:<6} "
        f"{t['table_cpu']:<4} {t['table_storage']}{Colors.RESET}"
    )
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


def print_details(system: System, step_delay: float, language: str) -> None:
    t = TEXT[language]
    print(f"\n{Colors.MAGENTA}╭── {t['report']}: {system.system_id} ──╮{Colors.RESET}")
    for phase in (t["preparing"], t["loading"], t["checking"], t["complete"]):
        print(f"\n{Colors.BLUE}{phase}...{Colors.RESET}")
        for percent in range(0, 101, 5):
            filled = percent // 10
            bar = "█" * filled + "░" * (10 - filled)
            sys.stdout.write(f"\r[{bar}] {percent:3d}%")
            sys.stdout.flush()
            time.sleep(step_delay)
        print()
    print(f"{Colors.GREEN}\n{t['ready']}{Colors.RESET}\n")

    fields = (
        ("field_status", system.status), ("field_type", system.device_type),
        ("field_os", system.operating_system), ("field_node", system.node),
        ("field_location", system.location), ("field_signal", f"{system.signal}%"),
        ("field_ping", f"{system.ping}ms"), ("field_uptime", system.uptime),
        ("field_cpu", f"{system.cpu}%"), ("field_storage", f"{system.storage}%"),
        ("field_memory", system.memory), ("field_clearance", str(system.clearance)),
        ("field_log", system.log),
    )
    print(f"{Colors.GREEN}╭── {t['details']}: {system.system_id} ──╮{Colors.RESET}")
    for key, value in fields:
        print(f"{t[key]+':':<19}{value}")
    print()


def print_status(systems: list[System], language: str) -> None:
    t = TEXT[language]
    if not systems:
        print(f"{Colors.RED}{t['no_batch']}{Colors.RESET}")
        return
    counts = {status: sum(system.status == status for system in systems) for status in STATUSES}
    print(f"{Colors.CYAN}{t['batch_status']} ({len(systems)} systems){Colors.RESET}")
    for status, count in counts.items():
        print(f"  {status:<12} {count}")
    print(f"  {t['avg_cpu']:<16} {sum(s.cpu for s in systems) / len(systems):.1f}%")
    print(f"  {t['avg_signal']:<16} {sum(s.signal for s in systems) / len(systems):.1f}%")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Offline console with locally generated telemetry")
    parser.add_argument("--interval", type=float, default=0.15, help="seconds between displayed scan rows")
    parser.add_argument("--animation-step", type=float, default=0.08, help="duration of each animation step")
    parser.add_argument("--language", choices=tuple(TEXT), help="interface language: it, en or es")
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval must be greater than zero")
    if args.animation_step <= 0:
        parser.error("--animation-step must be greater than zero")
    return args


def main() -> None:
    args = parse_args()
    language = args.language or choose_language()
    clear_screen()
    print_banner(language)

    next_number = 1
    current_batch: list[System] = []
    events: list[str] = []

    while True:
        t = TEXT[language]
        try:
            command = input(f"\n{Colors.GREEN}{t['prompt']}{Colors.RESET}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{t['ended']}")
            break
        if not command:
            continue

        parts = command.split()
        action = parts[0].lower()
        clear_screen()
        print_banner(language)

        if action in ("help", "?"):
            print_help(language)
        elif action in ("scan", "s"):
            batch_size = random.randint(5, 15)
            current_batch = [make_system(n) for n in range(next_number, next_number + batch_size)]
            next_number += batch_size
            record_event(events, f"{t['event_batch']}: {len(current_batch)}")
            print_scan_batch(current_batch, args.interval, language)
        elif action in ("list", "ls"):
            if not current_batch:
                print(f"{Colors.RED}{t['no_batch']}{Colors.RESET}")
            else:
                print(f"{Colors.CYAN}{t['active_batch']} ({len(current_batch)}){Colors.RESET}")
                for system in current_batch:
                    print(f"  {system.system_id} | {system.status} | {system.node} | {system.signal}%")
        elif action in ("access", "a"):
            if len(parts) != 2:
                print(f"{Colors.RED}{t['usage_access']}{Colors.RESET}")
            elif not current_batch:
                print(f"{Colors.RED}{t['no_batch']}{Colors.RESET}")
            else:
                system = find_system(parts[1], current_batch)
                if system is None:
                    print(f"{Colors.RED}{t['not_found']}{Colors.RESET}")
                    record_event(events, f"{t['event_missing']}: {parts[1]}")
                else:
                    record_event(events, f"{t['event_report']}: {system.system_id}")
                    print_details(system, args.animation_step, language)
        elif action == "status":
            print_status(current_batch, language)
            if current_batch:
                record_event(events, t["event_status"])
        elif action == "log":
            if not events:
                print(t["no_events"])
            else:
                print(f"{Colors.CYAN}{t['events_title']}{Colors.RESET}")
                for event in events[-20:]:
                    print(f"  {event}")
        elif action == "clear":
            print(t["cleared"])
        elif action in ("lang", "language"):
            if len(parts) == 1:
                print(t["lang_usage"])
            elif parts[1].lower() not in TEXT:
                print(f"{Colors.RED}{t['lang_usage']}{Colors.RESET}")
            else:
                language = parts[1].lower()
                t = TEXT[language]
                print(t["lang_changed"])
                print_banner(language)
        elif action in ("exit", "quit", "q"):
            print(f"\n{t['closed']}")
            break
        else:
            print(f"{Colors.RED}{t['unknown']}{Colors.RESET}")


if __name__ == "__main__":
    main()
