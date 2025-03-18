import streamlit as st

def main():
    st.title("Analyse de données énergétiques")
    st.header("SAÉ 6 - Développement d'un outil décisionnel")
    st.subheader("Gaultier RAIMBAULT - Thibault RENAULT - Jad SAMAIN")
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