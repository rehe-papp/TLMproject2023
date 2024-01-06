"""
loen llm andmed sisse -
    nimetatud by model-prompt
    grouped by prompt
    
inimandmed sisse"""
import pandas as pd
import warnings
from scipy.stats import ttest_1samp

# Disable deprecation warnings for DataFrame.append
warnings.filterwarnings("ignore", category=FutureWarning, module="pandas.core.frame")


path_list = ["cue_dataset_pos.csv", "prompt_0_data_pos.csv", "prompt_1_data_pos.csv", "prompt_2_data_pos.csv",
             "gpt4_prompt_0_data_pos.csv", "gpt4_prompt_1_data_pos.csv", "gpt4_prompt_2_data_pos.csv"]
model_name_list = ["Human", "gpt3_0", "gpt3_1", "gpt3_2", "gpt4_0", "gpt4_1", "gpt4_2"]

def calculate(path_list, model_name_list):
    # Create base df-s
    result_df = pd.DataFrame(columns=['Model','Cues', 'Synonym_Count', 'Total_Count', 'p'])
    short_df = pd.DataFrame(columns=['Model', 'p'])
    
    for i in range(len(path_list)):
        # Read in data
        with open(path_list[i], "r") as prompts:
            df = pd.read_csv(prompts)
        
        model_name = model_name_list[i]
        
        # Calculate the counts based on conditions
        synonym_count = df[df['Synonym'] == True].groupby('Cues').size().reset_index(name='Synonym_Count')
        total_count = df.groupby('Cues').size().reset_index(name='Total_Count')

        together = pd.merge(synonym_count, total_count, on="Cues", how="left")
        together['Model'] = model_name

        s = sum(together["Synonym_Count"])/sum(together["Total_Count"])
        together['p'] = together["Synonym_Count"]/together["Total_Count"]

        result_df = pd.concat([result_df, together], ignore_index=True)
        short_df = pd.concat([short_df, pd.DataFrame({'Model': [model_name], 'p': [s]})], ignore_index=True)
    
    return result_df, short_df



results, short = calculate(path_list, model_name_list)

print(results.head(5))
print(short)

# Perform a one sample T-Test for each model compared to humans
# H0: the mean of the synonym-percentage of LLM datasets is the same as the expected mean of the human dataset
# The models have values significantly different from humans if p < 0.05

test_df = pd.DataFrame(columns=['Model', 'T Statistic', 'p-value'])
human_mean = short[short['Model'] == 'Human']['p'].values[0]

for model in short['Model']:
    if model != 'Human':
        model_values = results[results['Model'] == model]['p']

        # Paired t-test
        t_stat, p_value = ttest_1samp(a=model_values, popmean=human_mean)
        print(t_stat,"is t and p is",p_value)

        # Create a df for the current test and append to the results
        test_result = pd.DataFrame({'Model': [model], 'T Statistic': [t_stat], 'p-value': [p_value]})
        test_df = pd.concat([test_df, test_result], ignore_index=True)


test_df.to_csv("t-test.csv")