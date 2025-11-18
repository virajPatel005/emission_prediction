# app.py
# === NOISE POLLUTION PREDICTION APP ===

import streamlit as st
import pandas as pd
import joblib
import numpy as np

# -----------------------------
# Load trained model
# -----------------------------
lgb_model = joblib.load("lgb_model_2.pkl")

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="Noise Pollution Predictor", 
    page_icon="🔊", 
    layout="centered"
)

# -----------------------------
# Custom HTML/CSS Header
# -----------------------------
header_html = """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 30px; 
            border-radius: 15px; 
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h1 style="color: white; font-size: 3em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
        🔊 Noise Pollution Predictor
    </h1>
    <p style="color: #f0f0f0; font-size: 1.2em; margin-top: 10px;">
        Analyze environmental noise levels and protect your health
    </p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# -----------------------------
# Display image from URL
# -----------------------------
st.image(
    "https://images.unsplash.com/photo-1573152143286-0c422b4d2175?w=800",
    caption="Urban Noise Pollution Monitoring",
    use_container_width=True
)

# Alternative: Display local image (uncomment if you have a local file)
# st.image("noise_pollution.jpg", caption="Noise Pollution", use_container_width=True)

st.markdown("""
Enter location and environmental details to predict noise pollution levels 
and get personalized health recommendations.
""")

# -----------------------------
# User Input Section
# -----------------------------
st.header("📍 Input Location & Environmental Data")

col1, col2 = st.columns(2)

with col1:
    Latitude = st.number_input("Latitude", -90.0, 90.0, 19.0760)
    Longitude = st.number_input("Longitude", -180.0, 180.0, 72.8777)
    Month = st.slider("Month", 1, 12, 6)
    
    # User-friendly day selection
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected_day = st.selectbox("Day of Week", day_names, index=2)
    DayOfWeek = day_names.index(selected_day)  # Convert to 0-6
    
    UrbanTier = st.selectbox("Urban Tier", [1, 2, 3], help="1=Metro, 2=City, 3=Town")
    Wind_m_s = st.number_input("Wind Speed (m/s)", 0.0, 20.0, 5.0)

with col2:
    EventFlag = st.selectbox("Special Event?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    PopTraffic = st.number_input("Population Traffic Index", 0.0, 100000.0, 5000.0)
    IndustrialRoad = st.number_input("Industrial/Road Proximity Index", 0.0, 10000.0, 500.0)
    TempHumidity = st.number_input("Temperature × Humidity", 0.0, 1000.0, 300.0)

# -----------------------------
# Calculate cyclical encoding for DayOfWeek
# -----------------------------
DayOfWeek_sin = np.sin(2 * np.pi * DayOfWeek / 7)
DayOfWeek_cos = np.cos(2 * np.pi * DayOfWeek / 7)

# -----------------------------
# Prepare input data for model
# -----------------------------
input_data = pd.DataFrame({
    "Latitude": [Latitude],
    "Longitude": [Longitude],
    "Month": [Month],
    "DayOfWeek": [DayOfWeek],
    "UrbanTier": [UrbanTier],
    "Wind_m_s": [Wind_m_s],
    "EventFlag": [EventFlag],
    "PopTraffic": [PopTraffic],
    "IndustrialRoad": [IndustrialRoad],
    "TempHumidity": [TempHumidity],
    "DayOfWeek_sin": [DayOfWeek_sin]
})

# -----------------------------
# Prediction Button
# -----------------------------
if st.button("🔮 Predict Noise Levels", type="primary", use_container_width=True):
    
    # Make prediction
    prediction = lgb_model.predict(input_data)
    day_noise = prediction[0][0]
    night_noise = prediction[0][1]

    # -----------------------------
    # Custom HTML Results Display
    # -----------------------------
    results_html = f"""
    <div style="background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
                padding: 25px;
                border-radius: 12px;
                margin: 20px 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <h2 style="color: white; text-align: center; margin-bottom: 20px;">📊 Prediction Results</h2>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div style="background: white; padding: 20px; border-radius: 10px; min-width: 200px; margin: 10px;">
                <h3 style="color: #4facfe; text-align: center;">☀️ Day Noise</h3>
                <p style="font-size: 2.5em; font-weight: bold; text-align: center; color: #333; margin: 10px 0;">
                    {day_noise:.1f} dB
                </p>
            </div>
            <div style="background: white; padding: 20px; border-radius: 10px; min-width: 200px; margin: 10px;">
                <h3 style="color: #667eea; text-align: center;">🌙 Night Noise</h3>
                <p style="font-size: 2.5em; font-weight: bold; text-align: center; color: #333; margin: 10px 0;">
                    {night_noise:.1f} dB
                </p>
            </div>
        </div>
    </div>
    """
    st.markdown(results_html, unsafe_allow_html=True)
    
    st.markdown("---")

    # Determine pollution levels
    def get_pollution_level(noise_db, time_period="day"):
        if time_period == "day":
            if noise_db < 55:
                return "Low", "🟢", "safe"
            elif noise_db < 70:
                return "Moderate", "🟡", "warning"
            else:
                return "High", "🔴", "danger"
        else:
            if noise_db < 45:
                return "Low", "🟢", "safe"
            elif noise_db < 60:
                return "Moderate", "🟡", "warning"
            else:
                return "High", "🔴", "danger"

    day_level, day_icon, day_status = get_pollution_level(day_noise, "day")
    night_level, night_icon, night_status = get_pollution_level(night_noise, "night")

    # Day & Night Assessment
    st.subheader(f"{day_icon} Day Noise Assessment: {day_level}")
    st.subheader(f"{night_icon} Night Noise Assessment: {night_level}")

    # Health Effects
    st.header("⚠️ Potential Health Effects")
    if day_status == "danger" or night_status == "danger":
        st.markdown("""
        **Severe Health Risks:**
        - 🧠 Cognitive Impairment
        - 😫 Stress & Anxiety
        - ❤️ Cardiovascular Issues
        - 😴 Sleep Disruption
        - 👂 Hearing Damage
        - 👶 Child Development Problems
        """)
    elif day_status == "warning" or night_status == "warning":
        st.markdown("""
        **Moderate Health Concerns:**
        - 😟 Increased stress and irritability
        - 😪 Mild sleep disturbances
        - 🎯 Reduced focus and productivity
        - 💢 Headaches and fatigue
        - 📚 Learning difficulties
        """)
    else:
        st.markdown("""
        **Low Risk:**
        - ✅ Minimal health impact
        - 😊 Safe for living and working
        - 💤 Good sleep quality
        """)

    # Precautions
    st.header("🛡️ Recommended Precautions")
    if day_status == "danger" or night_status == "danger":
        st.markdown("""
        **Immediate Actions:**
        - 🏠 Soundproof indoor spaces
        - 👂 Wear ear protection
        - 🌳 Add vegetation or barriers
        - 🏥 Monitor health regularly
        - 📢 Report excessive noise
        """)
    elif day_status == "warning" or night_status == "warning":
        st.markdown("""
        **Preventive Measures:**
        - 🪟 Improve window insulation
        - 🌱 Add plants as sound barriers
        - 😴 Use earplugs while sleeping
        - ⏰ Avoid peak noise hours
        - 🔇 Create quiet zones at home
        """)
    else:
        st.markdown("""
        **Maintenance Tips:**
        - ✅ Continue monitoring noise levels
        - 🌳 Maintain green spaces
        - 🤝 Support community noise awareness
        """)

    st.markdown("---")
    with st.expander("ℹ️ About Noise Pollution Standards"):
        st.markdown("""
        **WHO Guidelines:**
        - Day (6 AM - 10 PM): <55 dB recommended, <70 dB acceptable
        - Night (10 PM - 6 AM): <45 dB recommended, <60 dB acceptable
        
        **Common Noise Levels:**
        - 30 dB: Whisper
        - 60 dB: Normal conversation
        - 85 dB: Heavy traffic
        - 100 dB: Nightclub
        - 120 dB: Jet takeoff
        """)

# -----------------------------
# Footer with custom HTML
# -----------------------------
footer_html = """
<div style="text-align: center; padding: 20px; margin-top: 40px; 
            background-color: #f0f2f6; border-radius: 10px;">
    <p style="color: #666; margin: 0;">
        Made with ❤️ for a quieter world | Data-driven noise pollution analysis
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)









# ============================================
# 🌍 FUTURE NOISE PREDICTIONS (HTML MAP)
# ============================================
st.header("🌍 Future Noise Trends (2025–2035)")

# Load HTML file
with open("future_noise_prediction_2025_2035.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Embed HTML
st.components.v1.html(html_content, height=800, scrolling=True)

st.markdown("---")



