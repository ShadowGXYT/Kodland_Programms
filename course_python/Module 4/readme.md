# 🎯 Multi-Lang: Speak Right!

An interactive, voice-controlled command-line game designed to train and check your pronunciation across multiple languages. The project uses speech recognition and live translation APIs to evaluate user input dynamically.

---

## 🚀 Features

* **One-Line Dynamic Setup:** Start the game instantly by defining your configuration in a single line (e.g., `ru en 1` for Russian → English on Easy mode).
* **Multi-Language Support:** Practice cross-translation between German (`de`), English (`en`), and Russian (`ru`).
* **Live Translation Engine:** Uses `deep-translator` to translate vocabulary words in real time.
* **Smart Speech Recognition:** Utilizes the Google Speech Recognition API adjusted dynamically to your target language.
* **Interactive CLI Interface:** Features clean ASCII borders, status bars, and a live loading animation during voice recording.
* **Built-in Game Mechanics:** Includes a countdown warning before recording, point tracking, penalty points for wrong answers, and custom text commands like `/score`.

---

## 🛠️ Requirements & Installation

Before running the game, make sure you have Python installed along with the required libraries.

### 1. Clone the repository or download the source code

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

### 2. Install the necessary dependencies

```bash
pip install sounddevice numpy scipy SpeechRecognition deep-translator
```

> ⚠️ **Note:** You also need a working microphone connected to your system and an active internet connection for the translation and speech recognition APIs to function correctly.

---

## 🎮 How to Play

### 1. Run the Python script

```bash
python new_bot.py
```

### 2. Configure your session

Enter your setup in the following format:

```text
[From Language Code] [To Language Code] [Difficulty Level (1-3)]
```

#### Examples

```text
ru en 1
```

Translate from Russian to English on **Easy** difficulty.

```text
de ru 3
```

Translate from German to Russian on **Hard** difficulty.

### 3. Follow the game flow

1. **Look at the prompt** – The game displays a word.
2. **Prepare to speak** – A 5-second countdown gives you time to think.
3. **Speak clearly** – When the 🔴 **SPEAK NOW** indicator appears with the live progress bar, say the translated word into your microphone.
4. **Check the results** – The system processes your speech and evaluates your pronunciation.

   * ✅ Correct answer: **+10 points**
   * ❌ Incorrect answer: **−1 point**
5. **Use control commands**

   * Press `Enter` to continue to the next round.
   * Type `/score` to view your current score.

---

## 📂 Code Structure

### Configuration

* Audio sample rates
* Recording durations
* Official word matrices
* Difficulty-based vocabulary lists
* Language mappings

### Input Validation

A robust parsing system that:

* Splits the user's setup line
* Validates language codes
* Checks difficulty levels
* Handles invalid input gracefully without crashing

### Main Game Loop

The core game sequence:

```text
Translation
    ↓
UI Countdown
    ↓
Audio Recording
    ↓
Speech-to-Text Recognition
    ↓
Answer Comparison
    ↓
Score Update
```

### Game Over Screen

Displays a final performance summary including:

* Final score
* Total mistakes
* Overall performance evaluation

---

## 🎓 Course Assignment Context

This project was developed as part of the **Kodland Python Course** (**Module 4 – Project 2**).

The implementation satisfies all required evaluation criteria, including:

* Multiple difficulty levels
* Point-based scoring system
* Error handling and validation
* Comprehensive user feedback
* Emoji and ASCII-enhanced interface
* Custom creative features beyond the minimum requirements

---

## 📜 License

This project was created for educational purposes as part of the Kodland Python Course.

Feel free to modify and improve it for personal learning and development.
