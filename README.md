# System Simulator

Console interattiva offline che genera dati sintetici per sistemi immaginari e li mostra in una dashboard da terminale.

> I valori sono generati localmente. Il programma non esegue scansioni di rete e non contatta dispositivi reali.

## Requisiti
- Python 3.10 o successivo
- macOS, Linux o Windows
- Nessuna dipendenza esterna

## Avvio
Dalla cartella principale del repository:

```bash
python3 scripts/system-simulator.py
```

Su Windows, se `python3` non è disponibile:

```powershell
py scripts/system-simulator.py
```

Per regolare la velocità di visualizzazione:

```bash
python3 scripts/system-simulator.py --interval 0.2 --animation-step 0.08
```

## Comandi
All'avvio viene mostrato un breve invito a usare `help`. Il comando `help` descrive in dettaglio tutti i comandi e include esempi.

| Comando | Descrizione |
| --- | --- |
| `help` | Mostra la guida dettagliata. |
| `scan` | Genera un gruppo casuale da 5 a 15 record. |
| `list` | Elenca il gruppo corrente. |
| `access 003` | Mostra il report per un ID del gruppo corrente. |
| `status` | Riepiloga stati, CPU media e segnale medio. |
| `log` | Mostra gli ultimi eventi della sessione. |
| `clear` | Pulisce il terminale. |
| `exit` | Chiude il programma. |

## Licenza
MIT. Consulta il file [LICENSE](LICENSE).
