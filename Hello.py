import streamlit as st

st.set_page_config(
    page_title="Glossary Browser",
    page_icon="📚",
)

st.write("# Welcome to the Glossary Browser! 📚")

st.markdown("""
This application helps you explore historical glossary terms from Dutch colonial archives.

### How to use:

**🔍 Search**: Use the search page to look up specific terms directly

**📖 Browse Alphabetically**: Browse terms organized by their first letter

---

Select a page from the sidebar to get started!
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
