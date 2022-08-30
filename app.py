import streamlit as st
import requests
from gad import detect_gender_age
import openai
import names

ageList={'(0-2)':'baby', '(4-6)':'kid', '(8-12)':'teenager', '(15-20)':'young adult', '(25-32)':'adult', '(38-43)':'middle age', '(48-53)':'older middle age', '(60-100)':'elderly'}

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



def app():

    st.title("Humans of Neverland")
    st.write(f"""
        Take yourself on an emotional rollercoaster, by reading touching stories about people that... never existed. 

        *Inspired by Humans of New York*
        """)

    api_key = st.sidebar.text_input("OpenAI API Key:", type="password")

    # Using the streamlit cache 
    # @st.cache
    # def process_prompt(input):
    #     return pred.model_prediction(input=input, api_key=api_key)
    
    if api_key:
        openai.api_key = api_key

        emotion = st.text_input("Describe a mood for a story")
        if st.button('Submit'):
            with st.spinner(text='We are finding a right person...'):
                image = get_person()
                save_person("person.jpg", image)
                st.image("person.jpg")
                gender, age = detect_gender_age("person.jpg")

            with st.spinner(text=f'We are discovering a story about a {ageList[age]} {gender.lower()}...'):
                story = get_person_story(gender, age, emotion)
                name = names.get_full_name(gender=gender)
                st.markdown(f'# A {emotion} story of {name}')
                st.markdown(story)
                # report_text = process_prompt(input)
                # st.markdown(report_text)
    else:
        st.error("🔑 API Key Not Found!")
        st.info("💡 Copy paste your OpenAI API key that you can find in User -> API Keys section once you log in to the OpenAI API Playground")


