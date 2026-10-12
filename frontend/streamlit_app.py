import streamlit as st
import requests
import random

st.set_page_config(page_title="Alt-nature", page_icon="🌿", layout="centered")

st.title("🌿 Alt-nature")
st.subheader("Step away from your screen. Let nature guide your walk.")

# Define user-facing labels mapped to backend-friendly keys
vibe_options = {
    "🍂 Fall Foliage Walk": "fall_foliage_walk",
    "🌲 Deep Pine Forest": "pine_forest_stroll",
    "🌧️ Quiet Morning Mist": "morning_mist",
    "☀️ Sunlit Meadow": "sunlit_meadow",
    "🍄 Mushroom Foraging Trail": "mushroom_foraging"
}

with st.form("quest_form"):
    location_name = st.text_input("Your Location (City or Trail Name)", "Ann Arbor, MI")
    
    # Display user-friendly names in the dropdown
    selected_label = st.selectbox("Choose Your Outdoor Vibe", options=list(vibe_options.keys()))
    
    submitted = st.form_submit_button("Get Me Outside 🌲")

if submitted:
    # Get the internal key to send in your API payload
    vibe = vibe_options[selected_label]
    
    with st.spinner("Gathering environmental context..."):
        try:
            res = requests.post(
                "http://localhost:8000/api/quest/generate",
                json={"location_name": location_name, "vibe": vibe}
            )
            if res.status_code == 200:
                data = res.json()
                st.session_state['quest_id'] = data['quest_id']
                st.success("Quest Generated! Lock your phone and step outside.")
                
                st.markdown(f"### 🎯 {data['title']}")
                st.info(f"**Objective:** {data['objective']}")
                st.write(f"🌲 **Trail Insight:** {data['environmental_lore']}")
                
                weather = data.get('weather_context', {})
                st.caption(f"Weather: {weather.get('condition')} | Temp: {weather.get('temperature')} | Foliage: {weather.get('foliage_status')}")
                
                if data.get('audio_file_path'):
                    audio_url = f"http://localhost:8000/{data['audio_file_path']}"
                    st.audio(audio_url, format='audio/mp3')
            else:
                st.error("Failed to generate quest. Is the backend running?")
        except Exception as e:
            st.error(f"Connection error: {e}")

if 'quest_id' in st.session_state:
    st.divider()
    st.subheader("Got back inside?")
    with st.form("reflection_form"):
        notes = st.text_area("What did you notice during quest?")
        finished = st.form_submit_button("Complete Quest")
        if finished:
            res = requests.post(
                "http://localhost:8000/api/quest/verify",
                json={"quest_id": st.session_state['quest_id'], "reflection_notes": notes}
            )
            if res.status_code == 200:
                nature_quotes = [
                    "“The earth has music for those who listen.” — George Santayana",
                    "“In every walk with nature one receives far more than he seeks.” — John Muir",
                    "“Adopt the pace of nature: her secret is patience.” — Ralph Waldo Emerson"
                ]
                st.toast("🌿 Welcome back inside.", icon="🌲")
                st.success("Quest completed successfully! Streak updated.")
                st.info(random.choice(nature_quotes))