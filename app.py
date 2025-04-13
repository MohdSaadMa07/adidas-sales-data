import streamlit as st
import pandas as pd 
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

#READING data from excel file
df=pd.read_excel("Adidas.xlsx")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</styles>',unsafe_allow_html=True)
image=Image.open('adidas-logo.jpg')

