import streamlit as st
import sqlite3
from annotated_text import annotated_text
from collections import Counter

def write_result(precontext, term, indicator,  postcontext):
    annotated_text(precontext, (term, "term", "#8ef"), (indicator, "ind."), postcontext)

def bag_words(results):
    bag_of_words = []
    for id, term, indicator, gloss, precontext, postcontext in results:
        bag_of_words = bag_of_words + gloss.split()

    return bag_of_words


if 'selected_term' in st.session_state and st.session_state.selected_term is not None:
    selected_term = st.session_state.selected_term
    st.title('Results')
    st.subheader('Summary')

    with sqlite3.connect("glosses.db") as con:
        cur = con.cursor()
        query = "SELECT * FROM glosses WHERE term = ?;"
        res = cur.execute(query, (selected_term,))

        results = res.fetchall()


    c = Counter(bag_words(results))
    

    st.write("Most frequent words in the glosses for this term include:")
    for word, count in c.most_common(5):
        st.write(f"{word}: {count} times")

    st.subheader(f"Search results for {selected_term}")

    

    for id, term, indicator, gloss, precontext, postcontext in results:
        st.divider()
        write_result(precontext, term, indicator, postcontext)
        


else:
    st.warning("⚠️ No data found. Please upload an article report on the upload page first.")
    if st.button("🔎 Go to Search Page"):
        st.switch_page("pages/Search.py")