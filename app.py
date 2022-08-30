import streamlit as st
import requests
from gad import detect_gender_age
import openai
import names
from ageList import ageList

def get_person():
    r = requests.get("https://thispersondoesnotexist.com/image", headers={'User-Agent': 'My User Agent 1.0'}).content
    return r

def save_person(filename: str, picture: bytes):
    with open(filename, "wb") as f:
        return f.write(picture)

def get_person_story(gender:str, age: str, emotion: str):
    response = openai.Completion.create(
    prompt=f"Write a story that is {emotion} in first person about a {gender.lower()} that is an {ageList[age]} and add a famous quote at the end",
    temperature=0.45,
    max_tokens=800,
    top_p=1,
    best_of=1,
    frequency_penalty=0.3,
    presence_penalty=0,
    engine="text-davinci-002",
    )
    return response["choices"][0]["text"].strip()

def write_header():
    st.title("Humans of Neverland")
    st.write(f"""
        Take yourself on an emotional rollercoaster, by reading touching stories about people that... never existed. 

        *Inspired by Humans of New York*
        """)

def get_person_image():
    image = get_person()
    save_person("person.jpg", image)
    st.image("person.jpg")


def create_a_story(emotion: str):
    with st.spinner(text='We are finding a right person...'):
        get_person_image()
        gender, age = detect_gender_age("person.jpg")

    with st.spinner(text=f'We are discovering a story about a {ageList[age]} {gender.lower()}...'):
        story = get_person_story(gender, age, emotion)
        name_surname = names.get_full_name(gender=gender)
        st.markdown(f'# A {emotion} story of {name_surname}')
        st.markdown(story)


def app():
    write_header()
    api_key = st.sidebar.text_input("OpenAI API Key:", type="password")
    
    if api_key:
        openai.api_key = api_key
        emotion = st.text_input("Describe a mood for a story")
        if st.button('Submit'):
            create_a_story(emotion)
    else:
        st.error("🔑 API Key Not Found!")
        st.info("💡 Copy paste your OpenAI API key that you can find in User -> API Keys section once you log in to the OpenAI API Playground")


