import streamlit as st
import sqlite3
from annotated_text import annotated_text
from collections import Counter
from utils import get_db_connection
from difflib import SequenceMatcher

def write_result(precontext, term, indicator, postcontext):
    annotated_text(precontext, (term, "term", "#8ef"), (indicator, "ind."), postcontext)

import re

def bag_words(results):
    # Extended Dutch stop words list
    stop_words = {
        'de', 'het', 'een', 'die', 'van', 'op', 'tussen', 'en', 'in', 'te', 
        'dat', 'met', 'als', 'voor', 'naar', 'door', 'bij', 'aan', 'uit', 
        'om', 'tot', 'over', 'onder', 'niet', 'is', 'was', 'zijn', 'wordt', 
        'ook', 'maar', 'dan', 'toch', 'nog', 'al', 'er', 'wel', 'geen', 'dus'
    }

    bag_of_words = []

    for id, term, indicator, gloss, precontext, postcontext, page in results:
        if gloss:
            # Split by non-word characters (regex) and normalize to lowercase
            bag_of_words = bag_of_words + gloss.split()

    # Filter out stop words
    filtered_words = [w for w in bag_of_words if w not in stop_words]

    return filtered_words

def parse_page_info(page):
    """Extract inventory number, scan number, and create link from page string"""
    if not page:
        return None, None, None
    
    # Extract filename from path
    filename = page.split('/')[-1].replace('.xml', '')
    
    # Parse the filename format: NL-HaNA_1.04.02_7609_0016
    parts = filename.split('_')
    if len(parts) >= 4:
        inventory_num = parts[2]
        scan_num = parts[3]
        
        # Construct the URN for the link: NL-HaNA_1.04.02_7609_16 (without leading zeros in last part)
        urn = f"{parts[0]}_{parts[1]}_{parts[2]}_{scan_num}"
        
        # Construct the link
        link = f"https://transcriptions.globalise.huygens.knaw.nl/detail/urn:globalise:{urn}?query[fullText]="
        
        return inventory_num, scan_num, link
    
    return None, None, None

def get_similar_terms(search_term, con, threshold=0.6):
    """Find terms similar to the search term using fuzzy matching"""
    cur = con.cursor()
    # Get all unique terms from the database
    res = cur.execute("SELECT DISTINCT term FROM glosses")
    all_terms = [row[0] for row in res.fetchall()]
    
    # Calculate similarity scores
    similar_terms = []
    search_lower = search_term.lower()
    
    for term in all_terms:
        term_lower = term.lower()
        
        # Exact match (case-insensitive)
        if search_lower == term_lower:
            return [term], True  # Return immediately with exact match
        
        # Calculate similarity ratio
        ratio = SequenceMatcher(None, search_lower, term_lower).ratio()
        
        # Also check if search term is contained in the term
        if search_lower in term_lower or term_lower in search_lower:
            ratio = max(ratio, 0.7)  # Boost substring matches
        
        if ratio >= threshold:
            similar_terms.append((term, ratio))
    
    # Sort by similarity (highest first)
    similar_terms.sort(key=lambda x: x[1], reverse=True)
    
    return [term for term, _ in similar_terms[:10]], False  # Return top 10 matches

st.title('🔍 Search Glossary')

# Search input with help text
search_term = st.text_input(
    "Search for a term", 
    placeholder="Enter term... (fuzzy matching enabled)",
    help="You don't need exact spelling - the search will find similar terms!"
)

if search_term:
    try:
        with get_db_connection() as con:
            # Get similar terms
            similar_terms, is_exact = get_similar_terms(search_term, con)
            
            if not similar_terms:
                st.warning(f"No similar terms found for '{search_term}'")
                st.info("💡 Try a different spelling or a shorter search term")
            else:
                # If not exact match, show suggestions
                if not is_exact and len(similar_terms) > 1:
                    st.info(f"🔎 Showing results for terms similar to '{search_term}'")
                    with st.expander("📋 Similar terms found", expanded=False):
                        st.write(", ".join(similar_terms))
                
                # Search for the first/best matching term
                selected_term = similar_terms[0]
                
                cur = con.cursor()
                query = "SELECT id, term, indicator, glossed_as, pre_context, post_context, page FROM glosses WHERE term = ?;"
                res = cur.execute(query, (selected_term,))
                results = res.fetchall()
                
                if results:
                    st.title('Results')
                    st.subheader('Summary')
                    
                    c = Counter(bag_words(results))
                    
                    if c:  # Only show if there are words in the glosses
                        st.write("Most frequent words in the glosses for this term include:")
                        for word, count in c.most_common(5):
                            st.write(f"{word}: {count} times")
                    
                    st.subheader(f"Search results for '{selected_term}' ({len(results)} occurrence{'s' if len(results) != 1 else ''})")
                    
                    for id, term, indicator, gloss, precontext, postcontext, page in results:
                        st.divider()
                        
                        # Display source information
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
                    
                    # Show other similar terms if available
                    if len(similar_terms) > 1:
                        st.divider()
                        st.subheader("🔄 Try other similar terms")
                        cols = st.columns(min(5, len(similar_terms) - 1))
                        for idx, other_term in enumerate(similar_terms[1:6]):
                            with cols[idx]:
                                if st.button(other_term, key=f"term_{idx}"):
                                    st.rerun()
                                    
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("👆 Enter a term to search")