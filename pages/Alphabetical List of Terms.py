import streamlit as st
import sqlite3
import string
from utils import display_results, get_db_connection

st.title("Browse Terms Alphabetically")

col1, col2, col3 = st.columns([2, 6, 6])

with col1:
    st.subheader("Letter")
    selected_letter = st.radio(
        "Choose a letter:",
        list(string.ascii_uppercase),
        label_visibility="collapsed"
    )

with col2:
    st.subheader('Available Terms')
    
    if selected_letter:
        try:
            with get_db_connection() as con:
                cur = con.cursor()
                # Use parameterized query to prevent SQL injection
                query = """
                    SELECT DISTINCT term 
                    FROM clusters 
                    WHERE term LIKE ? 
                    ORDER BY term ASC
                """
                res = cur.execute(query, (f"{selected_letter}%",))
                terms = [row[0] for row in res.fetchall()]
            
            if terms:
                selected_term = st.radio(
                    "Select a term:",
                    terms,
                    label_visibility="collapsed"
                )
            else:
                selected_term = None
                st.info(f"No terms starting with '{selected_letter}'")
                
        except sqlite3.Error as e:
            st.error(f"Database error: {e}")
            selected_term = None
        except Exception as e:
            st.error(f"An error occurred: {e}")
            selected_term = None
    else:
        selected_term = None

with col3:
    st.subheader("Details")
    if selected_term:
        display_results(selected_term)
    else:
        st.info("👈 Select a term to view details")
