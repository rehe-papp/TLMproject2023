import re
import pandas as pd

df = pd.DataFrame(columns=['Cues','Targets','Sample Size', 'Count'])

# all files from the same prompt
file_list = ["response_prompt_2_30_times_1.txt", "response_prompt_2_30_times_2.txt", "response_prompt_2_30_times_3.txt"
             , "response_prompt_2_30_times_4.txt", "response_prompt_2_30_times_5.txt"
             , "response_prompt_2_30_times_6.txt", "response_prompt_2_20_times_7.txt"]
#file_list = ["response_prompt_0_10_times_1.txt"]

for filename in file_list:
    
    with open(filename, "r") as f:
        lines = f.readlines()
        
    # Filter out empty rows
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    for line in non_empty_lines:
        line_clean = line.strip()
        # Split at ":" or "-"
        line_split = re.split(':|-', line_clean)
        print(line_split)
        
        if len(line_split) < 2:
            pass

        # find splitting token
        cue = line_split[0].strip().split()[-1].upper()
        response = line_split[1].strip().upper()
        
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

df.to_csv('prompt_2_data.csv', index=False)