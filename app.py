import streamlit as st
import pandas as pd 
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Reading data from Excel file
df = pd.read_excel("Adidas.xlsx")
st.set_page_config(layout="wide")

# Adding custom style for padding
st.markdown('<style>div.block-container{padding-top:1rem;padding-left:1rem;}</style>', unsafe_allow_html=True)

# Loading logo image
image = Image.open('adidas-logo.jpg')

# Create columns
col1, col2 = st.columns([0.1, 0.6])

# Add logo with padding
with col1:
    st.markdown("<div style='padding-top: 20px; padding-left: 20px;'>", unsafe_allow_html=True)  # Add padding around the image
    st.image(image, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Custom CSS for title
html_title = """
<style>
    .title-test {
        font-weight: bold;
        padding: 2.5px;
        border-radius: 6px;
        font-size: 30px;
    }
</style>
<center><h1 class="title-test">Adidas Interactive Sales Dashboard</h1></center>
"""

# Add title to col2
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5= st.columns([0.1,0.45,0.45])

with col3:
    box_date= str(datetime.datetime.now().strftime("%d %B %Y")) #getting the current date in the format day month year
    st.write(f"Last updated by:  \n {box_date}")

with col4:
    fig=px.bar(df, x="Retailer", y="TotalSales", labels={"TotalSales":"Total sales {$}"},
               title="Total sales by Retailer", hover_data=["TotalSales"],
               template="gridon", height=500)
    st.plotly_chart(fig,use_container_width=True)

__, view1, dwn1, view2,  dwn2= st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Retailer wise sales")# collapsible section titled "Retailer wise sales".
    data=df[["Retailer","TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)

with dwn1:
    st.download_button("Get Data",data=data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")