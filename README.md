# 🤖 Jimmy – Desktop AI Assistant  
### A 3D Animated AI Companion with Voice, Vision & System Control

---

## 🧠 Overview

**Jimmy** is a Desktop AI Assistant featuring a fully animated 3D avatar that lives on your desktop.  

It combines the intelligence of a Large Language Model (LLM) with real-time voice interaction, Spotify control, system automation, and multimodal vision capabilities.

Built using **Python (PyQt6)** and **Three.js**, Jimmy bridges desktop-level control with modern web-based 3D rendering.

---

## ✨ Core Capabilities

### 🗣️ Voice & Personality

- Wake word support (e.g., *"Hey Jimmy"*)
- Real-time speech recognition
- Natural speech synthesis responses
- LLM-powered conversations (Google Gemini / Local Ollama)
- Consistent personality and contextual memory

#### Avatar States
- 💤 Idle – Breathing & subtle motion
- 🧠 Thinking – Processing animations
- 🗨️ Talking – Tail wag & gestures
- 💃 Dancing – Reacts to music playback

---

### 🎵 Spotify Integration

- ▶️ Play / Pause / Skip tracks
- 🔍 Search & queue songs ("Play some jazz")
- 🔊 Volume adjustment
- 💃 Automatic dance mode when music plays

---

### 🖥️ System Automation

- Open & close applications
- Adjust system volume & screen brightness
- Battery & system info reporting
- Screenshot capture via voice command

---

### 👁️ Multimodal Vision (Gemini Powered)

Jimmy can:
- Take a screenshot of your desktop
- Analyze what’s on your screen
- Explain code, UI, documents, or images
- Answer questions about what you're viewing

Example:
> "Jimmy, what is on my screen?"  
> "Explain this code."

---

### 🔵 Bluetooth "Jabba" Connection

- Automatically connects to a Bluetooth device named **"Jabba"**
- Designed for custom peripherals or external speakers

---

## 🎭 Visual Representation

Jimmy is rendered in a transparent PyQt WebEngine window, allowing it to float on the desktop.

### 3D Avatar (Jimmy)

<p align="center">
  <img width="1100" height="529" alt="Screenshot 2026-02-14 211714" src="https://github.com/user-attachments/assets/c987e2dd-c29e-4181-b9e6-5a2c968f84d2" />
</p>

- Auto-scaling model loading  
- Bone-based procedural animation  
- Real-time state switching (Idle, Thinking, Talking, Dancing)  

### 🐍 Backend (Python)

| File | Responsibility |
|------|---------------|
| `main.py` | Application orchestrator |
| `modules/llm.py` | LLM abstraction layer |
| `modules/gemini_llm.py` | Gemini API integration |
| `modules/voice.py` | Speech recognition & TTS |
| `modules/spotify_client.py` | Spotify API interaction |
| `modules/system_control.py` | OS-level automation |

Framework:
- PyQt6 (GUI)
- PyQt WebEngine (Embedded web rendering)

---

### 🌐 Frontend (HTML / JavaScript)

| File | Responsibility |
|------|---------------|
| `modules/avatar_view.html` | 3D rendering interface |

Technologies:
- Three.js
- GLTF Loader
- WebGL Rendering

---

## 🎭 3D Avatar System

### Model: `Jimmy.glb`

Features:

- Auto-scaling to fit window dynamically
- Transparent floating desktop window
- Procedural bone animation
- Tail, Neck, and Spine bone detection
- Breathing animation
- Head bobbing
- Dance motion during music playback

The avatar is rendered in a transparent PyQt WebEngine window, allowing it to float seamlessly on the desktop.

---

## 🛠️ Tech Stack

### Backend
- Python 3.x
- PyQt6
- PyQt WebEngine
- Google Gemini API
- Ollama (optional local LLM)

### Frontend
- HTML
- JavaScript
- Three.js

### APIs
- Spotify Web API
- Gemini Multimodal API

---

## 🔄 System Flow

1. Wake word detected
2. Voice command captured
3. LLM processes intent
4. If system command → Execute via OS module
5. If Spotify command → API call
6. If vision command → Screenshot + Gemini Vision analysis
7. Avatar animation updates based on state

---

## 🚀 Features Summary

- 🎙️ Voice-controlled AI assistant
- 🤖 3D animated avatar
- 🎵 Spotify integration
- 🖥️ System automation
- 👁️ Multimodal screen analysis
- 🔵 Bluetooth device auto-connection
- 💬 Intelligent contextual conversations

---

## 🔮 Future Enhancements

- Custom wake-word training
- Emotion-based animation blending
- Multi-device synchronization
- Plugin architecture for new skills
- Cross-platform packaging (Windows/Mac/Linux installer)

---

