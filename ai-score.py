import pandas as pd
import ollama
import tqdm
import ast

llm_model = "mistral:7b"

# Load the spreadsheet
df = pd.read_csv("sp_25_apps.csv", encoding="utf-8-sig")
df['Total Score 0'] = 0.0
df['Total Score 1'] = 0.0

list1 = []

def llm_q1_score(response):
    prompt = f"""
    Strictly evaluate the following response for the question "Why are you interested in ABA? What do you hope to gain from your team experience?":

    "{response}"

    Score it based on:
    - Relevance & Alignment (0-5 points): A good candidate will demonstrate their alignment with ABA's mission to develop well-rounded business leaders who put their skills to work and never compromise their humility, integrity, or passion for each other and the work that they do.
    - Specificity (0-5 points): A good answer will provide specific examples of how they want to contribute in the club, how they have been a leader in the past, or how they plan on giving back to ABA.
    - Passion & Authenticity (0-3 points): A good answer will highlight positive past experiences with ABA members and show genuine interest in joining the club and community.
    - Clarity & Grammar (0-2 points): A good answer will have zero grammar mistakes and have clear and concise thought.

    Remember to grade STRICTLY. ONLY return a python dictionary of the scores in exactly this order:
    Relevance: X, Specificity: X, Passion: X, Clarity: X
    """

    # Query the Llama model
    result = ollama.chat(model=llm_model, messages=[{"role": "user", "content": prompt}])

    return result["message"]["content"]

def llm_q2_score(response):
    prompt = f"""
    Strictly evaluate the following response for the question "Which of ABA's five core values best describe you? How do your past experiences demonstrate this value?":

    "{response}"

    Score it based on:
    - Relevance & Alignment (0-5 points): A good answer will explicitly mention one of five core values: #ABALOVE, #GAIN&GIVE, #INIT2GETHER, #BE, or #JSE and explain why they resonate with it.
    - Specificity (0-5 points): A good answer will provide an example demonstrating how they have exercised this value in the past or in some aspect of their life.
    - Passion & Authenticity (0-3 points): A good answer will highlight a positive past experience with real-world impact.
    - Clarity & Grammar (0-2 points): A good answer will have zero grammar mistakes and have clear and concise thought.

    ONLY return a python dictionary of the scores in exactly this order:
    'Relevance': X, 'Specificity': X, 'Passion': X, 'Clarity': X
    """

    # Query the Llama model
    result = ollama.chat(model=llm_model, messages=[{"role": "user", "content": prompt}])

    return result["message"]["content"]

# for i in tqdm.tqdm(range(df.shape[0])):
i=df.shape[0]-1
for j in range(9):
    response_1 = df.iloc[i, 8]
    response_2 = df.iloc[i, 9]

    q1_score = llm_q1_score(response_1)
    q1_dict = ast.literal_eval(q1_score)
    q1_composite = sum(q1_dict.values())

    q2_score = llm_q1_score(response_2)
    q2_dict = ast.literal_eval(q2_score)
    q2_composite = sum(q2_dict.values())

    list1 += [q1_composite+q2_composite]

    # df.loc[i, f"Total Score {j}"] = q1_composite + q2_composite

# Save results
#df.to_csv("sp_25_scored_applicants.csv", index=False)

print(list1)

print("Scoring complete! Results saved to scored_applicants.csv")
