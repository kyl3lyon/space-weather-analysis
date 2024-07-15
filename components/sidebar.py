import streamlit as st
import json

def display_sidebar():
    st.sidebar.title("Space Weather Data Explorer")
    st.sidebar.write("Welcome to the Space Weather Analysis Tool!")

def load_datasets():
    """Load dataset names from a JSON file."""
    with open("utils/datasets.json", "r") as f:
        datasets = json.load(f)
    return datasets

def get_user_inputs(dataset_names):
    """Get user inputs for dataset selection, date range, limit, and format."""
    selected_datasets = st.sidebar.multiselect("Select Dataset(s)", dataset_names)
    selected_time_start = st.sidebar.date_input("Start Time", value=None, format="YYYY-MM-DD")
    selected_time_end = st.sidebar.date_input("End Time", value=None, format="YYYY-MM-DD")
    limit = st.sidebar.number_input("Limit Results", min_value=1, value=10, step=1)
    selected_format = st.sidebar.radio("Select Format", [".csv", ".json"])
    operations = st.sidebar.multiselect("Select Operations", ['rename', 'formatTime', 'max', 'min', 'limit'])
    operation_values = {op: st.sidebar.text_input(f"Enter value for {op}", "") for op in operations}
    return selected_datasets, selected_time_start, selected_time_end, limit, selected_format, operations, operation_values

def generate_dataset_urls(base_url, datasets, selected_datasets, selected_format, selected_time_start, selected_time_end, limit, operations, operation_values):
    """Generate full URLs for the selected datasets with user-selected configurations."""
    urls = []
    for name in selected_datasets:
        if name in datasets:
            url = f"{base_url}{datasets[name]}{selected_format}?"
            if selected_time_start:
                url += f"time>={selected_time_start}&"
            if selected_time_end:
                url += f"time<={selected_time_end}&"
            for op in operations:
                value = operation_values[op]
                if op == "rename":
                    url += f"rename({value})&"  # Assume value is in the format "old_name,new_name"
                elif op == "formatTime":
                    url += f"formatTime({value})&"  # Assume value is a valid time format
                elif op == "limit" and limit > 0:
                    url += f"limit({limit})&"
                elif op in ["max", "min"]:
                    url += f"{op}({value})&"  # Assume value is a variable name for max or min
            urls.append(url.strip('&'))  # Remove trailing ampersand
    return urls

def dataset_selector():
    base_url = "https://lasp.colorado.edu/space-weather-portal/latis/dap/"
    datasets = load_datasets()
    dataset_names = list(datasets.keys())

    st.sidebar.header("Dataset Configuration")
    selected_datasets, selected_time_start, selected_time_end, limit, selected_format, operations, operation_values = get_user_inputs(dataset_names)

    st.sidebar.markdown("---")  # Add a horizontal line for separation

    st.sidebar.header("Generated URLs")
    dataset_urls = generate_dataset_urls(base_url, datasets, selected_datasets, selected_format, selected_time_start, selected_time_end, limit, operations, operation_values)
    display_dataset_urls(dataset_urls, selected_datasets)

def display_dataset_urls(dataset_urls, selected_datasets):
    """Display generated URLs in the sidebar as an ordered list with titles."""
    for i, (url, dataset) in enumerate(zip(dataset_urls, selected_datasets), 1):
        st.sidebar.subheader(f"{i}. {dataset}")
        st.sidebar.code(url, language="")
