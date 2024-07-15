import streamlit as st
from components.sidebar import display_sidebar, dataset_selector

# Call Main Function
st.set_page_config(page_title="Space Weather Analysis", layout="wide")

def main():
    display_sidebar()
    dataset_selector()

if __name__ == "__main__":
    main()