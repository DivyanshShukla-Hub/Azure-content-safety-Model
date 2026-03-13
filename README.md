# Azure-content-safety-Model
# 🛡️ Multi-Modal AI Content Safety Dashboard

A professional-grade web application built to analyze both **Text** and **Images** for harmful content using **Microsoft Azure AI Content Safety**. Designed with a modern, responsive UI using **Streamlit**.

This project demonstrates the real-time application of cloud-based machine learning models in content moderation, vision AI, and cybersecurity.

## ✨ Key Features
* **Multi-Modal Analysis:** Seamlessly toggle between scanning text strings or uploading image files (`.jpg`, `.png`).
* **Real-Time Risk Scoring:** Instantly scores content across four critical hazard categories: Hate, Self-Harm, Sexual, and Violence (Severity 0-6).
* **Interactive Dashboard:** Features a clean, tabbed interface utilizing Streamlit metric cards for clear visual feedback and risk assessment.
* **Smart Session Memory:** Automatically tracks and securely stores recent scan history during the active session, tagged with media type icons (📝/🖼️).
* **Enterprise UI:** Custom branding integration highlighting technology providers and university affiliations.

## 🛠️ Technologies Used
* **Backend:** Microsoft Azure AI Content Safety API (Text & Vision Models)
* **Frontend:** Streamlit 
* **Language:** Python

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DivyanshShukla-Hub/Azure-content-safety-Model.git

2. Install the required dependencies:
   
       Bash
       pip install -r requirements.txt
   
3. Add your Azure Credentials:
You will need an active Azure AI Content Safety resource. You can input your Endpoint and API Key directly into the app's secure sidebar.

4.Run the application:

     Bash
    streamlit run app.py


#Acknowledgments

A special thanks to my mentor, Mr. Abhimanyu Sharma (ByteXL Faculty), for his continued guidance and support on this project, and to Chandigarh University for fostering an environment of innovation.
