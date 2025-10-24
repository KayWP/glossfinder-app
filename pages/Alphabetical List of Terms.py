import streamlit as st
import sqlite3
import string
from utils import display_results, get_db_connection

st.title("Browse Terms Alphabetically")

# --- Initialize session state for selected letter ---
if "selected_letter" not in st.session_state:
    st.session_state.selected_letter = None

# --- Letter selection as clickable buttons ---
st.subheader("Choose a starting letter")
cols = st.columns(len(string.ascii_uppercase))
for i, letter in enumerate(string.ascii_uppercase):
    if cols[i].button(letter):
        st.session_state.selected_letter = letter

selected_letter = st.session_state.selected_letter

# --- Fetch terms ---
@st.cache_data(show_spinner=False)
def fetch_terms(letter):
    try:
        with get_db_connection() as con:
            cur = con.cursor()
            query = """
                SELECT DISTINCT term
                FROM clusters
                WHERE term LIKE ?
                ORDER BY term ASC
            """
            cur.execute(query, (f"{letter}%",))
            return [row[0] for row in cur.fetchall()]
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []

if selected_letter:
    terms = fetch_terms(selected_letter)

    # --- Term search/filter ---
    if terms:
        search_input = st.text_input("Search term:", "")
        filtered_terms = [t for t in terms if search_input.lower() in t.lower()]

        if filtered_terms:
            selected_term = st.selectbox("Select a term:", filtered_terms)
        else:
            selected_term = None
            st.info("No matching terms found.")
    else:
        selected_term = None
        st.info(f"No terms starting with '{selected_letter}'")

    # --- Display results ---
    if selected_term:
        display_results(selected_term)
    else:
        st.info("👈 Select a term to view details")
else:
    st.info("👈 Click a letter to browse terms")
