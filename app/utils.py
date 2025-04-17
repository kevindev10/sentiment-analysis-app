from google import genai
from google.genai import types
import os
from sqlalchemy.orm import Session
import threading
from concurrent.futures import ThreadPoolExecutor
import crud, models


# Only run this block for Gemini Developer API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#Define a semaphore to limit the number of concurrent threads
semaphore = threading.Semaphore(5) #Adjust the number of concurrent threads as needed

def generate_content(db: Session, topic: str) -> str:
   with semaphore:
      search_term = crud.create_search_term(db, topic)
      if not search_term:
         search_term = crud.create_search_term(db, topic)

      # response = client.generate_text(
      #    model="gemini",
      #    prompt=types.Prompt(
      #       text=f"Write a blog post about {topic} using the keyword {search_term}.",
      #    ),
      #    temperature=0.7,
      #    max_output_tokens=300,
      # )
      

      response = client.models.generate_content(
          model="gemini-2.0-flash",
          contents=f"Write a blog post about {topic} using the keyword {search_term}."
      )
      # print(response)

      # print(response.text)
      text_content = response.candidates[0].content.parts[0].text
      print(text_content)
      generated_text = text_content
      crud.create_generated_content(db, generated_text, search_term.id)

      return generated_text