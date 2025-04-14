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
    
df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")
result=df.groupby(by=df["Month_Year"])["TotalSales"].sum().reset_index()
                                       
with col5:
    fig1=px.line(result, x="Month_Year",y="TotalSales",title="Total sales over time",
                 template="gridon")
    st.plotly_chart(fig1,use_container_width=True)

with view2:
    expander=st.expander("Monthly Sales")
    data=result
    expander.write(data)

with dwn2:
    st.download_button("Get Data", data=result.to_csv().encode("utf-8"),
                       file_name="MonthlySales.csv", mime="text/csv")
    
st.divider()

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Group and aggregate
result1 = df.groupby("state")[["totalsales", "unitssold"]].sum().reset_index()

# Rename columns for display
result1.rename(columns={
    "state": "State",
    "totalsales": "Total Sales",
    "unitssold": "Units Sold"
}, inplace=True)

# Create the Plotly figure
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1["State"], y=result1["Total Sales"], name="Total Sales"))
fig3.add_trace(go.Scatter(x=result1["State"], y=result1["Units Sold"], mode="lines",
                          name="Units Sold", yaxis="y2"))

# Update layout
fig3.update_layout(
    title="Total Sales and Units Sold by State",
    xaxis=dict(title="State"),
    yaxis=dict(title="Total Sales", showgrid=False),
    yaxis2=dict(title="Units Sold", overlaying="y", side="right"),
    template="gridon",
    legend=dict(x=1, y=1)
)

# Display chart
_, col6 = st.columns([0.1, 0.9])
with col6:
    st.plotly_chart(fig3, use_container_width=True)

# View data and download button
__, view3,__, dwn3 = st.columns([0.1,0.55,0.03, 0.45])
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)

with dwn3:
    st.download_button("Get Data", data=result1.to_csv(index=False).encode("utf-8"),
                       file_name="SalesbyUnitsSold.csv", mime="text/csv")

# Divider

st.divider()

# Create treemap data and format sales
_, col7 = st.columns([0.1, 1])
treemap = df[["region", "city", "totalsales"]].groupby(by=["region", "city"])["totalsales"].sum().reset_index()

# Define function to format sales in Lakhs
def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)

treemap["TotalSales (Formatted)"] = treemap["totalsales"].apply(format_sales)

# Create the treemap figure
fig4 = px.treemap(treemap, path=["region", "city"], values="totalsales",
                  hover_name="TotalSales (Formatted)",  # Fixed hover_name column
                  hover_data=["TotalSales (Formatted)"],
                  color="city", height=700, width=600)

fig4.update_traces(textinfo="label+value")

# Display the treemap in the column
with col7:
    st.subheader("Total Sales by Region and City")
    st.plotly_chart(fig4, use_container_width=True)