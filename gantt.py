from st_aggrid import AgGrid
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import io

# st.set_page_config(layout='wide')  # Choose wide mode as the default setting

# Add a logo (optional) in the sidebar
# logo = Image.open(r'...\Insights_Bees_logo.png')
# st.sidebar.image(logo, width=120)

# Add the expander to provide some information about the app
with st.sidebar.expander("About the App"):
    st.write(
        """
        For SWS MPPE which provide a platform to visualize abnormal staion issue tracking 
     """
    )


# Add a template screenshot as an example
# st.subheader('Step 1: Download the project plan template')
# image = Image.open(r'...\example.png')  # template screenshot provided as an example
# st.image(image, caption='Make sure you use the same column names as in the template')

# Allow users to download the template
# @st.cache
# def convert_df(df):
#     return df.to_csv().encode('utf-8')


# df = pd.read_csv('output.csv')
# csv = convert_df(df)
# st.download_button(
#     label="Download Template",
#     data=csv,
#     file_name='project_template.csv',
#     mime='text/csv',
# )


# Main interface section 2
st.subheader('Step 1: Upload Your Latest SWS MPPE.CSV ')
uploaded_file = st.file_uploader(
    "Fill out the project plan template and upload your file here. After you upload the file, you can edit your project plan within the app.",
    type=['csv'],
)
if uploaded_file is not None:
    Tasks = pd.read_csv(uploaded_file)
    Tasks['Start'] = Tasks['Start'].astype('datetime64')
    Tasks['Finish'] = Tasks['Finish'].astype('datetime64')

    grid_response = AgGrid(
        Tasks,
        editable=True,
        height=300,
        width='100%',
    )

    updated = grid_response['data']
    df = pd.DataFrame(updated)

    # Main interface - section 3
    st.subheader('Step 2: Generate the Gantt chart')

    Options = st.selectbox("View Gantt Chart by:", ['Factory', 'Line', 'Product', 'Station'], index=0)
    if st.button('Generate Gantt Chart'):
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Product", color=Options, hover_name="Station")

        fig.update_yaxes(
            autorange="reversed"
        )  # if not specified as 'reversed', the tasks will be listed from bottom up

        fig.update_layout(
            title='SWS Abnormal Station Issue Tracking',
            hoverlabel_bgcolor='#DAEEED',  # Change the hover tooltip background color to a universal light blue color. If not specified, the background color will vary by team or completion pct, depending on what view the user chooses
            bargap=0.2,
            height=600,
            xaxis_title="",
            yaxis_title="",
            title_x=0.5,  # Make title centered
            xaxis=dict(
                tickfont_size=15,
                tickangle=270,
                rangeslider_visible=True,
                side="top",  # Place the tick labels on the top of the chart
                showgrid=True,
                zeroline=True,
                showline=True,
                showticklabels=True,
                tickformat="%x\n",  # Display the tick labels in certain format. To learn more about different formats, visit: https://github.com/d3/d3-format/blob/main/README.md#locale_format
            ),
        )

        fig.update_xaxes(tickangle=0, tickfont=dict(family='Rockwell', color='blue', size=15))

        st.plotly_chart(fig, use_container_width=True)  # Display the plotly chart in Streamlit

        st.subheader('Step 3: Generate the HTML')

        buffer = io.StringIO()
        fig.write_html(buffer, include_plotlyjs='cdn')
        html_bytes = buffer.getvalue().encode()
        st.download_button(label='Export to HTML', data=html_bytes, file_name='SWS_Issue_Track.html', mime='text/html')
    else:
        st.write('---')

else:
    st.warning('You need to upload a csv file.')
