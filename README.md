
# AI Vision Console 🤖✨

<p align="center">
  <img src="Dashboard.png" width="700" alt="Main Dashboard Interface">
</p>

This AI Vision Console is a centralized Python dashboard developed by Archit Yadav, designed to showcase the power of real-time computer vision. By integrating OpenCV, Mediapipe, and TensorFlow, the application features an interactive suite of projects including an Invisibility Cloak that utilizes color-based background substitution, an Air Canvas for touchless digital drawing via hand tracking, and an Emotion-based Music Player that curates playlists by analyzing facial expressions. Built with a clean, dark-themed Tkinter interface, the console serves as a professional portfolio piece that bridges advanced deep learning models with accessible, user-friendly desktop utility.

## 🌟 Feature Gallery

| 🎭 Emotion Detection | ✨ Invisibility Cloak | 🎨 Air Canvas |
| :---: | :---: | :---: |
| <img src="Emotion-Detection.png" width="250"> | <img src="Harry-Cloak.png" width="250"> | <img src="Air-Canvas.png" width="250"> |
| Real-time mood analysis | Color-based cloaking | Hand-tracking drawing |

## 🚀 Features

- **✨ Invisibility Cloak:** Uses color detection and background frame substitution to mimic the Harry Potter Invisibility Cloak.
- **🎨 Air Canvas:** Leveraging Mediapipe for hand tracking to draw on the screen in real-time.
- **🎵 Emotion Music Player:** Analyzes facial expressions to detect mood and suggest/play music accordingly.
- **🖥️ Centralized Dashboard:** A clean, dark-themed UI to launch all projects from one place.

## 🛠️ Technology Stack

- **Language:** Python 3.12
- **UI Framework:** Tkinter
- **Vision Libraries:** OpenCV, Mediapipe
- **Deep Learning:** TensorFlow / Keras (for emotion detection)

## 📦 Installation & Setup

Follow these steps to get the project running on your local machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ArchitYadav07/AI-Vision-App1.git](https://github.com/ArchitYadav07/AI-Vision-App1.git)
   cd AI-Vision-App1

```

2. **Create a Virtual Environment:**
```bash
python -m venv venv312

```


3. **Activate the Environment:**
* **Windows:** `.\venv312\Scripts\activate`
* **Mac/Linux:** `source venv312/bin/activate`


4. **Install Dependencies:**
```bash
pip install -r requirements.txt

```



## 🎮 How to Use

Run the main dashboard script:

```bash
python main_dashboard.py

```

* Select any project button to launch the camera window.
* **Tip:** Press `q` or `ESC` in any camera window to return to the main dashboard.

## 👤 Author

**Archit Yadav** [GitHub Profile](https://www.google.com/search?q=https://github.com/ArchitYadav07)

---

*Created for AI Vision exploration and Computer Vision learning.*

```

---

### 🛠️ Important Note on Image Paths


For the code above to work, your image files (`Dashboard.png`, `Emotion-Detection.png`, etc.) must be in the **root folder** of your repository (the same place as your `.py` files). 

* **If you put them in a folder** named `images`, change the code to `src="images/Dashboard.png"`.
* **Check File Extensions:** Ensure they are `.png` and not `.PNG` or `.jpg`, as GitHub is case-sensitive.

### 🚀 Final Step
Once you save this `README.md`, do one final push to see it live:
```powershell
git add README.md
git commit -m "Updated README with project screenshots"
git push origin main
