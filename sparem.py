# .venv\Scripts\activate

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu


st.set_page_config(page_title="S-Parameters", page_icon=":satellite_antenna:", layout="wide")

st.title(':satellite_antenna: S-Parameter Viewer')
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

sparam_file = st.sidebar.file_uploader(":satellite_antenna: S-Parameter Files", type=(["csv", "txt"]))
# , accept_multiple_files=True

vport_file = st.sidebar.file_uploader("S11 V-Port Return Loss", type=(["csv", "txt"]))

hport_file = st.sidebar.file_uploader("S22 H-Port Return Loss", type=(["csv", "txt"]))

vhport_file = st.sidebar.file_uploader("S12 V-H-Port Isolation", type=(["csv", "txt"]))


