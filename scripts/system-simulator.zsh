#!/usr/bin/env zsh

# system-simulator
# Offline terminal demo: synthetic telemetry for fictional devices.
# This project does not scan the network and does not access real systems.

setopt no_nomatch

# Device state
typeset -A STATUSES TYPES OS NODES MEMORYS LOGS LOCATIONS SIGNALS PINGS UPTIMES CPUS STORAGES CLEARANCES

# Options
typeset -a STATUS_VALUES=(CONNECTED SCANNING ENCRYPTED)
typeset -a TYPE_VALUES=(LAPTOP WORKSTATION SERVER)
typeset -a OS_VALUES=(OS-ALPHA OS-BETA OS-GAMMA)
typeset -a NODE_VALUES=(NORTH EAST WEST SOUTH)
typeset -a MEMORY_VALUES=("8 GB" "16 GB" "32 GB")
typeset -a LOG_VALUES=(
  "Handshake simulato"
  "Sincronizzazione completata"
  "Controllo di routine superato"
  "Pacchetto demo ricevuto"
)

# Colors
GREEN=$'\033[32m'
CYAN=$'\033[36m'
YELLOW=$'\033[33m'
BLUE=$'\033[34m'
MAGENTA=$'\033[35m'
RED=$'\033[31m'
RESET=$'\033[0m'

random_index() {
  local total=$1
  echo $((RANDOM % total + 1))
}

generate_system() {
  local id=$1
  local status_index type_index os_index node_index memory_index log_index

  status_index=$(random_index ${#STATUS_VALUES[@]})
  type_index=$(random_index ${#TYPE_VALUES[@]})
  os_index=$(random_index ${#OS_VALUES[@]})
  node_index=$(random_index ${#NODE_VALUES[@]})
  memory_index=$(random_index ${#MEMORY_VALUES[@]})
  log_index=$(random_index ${#LOG_VALUES[@]})

  STATUSES[$id]=${STATUS_VALUES[$status_index]}
  TYPES[$id]=${TYPE_VALUES[$type_index]}
  OS[$id]=${OS_VALUES[$os_index]}
  NODES[$id]=${NODE_VALUES[$node_index]}
  MEMORYS[$id]=${MEMORY_VALUES[$memory_index]}
  LOGS[$id]=${LOG_VALUES[$log_index]}

  LOCATIONS[$id]=$(printf 'SECTOR-%02d' "$((RANDOM % 12 + 1))")
  SIGNALS[$id]=$((RANDOM % 45 + 55))
  PINGS[$id]=$((RANDOM % 169 + 12))
  UPTIMES[$id]="$((RANDOM % 240 + 1))h $((RANDOM % 60))m"
  CPUS[$id]=$((RANDOM % 91 + 5))
  STORAGES[$id]=$((RANDOM % 81 + 10))
  CLEARANCES[$id]=$((RANDOM % 5 + 1))
}

print_banner() {
  printf '%sSIMULATORE DI TELEMETRIA LOCALE%s\n' "$CYAN" "$RESET"
  printf '%sDemo terminale: dati sintetici, totalmente locali.%s\n\n' "$YELLOW" "$RESET"
}

print_details() {
  local id=$1

  printf '%s%s%s\n' "$GREEN" "$id" "$RESET"
  printf 'STATUS: %s\n' "${STATUSES[$id]}"
  printf 'TYPE: %s\n' "${TYPES[$id]}"
  printf 'OS: %s\n' "${OS[$id]}"
  printf 'NODE: %s\n' "${NODES[$id]}"
  printf 'LOCATION: %s\n' "${LOCATIONS[$id]}"
  printf 'SIGNAL: %s%%\n' "${SIGNALS[$id]}"
  printf 'PING: %sms\n' "${PINGS[$id]}"
  printf 'UPTIME: %s\n' "${UPTIMES[$id]}"
  printf 'CPU: %s%%\n' "${CPUS[$id]}"
  printf 'STORAGE USED: %s%%\n' "${STORAGES[$id]}"
  printf 'MEMORY: %s\n' "${MEMORYS[$id]}"
  printf 'CLEARANCE: LEVEL-%s\n' "${CLEARANCES[$id]}"
  printf 'LOG: %s\n' "${LOGS[$id]}"

  if [[ "${STATUSES[$id]}" == "ENCRYPTED" ]]; then
    printf '\n%sACCESSO DEMO%s\n' "$MAGENTA" "$RESET"
    printf 'Inizializzazione ambiente demo...\n'
    sleep 0.3
    printf 'Analisi del sistema...\n'
    sleep 0.3
    printf 'Controllo completato.\n'
    sleep 0.2
    printf '%sACCESSO COMPLETATO%s\n\n' "$GREEN" "$RESET"
  fi
}

normalize_system_id() {
  local raw=$1
  raw=${raw:u}

  if [[ "$raw" =~ ^[0-9]+$ ]]; then
    printf 'SYSTEM-%03d' "$raw"
  else
    printf '%s' "$raw"
  fi
}

print_dashboard() {
  clear
  print_banner

  for i in {1..15}; do
    local id
    id=$(printf 'SYSTEM-%03d' "$i")

    if [[ -z ${STATUSES[$id]+x} ]]; then
      generate_system "$id"
    fi

    printf '%s%s%s %s%s%s | NODE: %s | SIGNAL: %s%% | PING: %sms\n' \
      "$GREEN" "$id" "$RESET" \
      "$YELLOW" "${STATUSES[$id]}" "$RESET" \
      "${NODES[$id]}" "${SIGNALS[$id]}" "${PINGS[$id]}"
  done

  printf '\n%sInserisci un ID (es. SYSTEM-003) oppure Q per uscire:%s ' "$BLUE" "$RESET"
  read -r input
  echo

  if [[ "$input" == "q" || "$input" == "Q" ]]; then
    exit 0
  fi

  local system_id
  system_id=$(normalize_system_id "$input")

  if [[ -n "${STATUSES[$system_id]-}" ]]; then
    print_details "$system_id"
  else
    printf '%s%s%s: sistema non riconosciuto.\n' "$RED" "$system_id" "$RESET"
  fi

  printf '\n%sPremi Invio per continuare...%s' "$BLUE" "$RESET"
  read -r _
}

main() {
  for i in {1..15}; do
    local id
    id=$(printf 'SYSTEM-%03d' "$i")
    generate_system "$id"
  done

  while true; do
    print_dashboard
  done
}

main "$@"
