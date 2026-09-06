<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# [Project Name] 🎯


## Basic Details
### Team Name: Medillin


### Team Members
- Team Lead: Gautham R - SCMS School of Engineering and Technology
- Member 2: Goutham G Nair - SCMS School of Engineering and Technology

### Project Description
Shoe Dirt calculator

### The Problem (that doesn't exist)
Living room carpets face existential dread daily from footwear bearing outdoor grime. Entering a household requires an uncomfortably polite verbal exchange about whether shoes stay on or come off. Humanity suffers from the tragic lack of a cold, unforgiving digital authority to publicly humiliate guests before their soles touch sacred indoor fabric.

### The Solution (that nobody asked for)
Shoe Dirt Calculator & Living Room Bouncer: An AI-powered threshold gatekeeper. Guests hold their footwear up to a camera, and a judgmental vision model calculates the exact dirt percentage down to the decimal point. If the grime level exceeds safety tolerances, the system formally denies entry with exaggerated hazard warnings and a tailored roast.

## Technical Details
### Technologies/Components Used
For Software:

    Languages used: Python

    Frameworks used: Streamlit

    Libraries used: google-genai (Gemini Vision API / gemini-2.5-flash), pydantic, pillow, python-dotenv

    Tools used: Visual Studio Code, Git

For Hardware:

    Laptop or smartphone webcam / integrated camera

    Internet connectivity for Gemini API calls


### Implementation
For Software:
# Installation
cd D:\medellin\medellin_useless_project
pip install streamlit google-genai pillow pydantic python-dotenv

# Run
streamlit run app.py

### Project Documentation
For Software:

# Screenshots (Add at least 3)
![Screenshot1]: https://drive.google.com/file/d/1KquLlEW2nVtpKjAsAQV7M2AppjaOFmE8/view?usp=sharing
caption: Shoe scanning in progress with live status updates and model retry logs.

![Screenshot2]: https://drive.google.com/file/d/11FhiAgJ5PPWiy0OxDdR2wQY2Fyr9a8zK/view?usp=sharing
caption: Final analysis results showing a 0% dirt score and roast card.

# Diagrams
https://drive.google.com/file/d/1UFuX1sEAoSuPIfTziUsxvdFWlyltLpA8/view?usp=sharing
short explanation: Capture & Upload: The user shows their shoe to the webcam or uploads a photo through the Streamlit interface.
AI Dirt Scan: The image is sent to Gemini 2.5 Flash, which analyzes the sole and fabric to estimate the exact dirt percentage.
Structured Response: The API returns clean JSON data containing the score, verdict, and custom roast.
Bouncer Decision:
Under 20% dirt → Allowed inside (Sterile Royalty).
20% to 50% dirt → Warning issued (Civilian Walker).
50% or above → Entry denied (Biohazard Level 2).
UI Display: The app flashes the final verdict, displays the dirt gauge, and serves the comedic roast on screen.


## Team Contributions
- Team Member 1: Streamlit UI development, neon sensory-overload frontend styling, and camera integration.
- Team Member 2: Gemini Vision API setup, Pydantic schema enforcement, system prompt engineering, and environment/security management.

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



