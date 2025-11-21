import streamlit as st

st.set_page_config(
    page_title="Glossary Browser",
    page_icon="📚",
)

st.write("# Welcome to the VOC Glossing Explorer!")

st.markdown("""
This application helps you explore historical glossed terms from the Dutch East India Company (VOC) archives, extracted automatically from the **GLOBALISE** transcriptions using a method to recognize **glosses**: brief notations of the meaning of a word.  
""")

st.markdown("_Not sure where to start? Try searching for one of these:_")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Cannecappul'):
        st.session_state.selected_term = "cannecappul"
        st.switch_page("pages/Search.py")

with col2:
    if st.button('Winkondou'):
        st.session_state.selected_term = "winkondou"
        st.switch_page("pages/Search.py")

with col3:
    if st.button('Koutewaal'):
        st.session_state.selected_term = "koutewaal"
        st.switch_page("pages/Search.py")

st.markdown("""
The dataset contains terms and explanations of words identified as **foreign loanwords**, along with counts of their occurrences and glossed instances, enabling historical and sociolinguistic research into language contact, adoption, and understanding over time.
""")
            
with st.expander("How it works"):
    st.markdown("""
    The application builds on this abstract:

    **Pepping, K. (2024). Not something to gloss over: identifying foreign loanwords and their understood meaning in the corpus of the Dutch East India Company. Paper presented at Digital Humanities in the Benelux 2024 Conference, Leuven, Belgium.**  
    [https://doi.org/10.5281/zenodo.11455556](https://doi.org/10.5281/zenodo.11455556)

    In short:

    - The VOC archives contain millions of documents from the 17th–18th centuries, including terms borrowed from Asian languages.  
    - Glosses, often marked by the word **“of”** or a variant, can indicate a word’s meaning.  
    - Using word embeddings and a list of gloss indicators, terms and their explanations are extracted from the tokenized corpus.  
    - The result is a dataset of potential loanwords, their glosses, and statistics that allow insight into historical language use and adoption (plus a whole lot of noise!)
                
    However:
    - That means this data contains a lot of noise! It is an explorative tool, not a definitive answer to what something means, or even to what interesting words are!
                
    Note on cleaning:
    - In order to make the size of the data smaller, all terms of three letters or less were removed. Likewise, any terms with an occurence larger than 125 in the corpus were removed as well. If you are interested in those, feel free to run the code yourself without these filters!
    """)
                
with st.expander("Resources"):
    st.markdown("""
    ### Resources
    - GitHub repo for the data processing: [GLOBALISE-glossfinder](https://github.com/KayWP/GLOBALISE-glossfinder)  
    - Source data: [VOC transcriptions v2 – GLOBALISE](https://hdl.handle.net/10622/LVXSBW)  
    - Explore more VOC data: [vocdata.nl](https://www.vocdata.nl)
    """)

st.markdown("""
### How to use:

**🔍 Search**: Use the search page to look up specific terms directly  

**📖 Browse Alphabetically**: Browse terms organized by their first letter  
""")

# Optional: Add some statistics
try:
    import sqlite3
    con = sqlite3.connect("glosses.db")
    cur = con.cursor()
    
    # Get term count
    term_count = cur.execute("SELECT COUNT(DISTINCT term) FROM clusters").fetchone()[0]
    gloss_count = cur.execute("SELECT COUNT(*) FROM glosses").fetchone()[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Terms", term_count)
    with col2:
        st.metric("Total Glosses", gloss_count)
    
    con.close()
except Exception as e:
    st.info("Database statistics unavailable")

# Sidebar link to explore more VOC data
st.sidebar.markdown(
    "🔗 **Explore more VOC data:** [vocdata.nl](https://www.vocdata.nl)"
)

# Collapsible References & Citations
with st.expander("References & Citations"):
    st.markdown("""
1. Pepping, K. (2024). *Not something to gloss over: identifying foreign loanwords and their understood meaning in the corpus of the Dutch East India Company.* Paper presented at Digital Humanities in the Benelux 2024 Conference, Leuven, Belgium. [https://doi.org/10.5281/zenodo.11455556](https://doi.org/10.5281/zenodo.11455556)

2. GLOBALISE project (2024). *VOC transcriptions v2 - GLOBALISE*. IISH Data Collection, V1. [https://hdl.handle.net/10622/LVXSBW](https://hdl.handle.net/10622/LVXSBW)

3. GitHub repository for data processing: [https://github.com/KayWP/GLOBALISE-glossfinder](https://github.com/KayWP/GLOBALISE-glossfinder)
""")