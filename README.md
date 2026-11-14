# System Simulator

Simulatore offline da terminale con flusso continuo di telemetria sintetica per sistemi immaginari.

## Avviso
Tutti i dati sono inventati. Il programma non esegue scansioni, non si connette alla rete e non accede a dispositivi o sistemi reali. L'animazione di "ingresso" è una semplice sequenza grafica locale.

## Requisiti
- Python 3.10 o successivo
- macOS, Linux o Windows
- Nessuna libreria esterna

## Avvio
Dalla cartella del repository:

```bash
python3 scripts/system-simulator.py
```

Su Windows, se `python3` non è disponibile:

```powershell
py scripts/system-simulator.py
```

Per regolare il flusso (intervallo in secondi tra le righe):

```bash
python3 scripts/system-simulator.py --interval 0.2
```

Per rallentare l'animazione demo, aumentando il tempo per ogni passo:

```bash
python3 scripts/system-simulator.py --animation-step 0.08
```

## Uso
Il programma mostra 15 sistemi per batch. I loro numeri continuano a crescere anche dopo un'ispezione: ad esempio, il batch successivo parte da `SYSTEM-016` invece di tornare a `SYSTEM-001`.

- Inserisci un ID mostrato (ad esempio `SYSTEM-003`) o il suo numero (`3`) per vedere le specifiche fittizie e l'animazione di ingresso.
- Premi **Invio** per proseguire con il batch successivo.
- Scrivi **R** per generare subito un nuovo batch (la numerazione continua).
- Scrivi **Q** o premi **Ctrl+C** per uscire.

## Licenza
MIT. Consulta [LICENSE](LICENSE).
