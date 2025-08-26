import streamlit as st
import sqlite3
from annotated_text import annotated_text

con = sqlite3.connect("glosses.db")
cur = con.cursor()

st.title('Search bar')

search_term = st.text_input("Search here")

while not search_term:
    st.stop()

else:
    query = f"""
    SELECT * FROM glosses WHERE term = "{search_term}";
    """
    res = cur.execute(query)

    st.subheader("Results")

    for id, term, indicator, gloss, precontext, postcontext in res.fetchall():
        annotated_text(precontext, (term, "term", "#8ef"), (indicator, "ind."), postcontext)
