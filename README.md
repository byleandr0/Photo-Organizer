# Photo-Organizer
A professional, modular photo organizer. Features live image previews, automated conflict detection, and smart renaming for photographers.

# Photo Organizer

Welcome to the photo organization app!

## Why I built this
I work with multimedia and often deal with folders full of photos, exports and different image formats.
This project was created as a learning exercise to understand Python, file management and desktop UI development, while building something useful for a real creative workflow.

## 🏗️ Project Architecture
This application utilizes Object-Oriented Programming and is split into modular files:
- `main.py`: The entry point. Boots up the UI.
- `config.py`: Centralized settings (colors, image extensions).
- `organizer.py`: The Logic engine. Handles preview generation, conflict detection, and file movements safely.
- `ui.py`: The Graphical User Interface utilizing CustomTkinter for a modern, rounded, premium aesthetic.

## 🌟 Features
- **Live Preview Gallery:** Select any file in the list to see an immediate thumbnail preview powered by Pillow!
- **Conflict Management:** Before you overwrite anything, the app checks if files exist and flags them in red (⚠️ ALREADY EXISTS).
- **Safety First:** The "Organize Now" button is locked until a preview is generated, and a final confirmation dialog prevents accidents.
- **Premium UI:** Deep slate grays and warm golden accents create a relaxing, boutique user experience.

## 🚀 How to Run
Ensure you have the required dependencies:
`pip install customtkinter pillow`

Then, run the app:
`python main.py`
