import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GOOGLE-GEMINI-API")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal"
    elif 25.0 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obesity"


# st.set_page_config(page_title="HEALTHIFY", layout="centered")

st.title(":orange[HEALTHIFY] :blue[AI Powered Personal Health Assistant]")
st.markdown(
    "##### This application helps you live a healthier life with personalized guidance."
)

st.info(
    """
    **How to use:**
    - Enter your details in the sidebar
    - Provide your health-related question
    - Get personalized health insights
    """
)


st.sidebar.header(":red[ENTER YOUR DETAILS]")

name = st.sidebar.text_input("Enter your name")
gender = st.sidebar.selectbox("Select your gender", ["Male", "Female"])
age = st.sidebar.text_input("Enter your age (years)")
weight = st.sidebar.text_input("Enter your weight (kg)")
height = st.sidebar.text_input("Enter your height (feet)")
fitness = st.sidebar.slider("Rate your fitness (0 = Poor, 5 = Excellent)", 0, 5)


bmi = None
bmi_status = None

if height and weight:
    try:
        height_feet = pd.to_numeric(height)
        weight_kg = pd.to_numeric(weight)

        if height_feet > 0 and weight_kg > 0:
            bmi = round(weight_kg / (((height_feet * 30.48) / 100) ** 2), 2)
            bmi_status = bmi_category(bmi)

            st.sidebar.success(
                f"""
                **{name}'s BMI Details**
                - **BMI:** {bmi} kg/m²
                - **Category:** {bmi_status}
                """
            )
        else:
            st.sidebar.error("Height and weight must be positive numbers.")
    except:
        st.sidebar.error("Please enter valid numeric values for height and weight.")


user_query = st.text_input("Enter your health-related query")

if st.button("Get Health Advice"):
    if not name:
        st.warning("Please enter your name.")
    elif not user_query:
        st.warning("Please enter your query.")
    else:
        prompt = f"""
Assume you are a certified health expert.

User Details:
- Name: {name}
- Gender: {gender}
- Age: {age} years
- Weight: {weight} kg
- Height: {height} cm
- BMI: {bmi} kg/m^2
- BMI Category: {bmi_status}
- Fitness Level: {fitness}/5

User Query:
{user_query}

Instructions:
- Start with a brief comment on the user's health profile
- Identify the core health concern
- Explain possible reasons
- Suggest lifestyle-based solutions only
- Mention relevant doctor specialization if required
- DO NOT recommend medicines
- Use bullet points and tables if helpful
- End with a 5–7 line summary
"""

        with st.spinner("Analyzing your health profile..."):
            response = model.generate_content(prompt)

        st.success("Here is your personalized health guidance 👇")
        st.write(response.text)

