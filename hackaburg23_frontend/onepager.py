import base64
import glob
from path import Path
import streamlit as st

from st_click_detector import click_detector

st.set_page_config("Need Title!!!!", layout="wide", initial_sidebar_state="collapsed")

with open("hackaburg23_frontend/style.css", "r") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

with st.sidebar:
    filter_container = st.container()
    thumbnails_container = st.container()

    filter_container.selectbox("Filter", ["None"])
    filter_container.slider("Certainty %", min_value=0, max_value=100, value=80)

    clickable_image_content="""<div style="display: flex; flex: 1 1 0%; flex-direction: column; gap: 1rem;">"""

    counter = 0

    for filename in glob.iglob("/home/ec2-user/data/**/*.png", recursive=True):
        clickable_image_content += f"""
        <a href="#" id="{filename}">
            <div style="display: flex; flex-wrap: wrap; flex-grow: 1; align-items: stretch; gap: 1rem;">
                <div style="width: calc(25% - 1rem); flex: 1 1 calc(25% - 1rem);">
                    <img src="data:image/png;base64,{img_to_bytes(filename)}" width="64px" height="64px"/>
                </div>
                <div style="width: calc(75% - 1rem); flex: 1 1 calc(75% - 1rem); font-family: 'StagSans';">
                    Filename {filename}
                </div>
            </div>
        </a>"""

        counter += 1

        if counter == 100:
            break

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
        col1.image(f"{st.session_state['current_item']}")
        col2.text(f"Test: {st.session_state['current_item']}")
    else:
        st.info("Select a thumbnail for more details")
