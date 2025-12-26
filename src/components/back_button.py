import streamlit as st

def render_back_button(back_to="app.py", button_text="🏠 Home",
                      help_text="Go back to home page",
                      show_separator=True):

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button(button_text, help=help_text, use_container_width=True):
            st.switch_page(back_to)

    if show_separator:
        st.divider()

def render_navigation_breadcrumb(pages_list):

    breadcrumb_html = "<div style='margin-bottom: 1rem;'>"

    for i, (page_name, page_path) in enumerate(pages_list):
        if i == len(pages_list) - 1:

            breadcrumb_html += f"<strong>{page_name}</strong>"
        else:

            breadcrumb_html += f"<a href='
            breadcrumb_html += " → "

    breadcrumb_html += "</div>"

    st.markdown(breadcrumb_html, unsafe_allow_html=True)

def render_multi_back_buttons(buttons_config):

    if not buttons_config:
        return

    num_buttons = len(buttons_config)
    cols = st.columns(num_buttons)

    for i, config in enumerate(buttons_config):
        with cols[i]:
            if st.button(
                config["text"],
                help=config.get("help", "Navigate"),
                use_container_width=True,
                key=f"back_btn_{i}"
            ):
                st.switch_page(config["page"])
