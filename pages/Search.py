import streamlit as st
import sqlite3
from annotated_text import annotated_text
from collections import Counter
from utils import get_db_connection

def write_result(precontext, term, indicator, postcontext):
    annotated_text(precontext, (term, "term", "#8ef"), (indicator, "ind."), postcontext)

def bag_words(results):
    bag_of_words = []
    for id, term, indicator, gloss, precontext, postcontext, page in results:
        if gloss:  # Check if gloss is not None
            bag_of_words = bag_of_words + gloss.split()
    return bag_of_words

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

st.title('🔍 Search Glossary')

# Search input
search_term = st.text_input("Search for a term", placeholder="Enter term...")

if search_term:
    st.title('Results')
    st.subheader('Summary')
    
    try:
        with get_db_connection() as con:
            cur = con.cursor()
            query = "SELECT id, term, indicator, glossed_as, pre_context, post_context, page FROM glosses WHERE term = ?;"
            res = cur.execute(query, (search_term,))
            results = res.fetchall()
        
        if results:
            c = Counter(bag_words(results))
            
            if c:  # Only show if there are words in the glosses
                st.write("Most frequent words in the glosses for this term include:")
                for word, count in c.most_common(5):
                    st.write(f"{word}: {count} times")
            
            st.subheader(f"Search results for {search_term}")
            
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
                        st.markdown(f"[🔗 View source]({link}{search_term})")
                
                write_result(precontext, term, indicator, postcontext)
        else:
            st.info(f"No results found for '{search_term}'")
            
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("👆 Enter a term to search")