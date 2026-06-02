from groq import Groq
from groq import RateLimitError, APIError

from dotenv import load_dotenv
import os


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



def generate_response(prompt):


    try:


        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an expert legal contract reviewer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.1
        )



        return response.choices[0].message.content




    except RateLimitError as e:


        print(
            "Groq rate limit reached:",
            e
        )


        return {
            "error":
            "AI usage limit reached. Please try again after some time."
        }




    except APIError as e:


        print(
            "Groq API error:",
            e
        )


        return {
            "error":
            "AI service temporarily unavailable."
        }




    except Exception as e:


        print(
            "Unexpected LLM error:",
            e
        )


        return {
            "error":
            "Something went wrong while generating AI response."
        }