# The IBM AI International Racing League

This repository features an autonomous driving agent developed for **TORCS (The Open Racing Car Simulator)**. The project demonstrates a modular control architecture optimized through **IBM Granite AI** insights, balancing high-speed performance with robust stability on complex tracks like the **Corkscrew**.



## 🎯 Project Objectives
* **AI Integration:** Implementing decision-making logic informed by IBM Granite to optimize racing lines and speed management.
* **Control Engineering:** Developing a responsive modular controller using Python.
* **Robustness:** Ensuring the bot can recover from collisions or "wrong way" scenarios automatically.

## 🛠 Technical Architecture

The system follows a classic **Perception-Planning-Action** loop:

### 1. Perception (Sensor Fusion)
The bot processes a 19-range track sensor array to map the environment. It calculates real-time variables such as:
* **Track Position:** Deviation from the center line.
* **Angle:** The car's orientation relative to the track axis.
* **WheelSpin:** Detecting traction loss for active intervention.

### 2. Planning (IBM Granite Optimized Logic)
Instead of simple heuristics, the logic is segmented into:
* **Dynamic Speed Categorization:** Adjusting target speeds based on look-ahead distance (e.g., 75 km/h for 90-degree hairpins, 300 km/h for straights).
* **Predictive Braking:** Initiating deceleration at 75m markers to ensure stable corner entry.

### 3. Action (Actuation)
* **Steering:** A PID-inspired controller that combines angle correction with aggressive edge protection.
* **Throttle:** Traction-controlled acceleration to prevent power-sliding out of corners.
* **Gears:** An RPM-based shifting logic (up-shift at 9200 RPM, down-shift at 3800 RPM).

## 🏎️ Racing Demo
![Autonomous Driving on Corkscrew](docs/IBM_racecar_300126 - Compressed with FlexClip.mp4)


## 📂 Project Structure
```text
.
├── driver.py           # Core autonomous logic and modular controller
├── client.py           # Network protocol and server communication
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
