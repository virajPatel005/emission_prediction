# app.py
# === NOISE POLLUTION PREDICTION APP ===

import streamlit as st
import pandas as pd
import joblib

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

st.title("🔊 Noise Pollution Predictor")
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
    DayOfWeek = st.slider("Day of Week (0=Monday, 6=Sunday)", 0, 6, 2)
    UrbanTier = st.selectbox("Urban Tier", [1, 2, 3], help="1=Metro, 2=City, 3=Town")
    Wind_m_s = st.number_input("Wind Speed (m/s)", 0.0, 20.0, 5.0)

with col2:
    EventFlag = st.selectbox("Special Event?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    PopTraffic = st.number_input("Population Traffic Index", 0.0, 100000.0, 5000.0)
    IndustrialRoad = st.number_input("Industrial/Road Proximity Index", 0.0, 10000.0, 500.0)
    TempHumidity = st.number_input("Temperature × Humidity", 0.0, 1000.0, 300.0)
    DayOfWeek_sin = st.number_input("Day of Week (sin)", -1.0, 1.0, 0.5)

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

    # Display results
    st.header("📊 Prediction Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Day Noise Level", f"{day_noise:.1f} dB")
    with col2:
        st.metric("Night Noise Level", f"{night_noise:.1f} dB")
    
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
        - Day (6 AM - 10 PM): <55 dB recommended, >70 dB acceptable(ncreases risk of cardiovascular and sleep issues.)
        - Night (10 PM - 6 AM): <45 dB recommended, 55–60 dB( significantly affects sleep quality.)

  Common Real Worls Noise Level
---------------------------------------------        
| Source                       | Typical dB |
| ---------------------------- | ---------- |
| **Breathing / whisper (1m)** | 20–30 dB   |
| **Quiet room**               | 30 dB      |
| **Conversation (1m)**        | 55–65 dB   |
| **Car traffic (10m)**        | 70–85 dB   |
| **Motorcycle**               | 95 dB      |
| **Rock concert / nightclub** | 100–110 dB |
| **Jet taking off (close)**   | 120–140 dB |


