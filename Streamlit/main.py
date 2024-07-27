
# main.py
import streamlit as st
import time

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

def setup_info(): # read_csv
    print("호출됨")

def main():
    st.title("ShongStudio의 주식 정보 방")
    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")

if __name__== "__main__":
    main()
