import streamlit as st
import streamlit.components.v1 as components
import os

# Set page title and favicon
st.set_page_config(page_title="Major-Industry Dashboard", layout="wide")

# Path to the interactive dashboard HTML file
# We use a path relative to this script
HTML_PATH = os.path.join("major_industry_circos_draft1", "interactive_dashboard.html")

def main():
    st.title("Interactive Major-Industry Connections")
    st.markdown("""
    This dashboard visualizes the flow of graduates from college majors to various industries.
    *Hover over segments and links to explore the data.*
    """)

    if os.path.exists(HTML_PATH):
        with open(HTML_PATH, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Display the HTML content using streamlit components
        components.html(html_content, height=1000, scrolling=True)
    else:
        st.error(f"Dashboard file not found at {HTML_PATH}. Please ensure the project structure is correct.")

if __name__ == "__main__":
    main()
