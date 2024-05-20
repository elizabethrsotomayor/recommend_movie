import os
import google.generativeai as genai
import re
import requests
from headers import SESSION_HEADERS
import time
import urllib.parse
import streamlit as st

genai.configure(api_key=st.secrets['GENAI_API_KEY'])

class Recommend_movies:
    def __init__(self) -> None:
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }

        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                              generation_config=self.generation_config,
                              safety_settings=self.safety_settings)

        self.session = requests.Session()
        self.session.headers = SESSION_HEADERS

    def urlify_string(self,string):
        url_encoded = urllib.parse.quote(string)
        return url_encoded
    
    def generate(self, movie_name = str):
        
        result = []

        # prompt_parts = [
        #   {"role": "system", "content": f"{movie_name}"}
        # ]
        prompt_parts = [f"""
              "input: The Matrix",
              "output: Inception
                        The Terminator
                        Total Recall
                        Blade Runner
                        Looper",
              "input: {movie_name}",
              "output: ","""]
        
        response = self.model.generate_content(prompt_parts)
        recommendations = response.text.split("\n")

        time.sleep(0.1)

        for i in recommendations:
            movie = self.urlify_string(i)
            url = f"https://api.themoviedb.org/3/search/movie?query={movie}&include_adult=false&language=en-US&page=1"
            res = self.session.get(url).json()
            print(res)
            result.append(res["results"])

        return result
    
st.title("Movie Recommendation with Gemini Pro")
text_box = st.text_input("Your movie goes here 🎥")
col1, col2 = st.columns(2)

recom_movies = Recommend_movies()

if text_box:
    print(text_box)

    result = recom_movies.generate(str(text_box))

    for i in range(len(result)):
        if result[i] != []:
            if i % 2 == 0:
                col1.image(f"https://image.tmdb.org/t/p/w300_and_h450_bestv2{result[i][0]['poster_path']}")
                col1.write(result[i][0]['title'])
                col1.write(result[i][0]['overview'])
            else:
                col2.image(f"https://image.tmdb.org/t/p/w300_and_h450_bestv2{result[i][0]['poster_path']}")
                col2.write(result[i][0]['title'])
                col2.write(result[i][0]['overview'])