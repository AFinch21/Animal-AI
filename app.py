import streamlit as st
import requests
import pandas as pd
import json


st.title("AI Animal Wars")
st.write("This application allows players to create fantasitcal beasts and pit them against each other")

number = st.number_input("Insert a number", value=None, placeholder="Type a number...")
st.divider()

if number is not None:
    for value in range(1,int(number)+1):
        st.header(f"Player {value} define your animal")
        col1, col2, col3 = st.columns(3)

        with col1:
            head = st.text_input("Head", value=None, placeholder="Describe the head...", key=f"head_{value}")
            

        with col2:
            body = st.text_input("Body", value=None, placeholder="Describe the body...", key=f"body_{value}")

        with col3:
            ext = st.text_input("Extremeties", value=None, placeholder="Describe the extremities...", key=f"ext_{value}")
        st.divider()

    if st.button("Create and Fight!"):
        st.info("Generating outputs from model...")
        urls = []
        lore = {}
        for value in range(1, int(number)+1):
            prompts = {
                "head":st.session_state[f"head_{value}"],
                "body":st.session_state[f"body_{value}"],
                "ext":st.session_state[f"ext_{value}"],
                }

            # Send the HTTP POST request to the FastAPI endpoint
            response = requests.post("http://127.0.0.1:8000/process_image", json=prompts)
            if response.status_code == 200:
                st.header(f"Player {value} Animal")
                st.write(f"Lore:")
                st.write(f"{response.json()['Lore']}")

                st.image(response.json()['Image_URL'])
                urls.append(response.json()['Image_URL'])
                lore.update({f"Animal_{value}" : f"{response.json()['Lore']}"})

        comparison_prompts = {
                "urls":urls,
                "lore":lore,
                }

        print(comparison_prompts)
        
        comparison = requests.post("http://127.0.0.1:8000/compare_images", json=comparison_prompts)
        

        st.header(f"Who would win?")
        st.write(f"{comparison.json()['Comparison']}")
