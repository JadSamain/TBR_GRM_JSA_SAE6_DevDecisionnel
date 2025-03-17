import streamlit as st

def main():
    st.title("Welcome to My Streamlit App")
    st.header("This is a header")
    st.subheader("This is a subheader")
    st.text("This is some text")

    if st.button("Click me"):
        st.write("Button clicked!")

    name = st.text_input("Enter your name:")
    if name:
        st.write(f"Hello, {name}!")

    st.sidebar.title("Sidebar")
    st.sidebar.write("This is the sidebar")

if __name__ == "__main__":
    main()