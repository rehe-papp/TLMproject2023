import json
import os
from openai import OpenAI
import pandas as pd

#client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:


csv_file = pd.read_csv("cue_dataset.csv")
words = list(csv_file.apply(set)[1])

prompt = ""

for word in words:
    prompt += f"{word}, "

print(prompt)


client = OpenAI(
   api_key="",
)

"""
Within the OpenAI API, messages often adopt specific roles to guide the model’s responses. 
Commonly used roles include “system,” “user,” and “assistant.” The “system” provides high-level 
instructions, the “user” presents queries or prompts, and the “assistant” is the model’s response. 
By differentiating these roles, we can set the context and direct the conversation efficiently.
"""


responses = list()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content":
            "For each word proposed, return one word that you would think "
            "would correspond most with that word. Return the words in the form: original word: response"},
        {"role": "user", "content": prompt}
    ]
)



outfile = open("response_words.txt", "w")

outfile.write(f"{response.choices[0].message.content}")
outfile.close()
#print(response.choices[0].message)