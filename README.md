# System Simulator

Console interattiva offline che genera localmente record di telemetria per sistemi immaginari. Non esegue scansioni di rete e non contatta dispositivi reali.

## Requisiti
- Python 3.10 o successivo
- Nessuna dipendenza esterna

## Avvio
```bash
python3 scripts/system-simulator.py
```

All'avvio scegli la lingua dell'interfaccia: Italiano (`it`), English (`en`) o Español (`es`). Puoi anche impostarla direttamente:

```bash
python3 scripts/system-simulator.py --language en
```

La lingua si può cambiare durante l'esecuzione con `lang it`, `lang en` oppure `lang es`. I comandi restano gli stessi in tutte le lingue; `help` mostra la guida tradotta.

## Comandi
`help`, `scan`, `list`, `access ID`, `status`, `log`, `clear`, `lang [it|en|es]`, `exit`.

Per regolare la velocità di visualizzazione:

```bash
python3 scripts/system-simulator.py --interval 0.2 --animation-step 0.08
```

## Licenza
MIT. Consulta [LICENSE](LICENSE).
