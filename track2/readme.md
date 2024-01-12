# AAAI2024 COMPETITION ON MATH PROBLEM SOLVING - TRACK2

by CPDP-ICST

## Before Replication
In this competition, we integrated the chatGPT assistant API with the results from the [code interpreter](https://github.com/shroominic/codeinterpreter-api). Given that the latter might encounter various bugs during execution and the former has relatively good performance, it is recommended to prioritize using the chatGPT assistant API for replication.

<br/>

## Install dependencies for api(Recommend)

```
conda create -y -n API python=3.9
conda activate API
pip install -r api_requirements.txt
```

<br/>

## Install dependencies for Code Interpreter

```
conda create -y -n interpreter python=3.9
conda activate interpreter
pip install -r code_requirements.txt
```
You can also refer to Code Interpreter to install the necessary dependencies.

<br/>

## Create a GPT4 Assistant(1106-preview)

visit https://platform.openai.com/assistants, and create an new assistant, 

Set name="Math Tutor", instructions="You are a personal math tutor. Write and run code to answer math questions.", set code interpreter on and model = "gpt-4-1106-preview", then copy the assistant id for the variable assistant_id in api.py

or in the api.py you can use following code to create an assistant. Pay attention not to create duplicates!

```python
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)
```

<br/>

## Running: chatGPT assistant API(Recommend)

1. Complete the assistant_id and OPENAI_API_KEY in the api.py, check if the global path is correct, then run python api.py to start.
2. Run match.py and compile the answers into result.txt
3. Run generate.py to create a submission file that meets the specifications.
4. Optional: Run repeat.py to vote on the answers for repeated questions and select the most frequent one as the final answer.
5. Post-processing: Cleanse some answers that do not conform to the float format to ensure they meet the submission standards, for example, converting "2 days" to "2".
   
<br/>

## Running: Code Interpreter

1. Complete the "settings.OPENAI_API_KEY" in the api.py, then run python process.py to start.
2. Run match.py and compile the answers into result.txt
3. Run generate.py to create a submission file that meets the specifications.
4. Optional: Run repeat.py to vote on the answers for repeated questions and select the most frequent one as the final answer.
5. Post-processing: Cleanse some answers that do not conform to the float format to ensure they meet the submission standards, for example, converting "2 days" to "2".
   
<br/>

## Cost

It might cost $2-300 each method and take a few days to completely obtain all the answers for this competition's questions.

## Attention

Due to network and various other reasons, there may be instances where the GPT-4 response is empty. Simply retesting can resolve this issue.