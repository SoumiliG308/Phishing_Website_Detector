## 🛡️ Phishing Website Detector

A simple **Streamlit web app** that detects whether a given website URL is **legitimate or phishing** using a trained Machine Learning model.

## 🚀 Features
- Real-time URL structure analysis  
- Manual checks for reputation and behavior  
- AI-powered classification using Random Forest Algorithm 
- Clean and responsive UI built with Streamlit  

## 🧠 How It Works
The app extracts important URL features (like HTTPS usage, subdomains, redirects, URL length etc.), combines them with user inputs, and predicts whether a website is **phishing** or **legitimate** based on a trained ML model.

## 🧩 Files Included
- `phishing_app.py` → Main Streamlit application  
- `my_phishing_detector.pkl` → Trained ML model
- `feature_names.pkl` → Features used to train the model  
- `ui.css` → Custom UI styling   

## ⚙️ Installation Process
1. Clone this repository  
   ```bash
   git clone https://github.com/SoumiliG308/phishing-website-detector.git
   cd phishing-website-detector
2. Install dependencies
   ```bash
    pip install -r requirements.txt
3. Run the app
   ```bash
    streamlit run phishing_app.py

## 📦 Model Info
The model was trained using Random Forest on phishing datasets with extracted URL-based features.

## 💡 Disclaimer
This tool is for educational purposes only and should not replace professional cybersecurity checks.

- Developed by Soumili Ghosh ✨