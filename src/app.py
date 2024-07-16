import streamlit as st
from components.sidebar import (
    display_sidebar,
    dataset_selector
)

from components.homepage import homepage

# Call Main Function
st.set_page_config(page_title="Space Weather Analysis", layout="wide")

def main():
    display_sidebar()     # Initialize and render the sidebar components
    dataset_selector()    # Present dataset selection options in the sidebar
    homepage()            # Display the homepage

if __name__ == "__main__":
    main()