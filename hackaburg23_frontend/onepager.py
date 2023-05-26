import base64
import glob
import streamlit as st

from st_click_detector import click_detector

st.set_page_config("Need Title!!!!", layout="wide", initial_sidebar_state="collapsed")

with open("hackaburg23_frontend/style.css", "r") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

def img_to_bytes(img_path):
    with open(img_path, "rb") as f:
        img_bytes = f.read()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

with st.sidebar:
    filter_container = st.container()
    thumbnails_container = st.container()

    st.markdown(
        f"""
        <div id="logo">#TODO</div>
        <div style="display: flex; flex-direction: column; gap: 2rem;">
            <div id="filter-box" style="background-color: {st.get_option('theme.primaryColor')}; border-radius: 15px; padding: 8px;">
                <h3>Files</h3>
                <h5>Select your choice</h5>
                <button>Good Image</button>
                <button>Bad Image</button>
            </div>
            <div id="thumbnail-box" style="display: flex;">
                <div class="stTabs css-0 exp6ofz0">
                    <div class="st-cp">
                        <div class="">
                            <div data-baseweb="tab-list" role="tablist" aria-orientation="horizontal" class="st-cq st-b3 st-cr st-cs st-ct st-cu st-cv st-cw st-cx st-cy st-cz st-d0 st-d1">
                                <button data-baseweb="tab" id="tabs-bui3-tab-0" role="tab" aria-selected="true" aria-controls="tabs-bui3-tabpanel-0" tabindex="0" type="button" class="st-bz st-d2 st-b6 st-b5 st-ar st-as st-ck st-d3 st-c5 st-bd st-ci st-be st-cj st-d4 st-d5 st-d6 st-d7 st-cc st-c9 st-cb st-ca st-d8 st-d9 st-da st-b1 st-db st-c6 st-c7 st-dc st-dd st-de st-c8 st-df st-ae st-bx st-ag st-ah st-ai st-aj st-dg st-dh st-di st-dj st-dk st-dl">
                                    <div data-testid="stMarkdownContainer" class="css-xujc5b e16nr0p34">
                                        <p>All</p>
                                    </div>
                                </button>
                                <button data-baseweb="tab" id="tabs-bui3-tab-1" role="tab" aria-selected="false" aria-controls="tabs-bui3-tabpanel-1" tabindex="-1" type="button" class="st-bz st-d2 st-b6 st-b5 st-ar st-as st-ck st-d3 st-c5 st-bd st-ci st-be st-cj st-d4 st-d5 st-d6 st-d7 st-cc st-c9 st-cb st-ca st-by st-d9 st-da st-b1 st-db st-c6 st-c7 st-dc st-dd st-de st-c8 st-df st-ae st-bx st-ag st-ah st-ai st-aj st-dg st-dh st-di st-dj st-dk st-dl">
                                    <div data-testid="stMarkdownContainer" class="css-xujc5b e16nr0p34">
                                        <p>Good Image</p>
                                    </div>
                                </button>
                                <button data-baseweb="tab" id="tabs-bui3-tab-2" role="tab" aria-selected="false" aria-controls="tabs-bui3-tabpanel-2" tabindex="-1" type="button" class="st-bz st-d2 st-b6 st-b5 st-ar st-as st-ck st-d3 st-c5 st-bd st-ci st-be st-cj st-d4 st-d5 st-d6 st-d7 st-cc st-c9 st-cb st-ca st-by st-d9 st-da st-b1 st-db st-c6 st-c7 st-dc st-dd st-de st-c8 st-df st-ae st-bx st-ag st-ah st-ai st-aj st-dg st-dh st-di st-dj st-dk st-dl">
                                    <div data-testid="stMarkdownContainer" class="css-xujc5b e16nr0p34">
                                        <p>Bad Image</p>
                                    </div>
                                </button>
                                <div data-baseweb="tab-highlight" aria-hidden="true" role="presentation" class="st-dm st-dn st-do st-dp st-dq st-dr st-dx st-dt">
                                </div>
                            </div>
                        </div>
                        <div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-du st-cq st-dr"></div>
                        <div data-baseweb="tab-panel" role="tabpanel" id="tabs-bui3-tabpanel-0" aria-labelledby="tabs-bui3-tab-0" class="st-cs st-c6 st-dv st-be st-cj st-bd" style="position: relative;">
                            <div style="overflow: visible; width: 0px; display: flex; flex-direction: column; flex: 1 1 0%;">
                                <div width="607" data-testid="stVerticalBlock" class="css-e0kg7f e1tzin5v0"></div>
                            </div>
                            <div class="resize-triggers">
                                <div class="expand-trigger">
                                    <div style="width: 608px; height: 17px;"></div>
                                </div>
                                <div class="contract-trigger"></div>
                            </div>
                        </div>
                        <div data-baseweb="tab-panel" role="tabpanel" id="tabs-bui3-tabpanel-1" aria-labelledby="tabs-bui3-tab-1" hidden="" class="st-cs st-c6 st-dv st-be st-cj st-bd" style="position: relative;">
                            <div style="overflow: visible; width: 0px; display: flex; flex-direction: column; flex: 1 1 0%;">
                                <div width="0" data-testid="stVerticalBlock" class="css-g70r9e e1tzin5v0"></div>
                            </div>
                            <div class="resize-triggers">
                                <div class="expand-trigger">
                                    <div style="width: 1px; height: 1px;"></div>
                                </div>
                                <div class="contract-trigger"></div>
                            </div>
                        </div>
                        <div data-baseweb="tab-panel" role="tabpanel" id="tabs-bui3-tabpanel-2" aria-labelledby="tabs-bui3-tab-2" hidden="" class="st-cs st-c6 st-dv st-be st-cj st-bd" style="position: relative;">
                            <div style="overflow: visible; width: 0px; display: flex; flex-direction: column; flex: 1 1 0%;">
                                <div width="0" data-testid="stVerticalBlock" class="css-g70r9e e1tzin5v0"></div>
                            </div>
                            <div class="resize-triggers">
                                <div class="expand-trigger">
                                    <div style="width: 1px; height: 1px;"></div>
                                </div>
                                <div class="contract-trigger"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # filter_container.header("Files")
    # filter_container.caption("Select your choice")
    # filter_container.button("Good Image")
    # filter_container.button("Bad Image")

    # clickable_image_content="""<div style="display: flex; flex: 1 1 0%; flex-direction: column; gap: 1rem;">"""

    # counter = 0

    # for filename in glob.iglob("/home/ec2-user/data/**/*.png", recursive=True):
    #     clickable_image_content += f"""
    #     <a href="#" id="{filename}">
    #         <div style="display: flex; flex-wrap: wrap; flex-grow: 1; align-items: stretch; gap: 1rem;">
    #             <div style="width: calc(25% - 1rem); flex: 1 1 calc(25% - 1rem);">
    #                 <img src="data:image/png;base64,{img_to_bytes(filename)}" width="64px" height="64px"/>
    #             </div>
    #             <div style="width: calc(75% - 1rem); flex: 1 1 calc(75% - 1rem); font-family: 'StagSans';">
    #                 Filename {filename}
    #             </div>
    #         </div>
    #     </a>"""

    #     counter += 1

    #     if counter == 100:
    #         break

    # clickable_image_content+="""</div>"""

    # with thumbnails_container:
    #     st.session_state["current_item"] = click_detector(clickable_image_content)

top_container = st.container()
lower_container = st.container()

with top_container:
    st.header("Continental")
    with st.expander("Hidden Buttons", expanded=False):
        col1, col2 = st.columns(2)
        col1.button(on_click=st.balloons, label="Happy Birthday")
        col2.button(on_click=st.snow, label="Let it go")

with lower_container:
    st.tabs(["All", "Good Image", "Bad Image"])
    if "current_item" in st.session_state and st.session_state["current_item"]:
        col1, col2 = st.columns([1, 3])
        col1.image(f"{st.session_state['current_item']}")
        col2.text(f"Test: {st.session_state['current_item']}")
    else:
        st.info("Select a thumbnail for more details")
