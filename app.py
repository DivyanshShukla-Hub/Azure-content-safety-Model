import streamlit as st
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, AnalyzeImageOptions, ImageData
from azure.core.exceptions import HttpResponseError
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Azure Content Safety", page_icon="🛡️", layout="wide")

# --- Initialize Session State for History ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Helper Functions ---
def analyze_text(text_to_analyze, api_endpoint, api_key):
    """Calls Azure API to analyze text."""
    client = ContentSafetyClient(api_endpoint, AzureKeyCredential(api_key))
    request = AnalyzeTextOptions(text=text_to_analyze)
    try:
        response = client.analyze_text(request)
        return response, None
    except HttpResponseError as e:
        return None, f"Azure API Error: {e.error.message if e.error else str(e)}"
    except Exception as e:
        return None, f"Unexpected Error: {str(e)}"

def analyze_image(image_bytes, api_endpoint, api_key):
    """Calls Azure API to analyze an image."""
    client = ContentSafetyClient(api_endpoint, AzureKeyCredential(api_key))
    request = AnalyzeImageOptions(image=ImageData(content=image_bytes))
    try:
        response = client.analyze_image(request)
        return response, None
    except HttpResponseError as e:
        return None, f"Azure API Error: {e.error.message if e.error else str(e)}"
    except Exception as e:
        return None, f"Unexpected Error: {str(e)}"

def get_risk_label(severity):
    """Maps severity integer to a readable string."""
    labels = {0: "Safe", 2: "Low Risk", 4: "Medium Risk", 6: "High Risk"}
    return labels.get(severity, "Unknown")

# --- Sidebar (Settings) ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("Enter your Azure credentials.")
    endpoint = st.text_input("Azure Endpoint URL", type="password")
    key = st.text_input("Azure API Key", type="password")
    
    st.markdown("---")
    if st.button("Clear History", use_container_width=True):
        st.session_state.history = []
        st.success("History cleared!")

# --- Main UI ---
# Create columns to push the Azure logo to the top right
header_col1, header_col2 = st.columns([5, 1])

with header_col1:
    st.title("🛡️ AI Content Safety Dashboard")
    st.markdown("Powered by **Microsoft Azure**, **Chandigarh University**, and **ByteXL**")
    st.markdown("Designed and implemented by **Divyansh Shukla**")

with header_col2:
    try:
        # Pinned Azure Logo 
        st.image("5678876674654.jpg", use_container_width=True)
    except:
        st.error("Missing: 5678876674654.jpg")

st.markdown("---")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Analyze Content", "📜 Analysis History", "👨‍💻 About the Developer"])

