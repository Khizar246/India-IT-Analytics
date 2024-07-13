import streamlit as st
import pandas as pd
import plotly.express as px

# Load the main website data
@st.cache_data
def load_data():
    return pd.read_csv("Final_Data.csv")

data = load_data()

# Set the title of the Streamlit page with custom formatting
st.markdown('<h1 style="font-weight: bold; font-size: 36px; text-align: center; color: #4CAF50;">IT Skills and Salary Trends in India</h1>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
tab = st.sidebar.radio("Go to", ["Skills Analysis", "Salary", "My Profile", "About"])

# Sidebar for selecting job titles and categories
job_titles = ['All'] + data['TITLE'].unique().tolist()
categories = ['All'] + data['CATEGORY'].unique().tolist()

def plot_skills(data, title):
    skill_counts = data['SKILLS'].str.split(', ').explode().value_counts()
    skill_df = pd.DataFrame({'Skills': skill_counts.index, 'Count': skill_counts.values})
    fig = px.bar(skill_df, x='Count', y='Skills', orientation='h', text='Count', labels={'Count': 'Skill Count'}, title=title)
    fig.update_traces(marker_color='#4CAF50', textposition='outside')
    fig.update_layout(xaxis_title=None, yaxis_title=None, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_salary(data, title):
    avg_salary = data.groupby('EXPERIENCE')['SALARY'].mean().reset_index()
    fig = px.bar(avg_salary, x='EXPERIENCE', y='SALARY', text='SALARY', labels={'EXPERIENCE': 'Experience (years)', 'SALARY': 'Average Salary (₹)'}, title=title)
    fig.update_traces(marker_color='#4CAF50', texttemplate='%{text:.2s} ₹', textposition='outside')
    fig.update_layout(xaxis_title=None, yaxis_title=None, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

if tab == "Skills Analysis":
    st.sidebar.subheader("Filter Options")
    selected_title = st.sidebar.selectbox("Select Job Title", job_titles)
    selected_category = st.sidebar.selectbox("Select Category", categories)

    filtered_data = data.copy()
    if selected_title != 'All':
        filtered_data = filtered_data[filtered_data['TITLE'] == selected_title]
    if selected_category != 'All':
        filtered_data = filtered_data[filtered_data['CATEGORY'] == selected_category]

    if not filtered_data.empty:
        plot_skills(filtered_data, f"Skills Required for {selected_title} in {selected_category} Category" if selected_title != 'All' or selected_category != 'All' else "Skills Required for All Job Titles")
    else:
        st.warning("No data available for the selected filters.")

elif tab == "Salary":
    st.sidebar.subheader("Filter Options")
    selected_title = st.sidebar.selectbox("Select Job Title", job_titles[1:])

    if selected_title:
        filtered_data = data[data['TITLE'] == selected_title]
        if not filtered_data.empty:
            plot_salary(filtered_data, f"Average Salary for {selected_title}")
        else:
            st.warning("No data available for the selected job title.")

elif tab == "My Profile":
    st.header("My Profile")
    st.write("""
        **Mohd Khizar** is a budding professional in the realm of data analytics and technology. With a solid background in data analysis and a deep passion for data visualization, I'm on a dedicated journey to evolve into a proficient data scientist. Although I'm just at the beginning of my career, which kicked off a mere two months ago, I'm already driven to leave a significant mark on the industry.
        My commitment to data doesn't stop at the workplace. I've actively engaged in various projects, including web scraping, exploratory data analysis, prediction models, Tableau dashboards and much more. These endeavors not only reflect my thirst for knowledge but also underscore my genuine enthusiasm for the art of data.
        On my path of continuous learning, I've pursued certifications in areas like data visualization, machine learning, Excel proficiency, SQL fundamentals, and Python data structures and algorithms. These certifications not only serve as evidence of my dedication to self-improvement but also as a testament to my eagerness to contribute to the vibrant data science community. I'm thrilled about the journey ahead as I strive to become a skilled data scientist and share my expertise and insights in this dynamic field.
        I seek guidance from everyone in this wonderful Data Science community and I am willing to share my knowledge as well.
    """)
    st.write("1. [My LinkedIn](https://www.linkedin.com/in/khizar246/)")
    st.write("2. [My Tableau profile](https://public.tableau.com/app/profile/mohd.khizer/vizzes)")
    st.write("3. [My portfolio](https://www.datascienceportfol.io/Khizar246)")

elif tab == "About":
    st.header("About")
    st.write("""
        **Project Description:** This project is a testament to my journey as a data enthusiast and aspiring data scientist. It's a project that revolves around exploring the intricate world of IT job skills and salaries, utilizing a dataset meticulously collected and cleaned. This project combines data analysis, data visualization, and Python programming to uncover valuable insights that can help both job seekers and employers in the IT industry.
        **Skills Utilized:** Throughout this project, I've harnessed a diverse skill set, including data cleaning, exploratory data analysis, and data visualization. I've implemented Python programming to process and analyze the dataset, employing Pandas for data manipulation and Plotly Express for creating interactive visualizations. The ability to work with real-world data, extract meaningful information, and communicate findings effectively through visualizations and narratives has been crucial to this project.
        **Motivation and Future Plans:** The motivation behind this project stems from a passion for data-driven decision-making and a desire to bridge the gap between job seekers and employers in the IT sector. As I continue to learn and grow in the data science field, my future plans for this project involve expanding its scope and functionality. I aim to enhance the interactivity of the data visualizations, incorporate machine learning models for predictive analysis, and provide users with a comprehensive platform for exploring IT job market trends. Ultimately, I see this project evolving into a valuable resource for job seekers, employers, and data enthusiasts looking to gain insights into the ever-evolving IT job landscape.
    """)
    st.write("1. [Link to Dataset](https://www.kaggle.com/datasets/khizar246/it-jobs-in-india)")
    st.write("2. [GitHub Repository](https://github.com/Khizar246/Data-Analytics/blob/main/Job_Project.ipynb)")
    st.write("3. [YouTube](https://www.youtube.com/watch?v=7G_Kz5MOqps). This is from where I got the inspiration but Luke's project is way more advanced")

st.markdown('<hr style="border-top: 1px solid #e5e5e5;">', unsafe_allow_html=True)
st.markdown('<p style="font-size: 14px; color: #808080; text-align: center;">Designed by Mohd Khizar</p>', unsafe_allow_html=True)
