import json
import os
from openai import OpenAI
import time
from dotenv import load_dotenv

load_dotenv() #needed to load the API key from .env


def insert_string(original, inserted, index):
    """
    Combine two strings by inserting the second string into the first string at the specified index.

    Parameters:
    - original (str): The original string.
    - inserted (str): The string to be inserted.
    - index (int): The index where the insertion should occur.

    Returns:
    - str: The combined string.
    """
    combined = original[:index] + inserted + original[index:]
    return combined



#client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:

words = list()
with open('words.txt', encoding="UTF-8") as f:
    for line in f:
        words.append(line.strip())

print(words)

prompts = list()
with open('prompts.txt', encoding="UTF-8") as f:
    for line in f:
        line = line.strip()
        res = line.split(" | ")
        prompts.append((res[0], int(res[1])))

print(prompts)


client = OpenAI()

"""
Within the OpenAI API, messages often adopt specific roles to guide the model’s responses. 
Commonly used roles include “system,” “user,” and “assistant.” The “system” provides high-level 
instructions, the “user” presents queries or prompts, and the “assistant” is the model’s response. 
By differentiating these roles, we can set the context and direct the conversation efficiently.
"""


"""responses = list()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content":
            "For each word proposed, return one word that you would think "
            "would correspond most with that word. Return the words in the form: original word: response"},
        {"role": "user", "content": prompt}
    ]
)"""

"""prompt = f"Generate a word related to {words[0]}"l"""

"""def createPrompt(prompt, word):
    return """

"""i = 0
for prompt in prompts:
    response_words = list()
    for word in words:
        time.sleep(2)
        prompt_to_send = insert_string(prompt[0], word.lower(), prompt[1])
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt_to_send}
                ]
            )

            generated_word = response.choices[0].message.content
            print(f"{generated_word}")
            response_words.append(generated_word)

        except Exception as e:
            print(f"Error during API call: {e}")

    outfile = open(f"response_words_prompt_{i}.txt", "w")
    for line in response_words:
        outfile.write(line + "\n")
    outfile.close()
    i += 1"""

i = 6
prompt = prompts[i]
response_words = list()
for word in words:
    time.sleep(3)
    prompt_to_send = insert_string(prompt[0], word.lower(), prompt[1])
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_to_send}
            ]
        )

        generated_word = response.choices[0].message.content
        print(f"{generated_word}")
        response_words.append(generated_word)

    except Exception as e:
        print(f"Error during API call: {e}")

outfile = open(f"response_words_prompt_{i}.txt", "w")
for line in response_words:
    outfile.write(line + "\n")
outfile.close()

