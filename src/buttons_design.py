import streamlit as st
from streamlit_extras.stylable_container import stylable_container


def new_button(key, color="#a4b38f", typeB="sidebar"):
    with stylable_container(
            key="green_button",
            css_styles=f"""
                button {{
                    background-color: {color};
                    color: black;
                    border-radius:4px;
                }}
                """,
    ):  new = st.button(key,  use_container_width=True, key=key)
    return new


    with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    border: 4px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
    ):
        st.sidebar.markdown("This is a container with a border.")


def eliminate_button(key, color="#eea399"):
    with stylable_container(
            key="red_button",
            css_styles=f"""
                button {{
                    background-color: {color};
                    color: black;
                    border-radius:4px;
                }}
                """,
    ):
        delete = st.button(key,  use_container_width=True, key=key)
        return delete


    with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
    ):
        st.markdown("This is a container with a border.")
