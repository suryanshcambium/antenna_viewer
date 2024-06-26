# .venv\Scripts\activate

import plotly.graph_objects as go
import plotly.express as px
from scripts.data_clean import data_clean
from scripts.parameter_extract import parameter_extract
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Antenna Viewer", page_icon=":satellite_antenna:", layout="wide")

st.title(':satellite_antenna: Antenna Viewer')
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

uploaded_files = st.sidebar.file_uploader(":satellite_antenna: Antenna Files", accept_multiple_files=True, type=(["csv"]))

CrossPol = st.sidebar.checkbox("Read Cross-Pol Data")

selected = option_menu(
    menu_title = None,
    options=["Pattern", "Parameters"],
    orientation="horizontal"
)

if selected=="Pattern":
    if uploaded_files:
        number_of_files = len(uploaded_files)
        df = data_clean(uploaded_files)
        # st.write(df)
        dfp = df.iloc[:int(df.shape[0]/2),:]
        # st.write(dfp)
        if CrossPol:
            fig = px.line(df, x = df.iloc[:,1], y = df.columns[2:], color_discrete_sequence=px.colors.qualitative.G10)
            fig.update_layout(
            width=1900,  # Set the width of the plot
            height=700,   # Set the height of the plot
            title = 'Cross-Pol',
            hovermode="x unified"
            )
        else:

            fig = px.line(dfp, x = dfp.iloc[:,1], y = dfp.columns[2:], color_discrete_sequence=px.colors.qualitative.G10)
            fig.update_layout(
            width=1900,  # Set the width of the plot
            height=700,   # Set the height of the plot
            title = 'No Cross-Pol',
            hovermode="x unified"
            )

        st.plotly_chart(fig, config = {'scrollZoom': True})

        with st.expander("See Tabular Data"):
            st.write(df)

    # st.markdown('# Parameters')

if selected=="Parameters":
    if uploaded_files:
        number_of_files = len(uploaded_files)
        df = data_clean(uploaded_files)
        # st.write(df)
        dfp = df.iloc[:int(df.shape[0]/2),:]
        # st.write(dfp)
        col1, col2 = st.columns((2))
        col3, col4 = st.columns((2))


        df2 = parameter_extract(dfp, number_of_files)


        with col1:
            fig2 = px.line(df2, x = df2.index, y = df2.columns[2], color = 'FileName', color_discrete_sequence=px.colors.qualitative.Dark24)
            # , template='plotly_dark'

            fig2.update_layout(
                # width=1900,  # Set the width of the plot
                # height=1000,   # Set the height of the plot
                title = '3dB BeamWidth (dB)',
                xaxis_title = 'Frequency (Hz)',
                yaxis_title = '3dB BeamWidth (dB)',
                hovermode="x unified"
                )
        

            st.plotly_chart(fig2, config = {'scrollZoom': True})



        with col2:
            fig2 = px.line(df2, x = df2.index, y = df2.columns[3], color = 'FileName', color_discrete_sequence=px.colors.qualitative.Dark24)
            # , template='plotly_dark', markers = True

            fig2.update_layout(
                # width=1900,  # Set the width of the plot
                # height=1000,   # Set the height of the plot
                title = 'Side Lobe Level (dB)',
                xaxis_title = 'Frequency (Hz)',
                yaxis_title = 'Side Lobe Level (dB)',
                hovermode="x unified"
                )
        

            st.plotly_chart(fig2, config = {'scrollZoom': True})




        with col3:
            fig2 = px.line(df2, x = df2.index, y = df2.columns[0], color = 'FileName', color_discrete_sequence=px.colors.qualitative.Dark24)
            # , template='plotly_dark', markers = True

            fig2.update_layout(
                # width=1900,  # Set the width of the plot
                # height=1000,   # Set the height of the plot
                title = 'Gain (dB)',
                xaxis_title = 'Frequency (Hz)',
                yaxis_title = 'Gain (dB)',
                hovermode="x unified"
                )
        

            st.plotly_chart(fig2, config = {'scrollZoom': True})
        

        with col4:
            fig3 = px.line(df2, x = df2.index, y = df2.columns[1], color = 'FileName', color_discrete_sequence=px.colors.qualitative.Dark24)
            # , template='plotly_dark', markers = True

            fig3.update_layout(
                # width=1900,  # Set the width of the plot
                # height=1000,   # Set the height of the plot
                title = 'Beam-Squint',
                xaxis_title = 'Frequency (Hz)',
                yaxis_title = 'Beam-Squint'
                ,hovermode="x unified"
            )

            st.plotly_chart(fig3, config = {'scrollZoom': True})


        with st.expander("See Tabular Data (Parameters)"):
            st.write(df2)        # Contain this in expander





