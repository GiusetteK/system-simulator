# System Simulator

Simulatore offline da terminale con flusso continuo di telemetria sintetica.

## Descrizione
Il programma mostra sistemi immaginari, con colori e layout da dashboard cyberpunk. Ogni record contiene:
- stato del sistema
- tipo di dispositivo
- sistema operativo
- nodo di appartenenza
- segnale e ping
- uptime, CPU e storage
- memoria e clearance
- log sintetico

Questi dati sono completamente inventati e generati localmente. Il programma non scansisce reti né contatta dispositivi reali.

## Requisiti
- Python 3.10 o successivo
- macOS, Linux o Windows
- Nessuna libreria esterna

## Avvio
```bash
python3 scripts/system-simulator.py
```

Se vuoi una velocità maggiore del flusso:

```bash
python3 scripts/system-simulator.py --interval 0.2
```

Se vuoi rallentare l'animazione di ingresso:

```bash
python3 scripts/system-simulator.py --animation-step 0.08
```

## Uso
- Inserisci un ID del tipo `SYSTEM-003` oppure il numero `3` per vedere le specifiche di quel sistema.
- Premi **Invio** per continuare con il flusso successivo.
- Inserisci **R** per generare un altro batch.
- Inserisci **Q** o premi **Ctrl+C** per uscire.

## Licenza
MIT
