import streamlit as st
import sqlite3
import string
from collections import Counter
from annotated_text import annotated_text
from contextlib import contextmanager

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

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    con = sqlite3.connect("glosses.db")
    try:
        yield con
    finally:
        con.close()

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

def write_result(precontext, term, indicator, postcontext):
    """Annotated context display for a term occurrence"""
    annotated_text(precontext, (term, "term", "#8ef"), (indicator, "ind.", "#ffa"), postcontext)

def bag_words(results):
    """Return a bag of words from the glossed_as fields"""
    bag_of_words = []
    for id, term, indicator, gloss, precontext, postcontext, page in results:
        if gloss:
            bag_of_words.extend(gloss.split())
    return bag_of_words

def parse_page_info(page):
    """Extract inventory number, scan number, and source link from page string"""
    if not page:
        return None, None, None
    
    filename = page.split('/')[-1].replace('.xml', '')
    parts = filename.split('_')
    if len(parts) >= 4:
        inventory_num = parts[2]
        scan_num = parts[3]
        urn = f"{parts[0]}_{parts[1]}_{parts[2]}_{scan_num}"
        link = f"https://transcriptions.globalise.huygens.knaw.nl/detail/urn:globalise:{urn}?query[fullText]="
        return inventory_num, scan_num, link
    return None, None, None

# --- Main term selection & display ---
if selected_letter:
    terms = fetch_terms(selected_letter)
    
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

    if selected_term:
        try:
            with get_db_connection() as con:
                cur = con.cursor()
                query = """
                    SELECT id, term, indicator, glossed_as, pre_context, post_context, page
                    FROM glosses
                    WHERE term = ?
                    ORDER BY page
                """
                res = cur.execute(query, (selected_term,))
                results = res.fetchall()

                if results:
                    st.subheader('Summary')
                    c = Counter(bag_words(results))
                    if c:
                        st.write("Most frequent words in the glosses for this term include:")
                        for word, count in c.most_common(5):
                            st.write(f"{word}: {count} times")
                    
                    st.subheader(f"Occurrences of '{selected_term}' ({len(results)} occurrence{'s' if len(results) != 1 else ''})")
                    
                    for id, term, indicator, gloss, precontext, postcontext, page in results:
                        st.divider()
                        inventory_num, scan_num, link = parse_page_info(page)
                        if inventory_num and scan_num and link:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.caption(f"📁 Inventory: {inventory_num}")
                            with col2:
                                st.caption(f"🔢 Scan: {scan_num}")
                            with col3:
                                st.markdown(f"[🔗 View source]({link}{term})")
                        
                        write_result(precontext, term, indicator, postcontext)
                else:
                    st.info(f"No results found for '{selected_term}'")
        except sqlite3.Error as e:
            st.error(f"Database error: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("👈 Select a term to view details")
else:
    st.info("👈 Click a letter to browse terms")
