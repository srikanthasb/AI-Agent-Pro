import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from src.tools.maps_tool import get_route

from src.tools.voice import voice_supported

API_URL = "https://ai-agent-pro-webapp27-acgghkdsbuabgufn.southindia-01.azurewebsites.net/chat"

SPEECH_AVAILABLE = voice_supported()

if SPEECH_AVAILABLE:
    from src.tools.speech_tool import speech


# ---------------------------------------------------
# Display Route on Map
# ---------------------------------------------------
def display_route(route):

    m = folium.Map(
        location=route["start"],
        zoom_start=7,
    )

    folium.Marker(
        route["start"],
        popup=route["origin"],
        tooltip="Start",
        icon=folium.Icon(color="green"),
    ).add_to(m)

    folium.Marker(
        route["end"],
        popup=route["destination"],
        tooltip="Destination",
        icon=folium.Icon(color="red"),
    ).add_to(m)

    coords = [[lat, lon] for lon, lat in route["geometry"]]

    folium.PolyLine(
        coords,
        weight=5,
        color="blue",
    ).add_to(m)

    st_folium(
        m,
        width=900,
        height=500,
    )


# ---------------------------------------------------
# Streamlit Config
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Agent Pro")
st.caption("Powered by LangGraph • Groq • RAG • Maps • Memory")


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
with st.sidebar:

    if SPEECH_AVAILABLE:

        st.header("🎤 Voice Assistant")

        voice_enabled = st.toggle(
            "Enable Voice",
            value=True,
        )

        speed = st.slider(
            "Speech Speed",
            min_value=100,
            max_value=250,
            value=170,
            step=5,
            help="Higher = Faster",
        )

        volume = st.slider(
            "Volume",
            min_value=0,
            max_value=100,
            value=100,
            step=5,
        )

        if speed != speech.rate:
            speech.set_speed(speed)

        if (volume / 100) != speech.volume:
            speech.set_volume(volume / 100)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button("▶ Test"):

                speech.speak("Hello! I am your AI Assistant.")

        with col2:

            if st.button("⏹ Stop"):

                speech.stop()

    else:

        voice_enabled = False

        st.header("🎤 Voice Assistant")

        st.info("Voice responses are available only in the Windows desktop version.")

    st.divider()

    st.info("""
This assistant supports:

✅ Conversational Memory

✅ RAG over your documents

✅ Route Maps

✅ Web Search

✅ Voice Responses (Desktop)
""")


# ---------------------------------------------------
# Username
# ---------------------------------------------------
username = st.text_input(
    "Username",
    value="guest",
)


# ---------------------------------------------------
# Chat Memory
# ---------------------------------------------------
if "messages" not in st.session_state:

    st.session_state.messages = []


# ---------------------------------------------------
# Display Previous Messages
# ---------------------------------------------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])


# ---------------------------------------------------
# Chat Input
# ---------------------------------------------------
prompt = st.chat_input("Ask me anything...")

# ---------------------------------------------------
# Process User Input
# ---------------------------------------------------
if prompt:

    # Store User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    # ------------------------------------------------
    # ROUTE REQUEST
    # ------------------------------------------------
    if prompt.lower().startswith("route from"):

        try:

            text = prompt[10:].strip()

            origin, destination = text.split(" to ", 1)

            with st.spinner("Finding best route..."):

                route = get_route(
                    origin.strip(),
                    destination.strip(),
                )

            response = (
                f"📍 Route from **{route['origin']}** to **{route['destination']}**\n\n"
                f"📏 Distance : **{route['distance']:.1f} km**\n\n"
                f"⏱ Duration : **{route['duration']:.1f} minutes**"
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )

            with st.chat_message("assistant"):

                st.markdown(response)

                display_route(route)

            if SPEECH_AVAILABLE and voice_enabled:

                speech.speak(
                    f"Route from {route['origin']} to "
                    f"{route['destination']}. "
                    f"Distance is {route['distance']:.1f} kilometers. "
                    f"Estimated travel time is "
                    f"{route['duration']:.1f} minutes."
                )

        except ValueError:

            st.error("Use the format:\n\n" "route from Bangalore to Mysore")

        except Exception as e:

            st.error(e)

    # ------------------------------------------------
    # NORMAL AI CHAT
    # ------------------------------------------------
    else:

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "username": username,
                        "message": prompt,
                    },
                    timeout=120,
                )

                response.raise_for_status()

                answer = response.json()["response"]

            except Exception as e:

                answer = f"❌ Unable to contact AI Backend.\n\n{e}"

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        with st.chat_message("assistant"):

            st.write(answer)

        if SPEECH_AVAILABLE and voice_enabled:

            speech.speak(answer)


# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.divider()

st.caption(
    "🚀 AI Agent Pro | Built using Python, "
    "LangGraph, Groq, ChromaDB, Streamlit & Folium"
)