# --- TAB 1: Analysis ---
with tab1:
    # --- NEW: Choose Text or Image ---
    analysis_type = st.radio("Choose Input Type:", ["Text", "Image"], horizontal=True)
    st.markdown("---")

    if analysis_type == "Text":
        st.markdown("Enter text to check for Hate, Self-Harm, Sexual, or Violent content.")
        user_input = st.text_area("User Input", placeholder="Type or paste text here...", height=150)

        if st.button("Analyze Text", type="primary", use_container_width=True):
            if not endpoint or not key:
                st.error("⚠️ Please provide your Azure Endpoint and API Key in the sidebar.")
            elif not user_input.strip():
                st.warning("⚠️ Please enter some text to analyze.")
            else:
                with st.spinner("Scanning text securely with Azure..."):
                    results, error = analyze_text(user_input, endpoint, key)
                    
                    if error:
                        st.error(error)
                    elif results:
                        st.success("Scan Complete!")
                        
                        # Store in history
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        analysis_data = {"input_type": "Text", "text": user_input, "time": timestamp, "scores": {}}
                        
                        st.subheader("Safety Report")
                        cols = st.columns(4)
                        max_severity = 0
                        
                        for i, category_result in enumerate(results.categories_analysis):
                            cat_name = category_result.category
                            sev = category_result.severity
                            label = get_risk_label(sev)
                            
                            analysis_data["scores"][cat_name] = f"{sev} ({label})"
                            max_severity = max(max_severity, sev)
                            
                            with cols[i % 4]:
                                st.metric(label=cat_name, value=label, delta=f"Score: {sev}", delta_color="inverse")
                        
                        st.session_state.history.insert(0, analysis_data) 
                        
                        if max_severity > 0:
                            st.error(f"🚨 **Action Required:** Content flagged with a maximum severity of {max_severity}.")
                        else:
                            st.info("✅ This content appears safe across all categories.")

    elif analysis_type == "Image":
        st.markdown("Upload an image to check for Hate, Self-Harm, Sexual, or Violent content.")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Show a small preview of the image
            st.image(uploaded_file, caption="Image Preview", width=300)

            if st.button("Analyze Image", type="primary", use_container_width=True):
                if not endpoint or not key:
                    st.error("⚠️ Please provide your Azure Endpoint and API Key in the sidebar.")
                else:
                    with st.spinner("Scanning image securely with Azure Vision AI..."):
                        # Convert uploaded file to bytes for the API
                        image_bytes = uploaded_file.getvalue()
                        results, error = analyze_image(image_bytes, endpoint, key)
                        
                        if error:
                            st.error(error)
                        elif results:
                            st.success("Scan Complete!")
                            
                            # Store in history
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            analysis_data = {"input_type": "Image", "text": f"[Uploaded File: {uploaded_file.name}]", "time": timestamp, "scores": {}}
                            
                            st.subheader("Safety Report")
                            cols = st.columns(4)
                            max_severity = 0
                            
                            for i, category_result in enumerate(results.categories_analysis):
                                cat_name = category_result.category
                                sev = category_result.severity
                                label = get_risk_label(sev)
                                
                                analysis_data["scores"][cat_name] = f"{sev} ({label})"
                                max_severity = max(max_severity, sev)
                                
                                with cols[i % 4]:
                                    st.metric(label=cat_name, value=label, delta=f"Score: {sev}", delta_color="inverse")
                            
                            st.session_state.history.insert(0, analysis_data) 
                            
                            if max_severity > 0:
                                st.error(f"🚨 **Action Required:** Image flagged with a maximum severity of {max_severity}.")
                            else:
                                st.info("✅ This image appears safe across all categories.")

# --- TAB 2: History ---
with tab2:
    st.header("Recent Analyses")
    if not st.session_state.history:
        st.caption("No history yet. Analyze some text or images to see it here!")
    else:
        for item in st.session_state.history:
            icon = "🖼️" if item.get('input_type') == "Image" else "📝"
            with st.expander(f"{icon} Scanned at {item['time']}"):
                st.markdown(f"**Input Data ({item.get('input_type', 'Text')}):**")
                st.write(f"> {item['text']}")
                st.markdown("**Scores:**")
                for category, score in item['scores'].items():
                    st.write(f"- **{category}:** {score}")

# --- TAB 3: About the Developer ---
with tab3:
    st.header("Project & Developer Info")
    
    # Display Logos at the top
    logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
    with logo_col1:
        try:
            st.image("5354677586.jpeg", width=150)
        except:
            st.error("Missing: 5354677586.jpeg")
    with logo_col3:
        try:
            st.image("222347686872.jpeg", width=150)
        except:
            st.error("Missing: 222347686872.jpeg")
            
    st.markdown("---")
    
    # Developer Profile Section
    prof_col1, prof_col2 = st.columns([1, 3])
    
    with prof_col1:
        try:
            st.image("1773242404994.jpg", width=200)
        except:
            st.error("Missing: 1773242404994.jpg")
            
    with prof_col2:
        st.subheader("Divyansh Shukla")
        st.markdown("**B.Tech Computer Science (AI & ML)**")
        st.markdown("*Chandigarh University*")
        st.markdown("📧 [divyanshshukla765@gmail.com](mailto:divyanshshukla765@gmail.com)")
        st.markdown("🔗 [Divyansh Shukla | LinkedIn](https://www.linkedin.com/in/divyansh-shukla-cuuniversity/)") 
        
    st.markdown("---")
    
    # Acknowledgements / Mentor Section
    st.subheader("Acknowledgments")
    st.markdown("A special thanks to my mentor for their guidance and support on this project:")
    st.markdown("**Mr. Abhimanyu Sharma**")
    st.markdown("*ByteXL Faculty*")
    st.markdown("🔗 [Abhimanyu Sharma | LinkedIn](https://www.linkedin.com/in/017abhimanyu/)")