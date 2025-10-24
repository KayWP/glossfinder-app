import streamlit as st
import sqlite3
from annotated_text import annotated_text
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    con = sqlite3.connect("glosses.db")
    try:
        yield con
    finally:
        con.close()

def display_results(search_term):
    """Display glossary results for a given term"""
    try:
        with get_db_connection() as con:
            cur = con.cursor()
            # Use parameterized query to prevent SQL injection
            query = """
                SELECT id, term, indicator, glossed_as, pre_context, post_context, page 
                FROM glosses 
                WHERE term = ?
                ORDER BY page
            """
            res = cur.execute(query, (search_term,))
            results = res.fetchall()
            
            if not results:
                st.info(f"No results found for '{search_term}'")
                return
            
            st.subheader(f"Results ({len(results)} occurrence{'s' if len(results) > 1 else ''})")
            
            for id, term, indicator, glossed_as, pre_context, post_context, page in results:
                # Create a container for each result
                with st.container():
                    # Display page info and glossed_as in a compact header
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if glossed_as:
                            st.caption(f"**Glossed as:** {glossed_as}")
                    with col2:
                        if page:
                            # Extract just the filename from the page path
                            page_display = page.split('/')[-1].replace('.xml', '')
                            st.caption(f"📄 `{page_display}`")
                    
                    # Display the annotated context
                    annotated_text(
                        pre_context, 
                        (term, "term", "#8ef"), 
                        (indicator, "ind.", "#ffa"), 
                        post_context
                    )
                    st.divider()
                    
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
