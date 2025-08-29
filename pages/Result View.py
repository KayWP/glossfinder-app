import streamlit as st
import sqlite3
from annotated_text import annotated_text

def write_result(precontext, term, indicator,  postcontext):
    annotated_text(precontext, (term, "term", "#8ef"), (indicator, "ind."), postcontext)

con = sqlite3.connect("glosses.db")
cur = con.cursor()

if 'selected_term' in st.session_state and st.session_state.selected_term is not None:
    selected_term = st.session_state.selected_term
    st.title('Results')
    st.subheader(f"Search results for {selected_term}")

    query = f"""
    SELECT * FROM glosses WHERE term = "{selected_term}";
    """
    res = cur.execute(query)

    for id, term, indicator, gloss, precontext, postcontext in res.fetchall():
        st.divider()
        write_result(precontext, term, indicator, postcontext)
        


else:
    st.warning("⚠️ No data found. Please upload an article report on the upload page first.")
    if st.button("🔎 Go to Search Page"):
        st.switch_page("pages/Search.py")