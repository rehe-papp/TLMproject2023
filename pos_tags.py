import pandas as pd
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet



with open("cue_dataset.csv", "r") as prompts:
    prompt_df = pd.read_csv(prompts)
    prompt_df['Part of Speech'] = ''
    

# Use simple pos tags
def simplify_pos(tag):
    if tag.startswith('N'):
        return 'N'  # Noun
    elif tag.startswith('V'):
        return 'V'  # Verb
    elif tag.startswith('R'):
        return 'ADV'  # Adverb
    elif tag.startswith('J'):
        return 'AJ'  # Adjective
    else:
        return tag  # Keep other tags as they are

def add_pos_tags(text):
    tokens = word_tokenize(text)
    pos_tags = [tag for _, tag in pos_tag(tokens)][0]
    simple_tags = simplify_pos(pos_tags)
    return simple_tags

# Apply the function to each row of the 'Targets' column
prompt_df['Part of Speech'] = prompt_df['Targets'].apply(add_pos_tags)
#print(prompt_df[~prompt_df['Part of Speech'].isin(['N', 'V','ADV','AJ'])])

# Define a function to check if two words are synonyms
def are_synonyms(word1, word2):
    synsets1 = wordnet.synsets(word1)
    synsets2 = wordnet.synsets(word2)
    return any(set1.pos() == set2.pos() for set1 in synsets1 for set2 in synsets2)


prompt_df['Synonym'] = prompt_df.apply(lambda row: are_synonyms(row['Cues'], row['Targets']), axis=1)

print(prompt_df.head)
prompt_df.to_csv("cue_dataset_pos.csv")

