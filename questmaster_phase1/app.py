import streamlit as st
import json

# Imposta layout Streamlit
st.set_page_config(page_title="QuestMaster", layout="centered")
st.title("⚔️ QuestMaster")


# Carica il file story.json
@st.cache_data
def load_story():
    with open("../story.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Inizializza lo stato corrente nella sessione
if "current_state" not in st.session_state:
    st.session_state.current_state = "start"

# Funzione per cambiare scena
def change_state(next_state):
    st.session_state.current_state = next_state

# Caricamento storia
story = load_story()
state = st.session_state.current_state

if state not in story:
    st.error(f"Stato non valido: '{state}' non trovato in story.json")
    st.stop()

scene = story[state]
st.markdown(f"### {scene['text']}")



# Mostra le azioni disponibili
if scene.get("actions"):
    for action_text, next_state in scene["actions"].items():
        if st.button(action_text):
            change_state(next_state)
            st.rerun()
else:
    st.success("🏁 Fine dell'avventura. Ricarica la pagina per ricominciare.")
