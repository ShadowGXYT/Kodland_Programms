import os
import sys
import time
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator

# ==========================================
# 1. CONFIGURATION & LANG DATA
# ==========================================
DURATION = 5  # Sekunden für die Aufnahme (für Testzwecke auf 5s, beliebig änderbar)
SAMPLE_RATE = 44100

LANGUAGES = {
    "1": ("German", "de", "DE"),   "2": ("English", "en", "EN"),  "3": ("Russian", "ru", "RU"),
    "4": ("Spanish", "es", "ES"),  "5": ("French", "fr", "FR"),   "6": ("Italian", "it", "IT"),
    "7": ("Turkish", "tr", "TR"),  "8": ("Polish", "pl", "PL"),   "9": ("Portuguese", "pt", "PT")
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# 2. DYNAMISCHES MENÜ (3 SPALTEN)
# ==========================================
def print_menu():
    clear_screen()
    print("╔" + "═"*57 + "╗")
    print("║" + " AI AUDIO TRANSLATOR Terminal Pro ".center(57, " ") + "║")
    print("╠" + "═"*57 + "╣")
    
    # Generiert 3 saubere Spalten für die 9 Sprachen
    keys = list(LANGUAGES.keys())
    for i in range(0, 3):
        k1, k2, k3 = keys[i], keys[i+3], keys[i+6]
        n1, _, c1 = LANGUAGES[k1]
        n2, _, c2 = LANGUAGES[k2]
        n3, _, c3 = LANGUAGES[k3]
        
        row = f"  [{k1}] {n1:<10} ({c1})   [{k2}] {n2:<10} ({c2})   [{k3}] {n3:<10} ({c3})"
        print(f"║{row:<57}║")
        
    print("╚" + "═"*57 + "╝")

# ==========================================
# 3. INTERAKTIVE EINGABE-VALIDIERUNG
# ==========================================
print_menu()

# Auswahl Ausgangssprache
while True:
    src_choice = input(" ► Select YOUR Language (1-9): ").strip()
    if src_choice in LANGUAGES:
        src_name, src_code, src_cc = LANGUAGES[src_choice]
        print(f"   ✔ Selected: {src_name} [{src_cc}]")
        break
    print("   ❌ Invalid ID. Try again.")

print("─"*59)

# Auswahl Zielsprache
while True:
    dest_choice = input(" ► Select TARGET Language (1-9): ").strip()
    if dest_choice in LANGUAGES:
        dest_name, dest_code, dest_cc = LANGUAGES[dest_choice]
        print(f"   ✔ Selected: {dest_name} [{dest_cc}]")
        break
    print("   ❌ Invalid ID. Try again.")

# ==========================================
# 4. AUDIO-AUFNAHME MIT ECHTEM LADEBALKEN
# ==========================================
print("\n" + "░"*59)
print(f" 🎙️  READY TO RECORD: Please speak in {src_name.upper()} ".center(59, "░"))
print("░"*59 + "\n")

# Aufnahme im Hintergrund starten
recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")

# Der animierte Progress-Bar
bar_length = 30
for elapsed in range(DURATION * 10 + 1):
    percent = elapsed / (DURATION * 10)
    filled_length = int(bar_length * percent)
    # Erstellt den Ladebalken: ██████░░░░░░
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    
    # Berechnet verbleibende Sekunden
    rem_time = max(0.0, DURATION - (elapsed / 10))
    
    # \r überschreibt die aktuelle Zeile in der Konsole live
    sys.stdout.write(f"\r 🔴 RECORDING: [{bar}] {int(percent*100)}% | Rem: {rem_time:.1f}s ")
    sys.stdout.flush()
    time.sleep(0.1)

sd.wait()
print("\n\n ⏹️  Recording complete. Processing wave data...")
wav.write("output.wav", SAMPLE_RATE, recording)

# ==========================================
# 5. TRANSLATION ENGINE & BOX-OUTPUT
# ==========================================
recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

print(" 🔄 Querying Speech Engine...")

try:
    # Erkennung
    text = recognizer.recognize_google(audio, language=src_code)
    
    # Übersetzung
    translated = GoogleTranslator(source=src_code, target=dest_code).translate(text)
    
    # Ausgabe in einer stylischen Resultat-Box
    print("\n╔" + "═"*57 + "╗")
    print("║" + " TRANSLATION RESULTS ".center(57, "█") + "║")
    print("╠" + "═"*57 + "╣")
    print(f"║  ORIGINAL [{src_cc}]:".ljust(58) + "║")
    print(f"║  » \"{text}\"".ljust(58) + "║")
    print("║" + "─"*57 + "║")
    print(f"║  TRANSLATION [{dest_cc}]:".ljust(58) + "║")
    print(f"║  » \"{translated}\"".ljust(58) + "║")
    print("╚" + "═"*57 + "╝\n")

except sr.UnknownValueError:
    print("\n ❌ [ERROR]: Audio was too quiet or unclear. Please try again.")
except sr.RequestError:
    print("\n ❌ [API ERROR]: Google Speech API is offline or rate-limited.")
except Exception as e:
    print(f"\n ❌ [CRITICAL ERROR]: {e}")