import os, sys, time, random
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator

# ==========================================
# 1. CONFIGURATION & ALL WORDS DATA
# ==========================================
DURATION = 4  # Recording duration in seconds
SAMPLE_RATE = 44100

# Mapping for language codes
LANG_MAPPING = {
    "de": ("German", "DE-de"),
    "en": ("English", "EN-us"),
    "ru": ("Russian", "RU-ru")
}

LEVEL_MAPPING = {
    "1": "easy",
    "2": "medium",
    "3": "hard"
}

words_by_level = {
    "de": {
        "easy": ["katze", "hund", "apfel", "milch", "sonne"],
        "medium": ["banane", "schule", "freund", "fenster", "gelb"],
        "hard": ["technologie", "universität", "information", "aussprache", "fantasie"]
    },
    "en": {
        "easy": ["cat", "dog", "apple", "milk", "sun"],
        "medium": ["banana", "school", "friend", "window", "yellow"],
        "hard": ["technology", "university", "information", "pronunciation", "imagination"]
    },
    "ru": {
        "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
        "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
        "hard": ["технология", "университет", "информация", "произношение", "воображение"]
    }
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# 2. ONE-LINE INPUT SYSTEM
# ==========================================
clear_screen()
print("╔" + "═"*57 + "╗")
print("║" + " 🎯 MULTI-LANG: SPEAK RIGHT! 🎯 ".center(57, " ") + "║")
print("╚" + "═"*57 + "╝\n")

print(" Available languages: de, en, ru")
print(" Difficulty levels: 1 (Easy), 2 (Medium), 3 (Hard)\n")
print(" 👉 Format: [From] [To] [Level] (e.g., ru en 1)")

while True:
    try:
        user_input = input(" ► Enter setup: ").strip().lower()
        src_code, dest_code, lvl_num = user_input.split()
        
        if src_code in LANG_MAPPING and dest_code in LANG_MAPPING and lvl_num in LEVEL_MAPPING:
            src_name, _ = LANG_MAPPING[src_code]
            dest_name, dest_speech_code = LANG_MAPPING[dest_code]
            level = LEVEL_MAPPING[lvl_num]
            break
        else:
            print(" ❌ Invalid language codes or level! Please try again.")
    except ValueError:
        print(" ❌ Wrong format! Please enter 3 values separated by spaces (e.g., ru en 1).")

print(f"\n ✔ {src_name} ➔ {dest_name} ({level.upper()}) loaded! Starting the game...")
time.sleep(1.5)

# ==========================================
# 3. MAIN GAME LOOP
# ==========================================
score = 0
total_errors = 0  # Tracking errors for the summary

current_words = words_by_level[src_code][level].copy()
random.shuffle(current_words)

for word in current_words:
    clear_screen()
    print(f" Current Score: {score} Points")
    print("─"*59)
    
    try:
        correct_answer = GoogleTranslator(source=src_code, target=dest_code).translate(word).lower().strip()
    except Exception:
        correct_answer = "" 
    
    print("\n╔" + "═"*57 + "╗")
    print(f"║  Translate and SPEAK this word in {dest_name}:".ljust(56) + "║")
    print(f"║  👉  {word.upper()}".ljust(58) + "║")
    print("╚" + "═"*57 + "╝\n")
    
    for countdown in range(5, 0, -1):
        sys.stdout.write(f"\r ⏳ Recording starts in {countdown} sec... Get ready! ")
        sys.stdout.flush()
        time.sleep(1)
    
    print("\n")
    
    # Audio Recording
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    
    bar_length = 30
    for elapsed in range(DURATION * 10 + 1):
        percent = elapsed / (DURATION * 10)
        filled_length = int(bar_length * percent)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        rem_time = max(0.0, DURATION - (elapsed / 10))
        
        sys.stdout.write(f"\r 🔴 SPEAK NOW: [{bar}] {int(percent*100)}% | Rem: {rem_time:.1f}s ")
        sys.stdout.flush()
        time.sleep(0.1)
        
    sd.wait()
    print("\n\n ⏹️  Recording finished. Processing audio data...")
    wav.write("game_output.wav", SAMPLE_RATE, recording)
    
    # Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile("game_output.wav") as source:
        audio = recognizer.record(source)
        
    print(" 🔄 Checking pronunciation...")
    
    try:
        recognized = recognizer.recognize_google(audio, language=dest_speech_code).lower().strip()
        
        print(f"\n Detected: \"{recognized}\"")
        print(f" Expected : \"{correct_answer}\"")
        
        if recognized == correct_answer:
            print("\n 🎉 CORRECT! Great pronunciation! +10 Points 🎉")
            score += 10
        else:
            print("\n ❌ Incorrect or unclear. -1 Point!")
            score -= 1
            total_errors += 1
            
    except sr.UnknownValueError:
        print("\n ❌ Could not understand the audio. -1 Point")
        score -= 1
        total_errors += 1
    except sr.RequestError:
        print("\n ❌ [API ERROR]: Google Engine is offline.")
        
    user_command = input("\n [Enter] Continue | (Type /score for your score): ").strip().lower()
    
    if user_command == "/score":
        print("\n╔" + "═"*57 + "╗")
        print(f"║ 📊 CURRENT SCORE: {score} Points".ljust(56) + "║")
        print("╚" + "═"*57 + "╝")
        input("\n [Enter] Press Enter to continue...")

# ==========================================
# 4. GAME OVER SCREEN
# ==========================================
clear_screen()
print("╔" + "═"*57 + "╗")
print("║" + " 🔥 GAME OVER 🔥 ".center(57, " ") + "║")
print("╠" + "═"*57 + "╣")
print(f"║  Final Score: {score} Points".ljust(56) + "║")
print(f"║  Total Mistakes: {total_errors}".ljust(56) + "║")
print("╠" + "═"*57 + "╣")
if total_errors == 0:
    print("║  🎉 Perfect! Flawless run! 🎉".ljust(54) + "║")
else:
    print("║  Good job! Keep practicing to minimize mistakes! 💪".ljust(56) + "║")
print("╚" + "═"*57 + "╝\n")