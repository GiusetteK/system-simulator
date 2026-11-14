# System Simulator

Console interattiva offline che genera telemetria sintetica per sistemi immaginari, con un'interfaccia terminale in stile cyberpunk.

> **Nota:** tutti i dati e le animazioni sono fittizi e locali. Il programma non esegue scansioni di rete e non contatta né accede a dispositivi o sistemi reali.

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

Per regolare la velocità dello scan e dell'animazione:

```bash
python3 scripts/system-simulator.py --interval 0.2 --animation-step 0.08
```

## Comandi
Dopo l'avvio, inserisci un comando al prompt:

| Comando | Descrizione |
| --- | --- |
| `help` | Mostra i comandi disponibili. |
| `scan` | Genera e mostra 15 sistemi fittizi. La numerazione continua nei batch successivi. |
| `list` | Elenca i sistemi del batch attivo. |
| `access 003` | Mostra l'animazione locale e le specifiche fittizie del sistema selezionato. È possibile usare anche `access SYSTEM-003`. |
| `status` | Riepiloga stati, CPU media e segnale medio del batch attivo. |
| `log` | Mostra gli ultimi eventi della sessione. |
| `clear` | Pulisce il terminale. |
| `exit` | Chiude il programma. |

## Licenza
MIT. Consulta il file [LICENSE](LICENSE).
