import streamlit as st
from components.earth import earth

def homepage():
    """Display the homepage of the application."""

    def intro():
        """Display the introduction section of the homepage."""
        st.title("Space Weather Analysis")
        st.write("Welcome to the Space Weather Analysis Tool!")

    def body():
        """Display the body section of the homepage."""
        earth()


    intro()  # Render the introduction section
    body()   # Render the body section
