import json
import os
from openai import OpenAI
import time
from dotenv import load_dotenv

load_dotenv(dotenv_path="C:/Users/Raiko/Desktop/code/TLMproject2023/CAUTION.env",verbose=True) #needed to load the API key from .env #REMOVE


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


def prompts_for_words_one_by_one(filename):
    """
    :param filename: name of txt file to read in the prompts, prompts should be in the form
    "text | index", where the text contains a gap at the 'index' into where the words will be inserted
    :return: a list of tuples, where the first element of the tuple is the text and second element is the index.
    """
    prompts = list()
    with open(f'{filename}.txt', encoding="UTF-8") as f:
        for line in f:
            res = line.strip().split(" | ")
            prompts.append((res[0], int(res[1])))
    return prompts


def run_prompt_all_words_one_by_one(words, prompt):
    """
    :param words: list of words to test
    :param prompt: prompt in the form of a tuple (text, index), where the text is the string of the prompt and
    index is where a word will be inserted.
    :return: returns the list of all the words returned
    """
    client = OpenAI()
    print(prompt)
    response_words = list()
    for word in words:
        time.sleep(3)
        prompt_to_send = insert_string(prompt[0], word.lower(), int(prompt[1]))
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
    return response_words


def run_prompt_100_words_together(words, prompt, filename):
    """
    :param words: list of words to test
    :param prompt: prompt, where there is the string <word>, where individual words will be inserted
    :param filename: name of the .txt file, where the results will be written
    """
    client = OpenAI() 
    response_words = list()
    words_to_send = ""
    for word in words:
        words_to_send += word+", "
    print(words_to_send)
    for i in range(20):
        time.sleep(1)
        prompt_to_send = "You are given a prompt and a list of words. For each word, replace the string '<word>' with a word from the list and give back a one word response, return answers for all words."
        try:
            # Timeout to keep loop from freezing
            response = client.with_options(timeout=30).chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt_to_send},
                    {"role": "user", "content": "prompt:" + prompt},
                    {"role": "user", "content": "words:" + words_to_send}
                ]
            )

            generated = response.choices[0].message.content
            #print(f"{generated}")
            response_words.append(generated)

        except Exception as e:
            print(f"Error during API call: {e}")

    outfile = open(f"{filename}.txt", "w")
    for line in response_words:
        outfile.write(line + "\n")
        outfile.write("\n")
    outfile.close()




words = list()
with open('words.txt', encoding="UTF-8") as f:
    for line in f:
        words.append(line.strip())

print(words)


#comment uncomment methods as you please


prompt = "Provide a word that evokes emotions or thoughts related to the word <word>."
run_prompt_100_words_together(words, prompt, "response_prompt_2_20_times_7")

#prompts = prompts_for_words_one_by_one("prompts")

#print(run_prompt_all_words_one_by_one(words, prompts[5]))

