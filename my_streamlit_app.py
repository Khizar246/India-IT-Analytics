import streamlit as st
import pandas as pd
import plotly.express as px
import os
import csv
import urllib3
import time
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Verify Python version
python_version = sys.version
st.write(f"Python version: {python_version}")
logging.debug(f"Python version: {python_version}")

# Verify gradientai package installation
try:
    import gradientai
    st.write("gradientai version:", gradientai.__version__)
    logging.debug(f"gradientai version: {gradientai.__version__}")
    gradientai_files = os.listdir(os.path.dirname(gradientai.__file__))
    logging.debug(f"gradientai package contents: {gradientai_files}")
except ImportError as e:
    st.error(f"ImportError: {e}")
    logging.error(f"ImportError: {e}")

# Attempt to import Gradient from the correct module
try:
    from gradientai._gradient import Gradient
    st.write("Gradient imported successfully from gradientai._gradient.")
    logging.debug("Gradient imported successfully from gradientai._gradient.")
except ImportError as e:
    st.error(f"ImportError: {e}")
    logging.error(f"ImportError: {e}")

try:
    # Loading the main website data
    main_website_data = pd.read_csv("Final_Data.csv")
    logging.info("Main website data loaded successfully.")

    # Set the title of the Streamlit page with custom formatting
    st.markdown('<h1 style="font-weight: bold; font-size: 36px; margin-bottom: 20px;">IT Skills and Salary Trends in India</h1>', unsafe_allow_html=True)

    # Verify environment variables
    gradient_access_token = os.environ.get('GRADIENT_ACCESS_TOKEN')
    gradient_workspace_id = os.environ.get('GRADIENT_WORKSPACE_ID')
    st.write("GRADIENT_ACCESS_TOKEN:", gradient_access_token)
    st.write("GRADIENT_WORKSPACE_ID:", gradient_workspace_id)
    logging.debug(f"GRADIENT_ACCESS_TOKEN: {gradient_access_token}")
    logging.debug(f"GRADIENT_WORKSPACE_ID: {gradient_workspace_id}")

    # Create a list of unique job titles
    job_titles = ['all'] + main_website_data['TITLE'].unique().tolist()
    logging.info("Job titles loaded.")

    # Create a list of unique categories including "All"
    categories = ['all'] + main_website_data['CATEGORY'].unique().tolist()
    logging.info("Categories loaded.")

    # Create a sidebar with tabs
    selected_tab = st.sidebar.selectbox("Select a Tab", ["Skills Analysis", "Salary", "Career Recommendation", "My Profile", "About"])

    if selected_tab == "Skills Analysis":
        # Create a sidebar to select job title and category
        selected_title = st.sidebar.selectbox("Select a Job Title", job_titles)
        selected_category = st.sidebar.selectbox("Select a Category", categories)

        if selected_title == 'all' and selected_category == 'all':
            st.subheader("Skills Required for All Job Titles")
            skill_counts = main_website_data['SKILLS'].str.split(', ').explode().value_counts().sort_index(ascending=True)
            total_skills = skill_counts.sum()
            percentages = (skill_counts / total_skills) * 100

            skill_df = pd.DataFrame({'Skills': skill_counts.index, 'Count': skill_counts.values, 'Percentage': percentages.values})
            skill_df = skill_df.sort_values(by='Count', ascending=True)
            skill_df['Percentage'] = skill_df['Percentage'].round(1).astype(str) + '%'

            fig = px.bar(skill_df, x='Count', y='Skills', text='Percentage', labels={'Count': 'Skill Count', 'Percentage': 'Percentage'})
            fig.update_xaxes(title=None, showticklabels=False)
            fig.update_layout(width=1000, height=800, showlegend=False)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        else:
            if selected_title != 'all':
                selected_data = main_website_data[main_website_data['TITLE'] == selected_title]
                st.subheader(f"Skills Required for {selected_title}")
            if selected_category != 'all':
                selected_data = selected_data[selected_data['CATEGORY'] == selected_category] if selected_title != 'all' else main_website_data[main_website_data['CATEGORY'] == selected_category]
                st.subheader(f"Skills Required for {selected_title if selected_title != 'all' else 'all'} in {selected_category} Category")
            if selected_data.empty:
                st.warning("Oh, snap! We're currently in data collection mode for your requested graph, and it's like hunting for unicorns right now – pretty rare stuff! 😅")
            else:
                skill_counts = selected_data['SKILLS'].str.split(', ').explode().value_counts().sort_index(ascending=True)
                total_skills = skill_counts.sum()
                percentages = (skill_counts / total_skills) * 100

                skill_df = pd.DataFrame({'Skills': skill_counts.index, 'Count': skill_counts.values, 'Percentage': percentages.values})
                skill_df = skill_df.sort_values(by='Count', ascending=True)
                skill_df['Percentage'] = skill_df['Percentage'].round(1).astype(str) + '%'

                fig = px.bar(skill_df, x='Count', y='Skills', text='Percentage', labels={'Count': 'Skill Count', 'Percentage': 'Percentage'})
                fig.update_xaxes(title=None, showticklabels=False)
                fig.update_layout(width=1000, height=800, showlegend=False)
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

    elif selected_tab == "Salary":
        job_title_option = st.sidebar.radio("Select Job Title", ("Note", "Specific Job Title"))

        if job_title_option == "Note":
            st.subheader("Salary Note")
            st.write("Certainly! It's important to view the provided salary as a general reference. Salaries in the field can fluctuate significantly based on factors such as your experience, location, skill set, the company you work for, and more. Think of this figure as a starting point, but it's crucial to conduct thorough research and consider various elements that contribute to the overall compensation package.")
            st.write("Please select a specific job title in the 'Specific Job Title' tab to view detailed salary information.")

        elif job_title_option == "Specific Job Title":
            selected_title = st.sidebar.selectbox("Select a Job Title", job_titles[1:])

            if selected_title:
                st.subheader(f"Average Salary for {selected_title}")
                selected_data = main_website_data[main_website_data['TITLE'] == selected_title]
                if selected_data.empty:
                    st.warning("Oh, snap! We're currently in data collection mode for your requested graph, and it's like hunting for unicorns right now – pretty rare stuff! 😅")
                else:
                    avg_salary = selected_data.groupby('EXPERIENCE')['SALARY'].mean().reset_index()
                    avg_salary['SALARY'] = avg_salary['SALARY'].apply(lambda x: round(x, -5))
                    avg_salary = avg_salary.sort_values(by='SALARY', ascending=False)
                    fig_salary = px.bar(avg_salary, x='EXPERIENCE', y='SALARY', text=avg_salary['SALARY'].astype(str), labels={'EXPERIENCE': 'Experience (years)', 'SALARY': 'Average Salary (₹)'})
                    if selected_title == 'all':
                        fig_salary.update_xaxes(title=None, showline=False, showticklabels=False)
                    fig_salary.update_yaxes(title=None)
                    fig_salary.update_traces(texttemplate='%{text} ₹', textposition='outside')
                    st.plotly_chart(fig_salary, use_container_width=True)

    elif selected_tab == "Career Recommendation":
        gradient_access_token = os.environ['GRADIENT_ACCESS_TOKEN']
        gradient_workspace_id = os.environ['GRADIENT_WORKSPACE_ID']
        career_dataset_path = r"C:\Users\khize\Study_Material\Projects\Career_recommendation\Career_recommendation_data.csv"

        gradient = Gradient()

        formatted_data = []
        with open(career_dataset_path, encoding="utf-8-sig") as f:
            dataset_data = csv.DictReader(f, delimiter=",")
            for row in dataset_data:
                user_data = f"Interests: {row['Interests']}, Skills: {row['Skills']}, Degree: {row['Undergraduate Course']}, Working: {row['Employment Status']}"
                career_response = row['Career Path']
                formatted_entry = {
                    "inputs": f"### User Data:\n{user_data}\n\n### Suggested Career Path:",
                    "response": career_response
                }
                formatted_data.append(formatted_entry)

        base = gradient.get_base_model(base_model_slug="nous-hermes2")
        new_model_adapter = base.create_model_adapter(name="ai_career_recommender")
        chunk_size = 50
        total_chunks = [formatted_data[x:x+chunk_size] for x in range(0, len(formatted_data), chunk_size)]
        for i, chunk in enumerate(total_chunks):
            new_model_adapter.fine_tune(samples=chunk)

        st.subheader("Career Recommendation Bot")
        with st.form(key='user_input_form'):
            interests = st.text_input("Enter your interests:")
            skills = st.text_input("Enter your skills:")
            degree = st.text_input("Enter your degree:")
            working_status = st.text_input("Currently working? (Yes/No):")
            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            user_query = f"Interests: {interests}\nSkills: {skills}\nDegree: {degree}\nCurrently working? (Yes/No): {working_status}"
            formatted_query = f"### User Data:\n{user_query}\n\n### Suggested Career Path:"
            retries = 3
            while retries > 0:
                try:
                    response = new_model_adapter.complete(query=formatted_query, max_generated_token_count=500)
                    break
                except Exception as e:
                    st.error(f"Attempt failed due to error: {e}")
                    logging.error(f"Attempt failed due to error: {e}")
                    retries -= 1
                    if retries > 0:
                        st.warning("Retrying...")
                        time.sleep(5)
                    else:
                        raise

            st.subheader("Recommended Career Path")
            st.write(f"Based on the inputs you provided, a recommended career path for you is: {response.generated_output}")

    elif selected_tab == "My Profile":
        st.header("My Profile")
        st.write("Mohd Khizar is a budding professional in the realm of data analytics and technology. With a solid background in data analysis and a deep passion for data visualization, I'm on a dedicated journey to evolve into a proficient data scientist. Although I'm just at the beginning of my career, which kicked off a mere two months ago, I'm already driven to leave a significant mark on the industry.")
        st.write("My commitment to data doesn't stop at the workplace. I've actively engaged in various projects, including web scraping, exploratory data analysis, prediction models, Tableau dashboards and much more. These endeavors not only reflect my thirst for knowledge but also underscore my genuine enthusiasm for the art of data.")
        st.write("On my path of continuous learning, I've pursued certifications in areas like data visualization, machine learning, Excel proficiency, SQL fundamentals, and Python data structures and algorithms. These certifications not only serve as evidence of my dedication to self-improvement but also as a testament to my eagerness to contribute to the vibrant data science community. I'm thrilled about the journey ahead as I strive to become a skilled data scientist and share my expertise and insights in this dynamic field.")
        st.write("I seek guidance from everyone in this wonderful Data Science community and I am willing to share my knowledge as well")
        st.write("1.[My LinkedIn](https://www.linkedin.com/in/khizar246/)")
        st.write("2.[My Tableau profile](https://public.tableau.com/app/profile/mohd.khizer/vizzes)")
        st.write("3.[My portfolio](https://www.datascienceportfol.io/Khizar246)")

    elif selected_tab == "About":
        st.header("About")
        st.write("1. Project Description: This project is a testament to my journey as a data enthusiast and aspiring data scientist. It's a project that revolves around exploring the intricate world of IT job skills and salaries, utilizing a dataset meticulously collected and cleaned. This project combines data analysis, data visualization, and Python programming to uncover valuable insights that can help both job seekers and employers in the IT industry.")
        st.write("2. Skills Utilized: Throughout this project, I've harnessed a diverse skill set, including data cleaning, exploratory data analysis, and data visualization. I've implemented Python programming to process and analyze the dataset, employing Pandas for data manipulation and Plotly Express for creating interactive visualizations. The ability to work with real-world data, extract meaningful information, and communicate findings effectively through visualizations and narratives has been crucial to this project.")
        st.write("3. Motivation and Future Plans: The motivation behind this project stems from a passion for data-driven decision-making and a desire to bridge the gap between job seekers and employers in the IT sector. As I continue to learn and grow in the data science field, my future plans for this project involve expanding its scope and functionality. I aim to enhance the interactivity of the data visualizations, incorporate machine learning models for predictive analysis, and provide users with a comprehensive platform for exploring IT job market trends. Ultimately, I see this project evolving into a valuable resource for job seekers, employers, and data enthusiasts looking to gain insights into the ever-evolving IT job landscape.")
        st.write("For more information, you can refer to the following resources:")
        st.write("1. [Link to Dataset](https://www.kaggle.com/datasets/khizar246/it-jobs-in-india)")
        st.write("2. [GitHub Repository](https://github.com/Khizar246/Data-Analytics/blob/main/Job_Project.ipynb)")
        st.write("3. [YouTube](https://www.youtube.com/watch?v=7G_Kz5MOqps). This is from where I got the inspiration but Luke's project is way more advanced")

    st.markdown('<hr style="border-top: 1px solid #e5e5e5;">', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 14px; color: #808080; text-align: center;">Designed by Mohd Khizar</p>', unsafe_allow_html=True)

except Exception as e:
    logging.error(f"Error occurred: {e}")
    st.error(f"An error occurred: {e}")
