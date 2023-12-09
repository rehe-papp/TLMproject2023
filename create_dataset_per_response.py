import re
import pandas as pd

df = pd.DataFrame(columns=['Cues','Targets','Sample Size', 'Count'])

# all files one by one
filename = "./Prompted data/GPT4 responses/prompt3_creative/response_"

# Cues
words = list()
with open('words.txt', encoding="UTF-8") as f:
    for line in f:
        words.append(line.strip())

# have to change how to read in files
# then change how to make pairs, probably bring together by positioning
# put into df the same way

for i in range(0,100):
    
    with open(filename+str(i)+".txt", "r") as f:
        content = f.read()
    
    response_list = content.strip('.\n').split(',')
    
    # Filter out responses with wrong number of responses
    if len(response_list) != 100:
        print("Response "+str(i)+" is dysfunctional", len(response_list))
        continue
    
    for el in range(len(response_list)):
        response = response_list[el].strip().upper()
        cue = words[el].upper()
        
        #print(cue,"is the cue")
        #print(response,"is the response")
        
        # Check if the cue and target pair already exist in the DataFrame
        if ((df['Cues'] == cue) & (df['Targets'] == response)).any():
            # If it exists, increment the count
            df.loc[(df['Cues'] == cue) & (df['Targets'] == response), 'Count'] += 1
        else:
            # If it doesn't exist, create a new DataFrame with the current values
            new_row = pd.DataFrame({'Cues': [cue], 'Targets': [response], 'Count': [1]})
            # Concatenate the new DataFrame with the existing DataFrame
            df = pd.concat([df, new_row], ignore_index=True)

# Calculate and update the 'Sample Size'
for cue in df['Cues'].unique():
    # Calculate the sample size for each unique cue
    sample_size = df.loc[df['Cues'] == cue, 'Count'].sum()
    # Update 'Sample Size' column for all occurrences of the current cue
    df.loc[df['Cues'] == cue, 'Sample Size'] = sample_size
print(df)

df.to_csv('gpt4_prompt_3_data.csv', index=False)

#um = "sailor, color, create, push, trustworthy, production, cavity, friend, creativity, alive, autumn, rainfall, neat, countryside, cheese, ornament, barrier, soldier, summary, fear, speculate, prevent, knot, ghost, protect, exterior, broadcast, vomit, corner, LosAngeles, protect, butterfly, toilet, fundamental, farewell, odd, buckle, think, shingles, risky, critical, harass, bright, monarch, slope, snack, fin, jump, eraser, jelly, angling, lead, policy, Nashville, choice, assault, cashier, event, officer, agreement, scared, cold, preacher, cinema, warning, woman, parasite, diploma, close, halt, common, tobacco, funeral, repair, divide, galaxy, retina, rigid, swear, bell, stop, talent, deceive, result, fur, banned, meteor, happiness, get, finance, drift, game, toy, sphere, territory, slope, worried, liquor, formula, star, companionship"

#print("ummm",len(um.split(',')))