🚀 Projekt-Anleitung: Interaktive Flugsuche (Web & Telegram Bot)
Diese Anleitung erklärt dir Schritt für Schritt, was du für das Projekt benötigst, wie du alle Abhängigkeiten installierst und wie du die Flask-Webseite sowie den Telegram-Bot parallel startest.

1. System-Voraussetzungen (Was du brauchst)
Bevor du startest, müssen folgende Programme auf deinem Computer installiert sein:

Python (Empfohlen: Version 3.10 oder neuer)

Pipenv (Der Paket-Manager für die virtuelle Umgebung)

Falls noch nicht installiert, öffne dein normales Terminal und tippe: pip install pipenv

Zwei separate Terminal-Fenster (Kommandozeilen / VS Code Terminals)

2. Projekt-Struktur überprüfen
Stelle sicher, dass deine Dateien exakt so im Hauptordner PROJEKT 1 angeordnet sind:

Plaintext
PROJEKT 1/
│
├── Bot/
│   └── bot.py               # Der interaktive Telegram-Bot
│
├── Webpage/
│   ├── static/
│   │   ├── app.js           # Frontend JavaScript
│   │   └── style.css        # SWISS-Design CSS
│   ├── templates/
│   │   └── index.html       # HTML-Formular & Anzeige
│   └── app.py               # Die Flask-Webseite
│
├── General/
│   ├── __init__.py          # Macht den Ordner zum Python-Modul (leer)
│   └── flight_planner.py    # DAS RECHNERZENTRUM (Zentrale Logik für beide)
│
├── flights.json             # Die gemeinsame Flug-Datenbank
├── README.md                # Dein Punkt
└── Pipfile                  # Liste der benötigten Bibliotheken
3. Installation der Bibliotheken
Wenn du das Projekt zum ersten Mal startest oder Fehlermeldungen wie ModuleNotFoundError (z.B. No module named 'flask' oder 'telebot') bekommst, musst du die virtuelle Umgebung einrichten.

Öffne ein Terminal und wechsle in das Hauptverzeichnis PROJEKT 1.

Führe folgenden Befehl aus, um alle Abhängigkeiten aus dem Pipfile automatisch zu installieren:

Bash
pipenv install
(Hinweis: Dadurch werden Flask, PyTelegramBotAPI und Requests in einer isolierten Umgebung installiert, ohne dein globales Python zu verändern).

4. Parallel starten (Schritt-für-Schritt)
Da es sich um zwei eigenständige Programme handelt, müssen sie in zwei separaten Terminal-Fenstern gleichzeitig laufen.

Schritt 1: Die Flask-Webseite starten
Öffne das erste Terminal-Fenster und vergewissere dich, dass du im Ordner PROJEKT 1 bist.

Starte die Webseite mit dem Befehl:

Bash
pipenv run python Webpage/app.py
Ergebnis: Das Terminal bleibt aktiv und zeigt an: * Running on http://127.0.0.1:5000. Du kannst die Website jetzt in deinem Browser unter dieser Adresse öffnen.

Schritt 2: Den Telegram-Bot starten
Öffne ein zweites, neues Terminal-Fenster (schließe das erste nicht!). Stelle sicher, dass du auch hier im Ordner PROJEKT 1 bist.

Starte den Bot mit dem Befehl:

Bash
pipenv run python Bot/bot.py
Ergebnis: Das Terminal zeigt 🚀 Interactive Bot is polling... an. Der Bot ist nun live und reagiert in Echtzeit in Telegram auf /flight.

5. Steuerung & Beenden
Aktualisierungen: Wenn du Code änderst, startet sich die Webseite (app.py) dank des debug=True-Modus von alleine neu. Der Bot (bot.py) muss nach Code-Änderungen im Terminal einmal neu gestartet werden.

Beenden: Um ein Programm zu stoppen, klicke in das jeweilige Terminal-Fenster und drücke die Tastenkombination:

Plaintext
Strg + C  (oder Ctrl + C bei Mac)