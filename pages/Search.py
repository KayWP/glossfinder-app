import streamlit as st
import sqlite3
from utils import display_results, get_db_connection

st.title('🔍 Search Glossary')

# Search input
search_term = st.text_input("Search for a term", placeholder="Enter term...")

# Add an option to show glossed_as meanings
if search_term:
    # First, get the glossed_as values for preview
    try:
        with get_db_connection() as con:
            cur = con.cursor()
            query = """
                SELECT DISTINCT glossed_as 
                FROM glosses 
                WHERE term = ? AND glossed_as IS NOT NULL
            """
            res = cur.execute(query, (search_term,))
            meanings = [row[0] for row in res.fetchall() if row[0]]
            
            if meanings:
                with st.expander("📖 Meanings found", expanded=True):
                    for meaning in meanings:
                        st.markdown(f"- {meaning}")
    except:
        pass
    
    # Display full results
    display_results(search_term)
else:
    st.info("👆 Enter a term to search")
    
    # Optional: Show recent or example terms
    try:
        with get_db_connection() as con:
            cur = con.cursor()
            query = "SELECT DISTINCT term FROM glosses ORDER BY RANDOM() LIMIT 5"
            res = cur.execute(query)
            examples = [row[0] for row in res.fetchall()]
            
            if examples:
                st.markdown("**Example terms:**")
                cols = st.columns(len(examples))
                for i, term in enumerate(examples):
                    with cols[i]:
                        if st.button(term, key=f"example_{i}", use_container_width=True):
                            st.rerun()
    except:
        pass
