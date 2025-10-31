import streamlit as st
import sqlite3
from annotated_text import annotated_text
from collections import Counter
from utils import get_db_connection
from difflib import SequenceMatcher
import re

# -----------------------------
# 🔹 Helper functions
# -----------------------------
def write_result(precontext, term, indicator, postcontext):
    annotated_text(precontext, (term, "term", "#8ef"), (indicator, "ind."), postcontext)

def bag_words(results):
    stop_words = {
        'de', 'het', 'een', 'die', 'van', 'op', 'tussen', 'en', 'in', 'te', 
        'dat', 'met', 'als', 'voor', 'naar', 'door', 'bij', 'aan', 'uit', 
        'om', 'tot', 'over', 'onder', 'niet', 'is', 'was', 'zijn', 'wordt', 
        'ook', 'maar', 'dan', 'toch', 'nog', 'al', 'er', 'wel', 'geen', 'dus'
    }
    bag_of_words = []
    for id, term, indicator, gloss, precontext, postcontext, page in results:
        if gloss:
            words = re.findall(r'\b\w+\b', gloss.lower())
            bag_of_words.extend(words)
    return [w for w in bag_of_words if w not in stop_words]

def parse_page_info(page):
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

def get_similar_terms(search_term, con, threshold=0.6):
    cur = con.cursor()
    res = cur.execute("SELECT DISTINCT term FROM glosses")
    all_terms = [row[0] for row in res.fetchall()]
    
    similar_terms = []
    search_lower = search_term.lower()
    
    for term in all_terms:
        term_lower = term.lower()
        if search_lower == term_lower:
            return [term], True
        ratio = SequenceMatcher(None, search_lower, term_lower).ratio()
        if search_lower in term_lower or term_lower in search_lower:
            ratio = max(ratio, 0.7)
        if ratio >= threshold:
            similar_terms.append((term, ratio))
    similar_terms.sort(key=lambda x: x[1], reverse=True)
    return [term for term, _ in similar_terms[:10]], False

# -----------------------------
# 🔹 Streamlit App
# -----------------------------
st.title("🔍 Search Glossary")

# Initialize session state
if "selected_term" not in st.session_state:
    st.session_state.selected_term = ""

# Search input
search_term = st.text_input(
    "Search for a term", 
    placeholder="Enter term... (fuzzy matching enabled)",
    help="You don't need exact spelling - the search will find similar terms!",
    value=st.session_state.selected_term
)

# Update session state if user types a new term
if search_term != st.session_state.selected_term:
    st.session_state.selected_term = search_term

if st.session_state.selected_term:
    try:
        with get_db_connection() as con:
            similar_terms, is_exact = get_similar_terms(st.session_state.selected_term, con)
            
            if not similar_terms:
                st.warning(f"No similar terms found for '{st.session_state.selected_term}'")
                st.info("💡 Try a different spelling or a shorter search term")
            else:
                # Suggestions box
                if not is_exact and len(similar_terms) > 1:
                    st.info(f"🔎 Showing results for terms similar to '{st.session_state.selected_term}'")
                    with st.expander("📋 Similar terms found", expanded=False):
                        st.write(", ".join(similar_terms))
                
                selected_term = similar_terms[0]
                cur = con.cursor()
                query = """
                    SELECT id, term, indicator, glossed_as, pre_context, post_context, page 
                    FROM glosses 
                    WHERE term = ?;
                """
                res = cur.execute(query, (selected_term,))
                results = res.fetchall()
                
                if results:
                    st.title("Results")
                    st.subheader("Summary")
                    c = Counter(bag_words(results))
                    if c:
                        st.write("Most frequent words in the glosses for this term include:")
                        for word, count in c.most_common(5):
                            st.write(f"{word}: {count} times")
                    
                    st.subheader(f"Search results for '{selected_term}' ({len(results)} occurrence{'s' if len(results) != 1 else ''})")
                    
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
                    
                    # 🔁 Other similar term buttons
                    if len(similar_terms) > 1:
                        st.divider()
                        st.subheader("🔄 Try other similar terms")
                        cols = st.columns(min(5, len(similar_terms) - 1))
                        for idx, other_term in enumerate(similar_terms[1:6]):
                            with cols[idx]:
                                if st.button(other_term, key=f"term_{idx}"):
                                    st.session_state.selected_term = other_term
                                    st.rerun()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("👆 Enter a term to search")
