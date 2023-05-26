import streamlit as st

from st_click_detector import click_detector

st.set_page_config("Need Title!!!!", layout="wide", initial_sidebar_state="collapsed")

with open("hackaburg23_frontend/style.css", "r") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

with st.sidebar:
    filter_container = st.container()
    thumbnails_container = st.container()

    filter_container.selectbox("Filter", ["None"])
    filter_container.slider("Certainty %", min_value=0, max_value=100, value=80)

    clickable_image_content="""<div style="display: flex; flex: 1 1 0%; flex-direction: column; gap: 1rem;">"""

    for i in range(1, 6):
        # thumbnails_container.image(f"https://picsum.photos/seed/{i}/300/200")
        clickable_image_content += f"""
        <a href="#" id="{i}">
            <div style="display: flex; flex-wrap: wrap; flex-grow: 1; align-items: stretch; gap: 1rem;">
                <div style="width: calc(25% - 1rem); flex: 1 1 calc(25% - 1rem);">
                    <img src="https://picsum.photos/seed/{i}/64/64"/>
                </div>
                <div style="width: calc(75% - 1rem); flex: 1 1 calc(75% - 1rem); font-family: 'StagSans';">
                    Filename {i}
                </div>
            </div>
        </a>"""

    clickable_image_content+="""</div>"""

    with thumbnails_container:
        st.session_state["current_item"] = click_detector(clickable_image_content)

top_container = st.container()
lower_container = st.container()

with top_container:
    st.header("Continental")
    with st.expander("Hidden Buttons", expanded=False):
        col1, col2 = st.columns(2)
        col1.button(on_click=st.balloons, label="Happy Birthday")
        col2.button(on_click=st.snow, label="Let it go")

with lower_container:
    if "current_item" in st.session_state and st.session_state["current_item"]:
        col1, col2 = st.columns([1, 3])
        col1.image(f"https://picsum.photos/seed/{st.session_state['current_item']}/1024/768")
        col2.text(f"Test: {st.session_state['current_item']}")
    else:
        st.info("Select a thumbnail for more details")
