import streamlit as st
import sqlite3
import string
from annotated_text import annotated_text

con = sqlite3.connect("glosses.db")
cur = con.cursor()

def print_results(search_term):
    query = f"""
    SELECT * FROM glosses WHERE term = "{search_term}";
    """
    res = cur.execute(query)

    st.subheader("Results")

    for id, term, indicator, gloss, precontext, postcontext in res.fetchall():
        annotated_text(precontext, (term, "term", "#8ef"), (indicator, "ind."), postcontext)

selected_letter = None
selected_term = None

col1, col2, col3 = st.columns([2, 6, 6])

with col1:
    selected_letter = st.radio(
    "Choose a letter:",
    list(string.ascii_uppercase)  # ['A', 'B', ..., 'Z']
    )

with col2:
    st.subheader('Available terms')

    if not selected_letter:
        st.stop()

    query = """
        SELECT term 
        FROM clusters 
        WHERE term LIKE ? 
        ORDER BY term ASC;
    """
    res = cur.execute(query, (f"{selected_letter}%",))
    terms = [row[0] for row in res.fetchall()]  # extract terms from tuples

    if terms:
        selected_term = st.radio(
            "Choose a term:",  # updated label
            terms
        )
    else:
        st.info("No terms available for this letter.")

with col3:
    while not selected_term:
        st.stop()

    else:
        print_results(selected_term)