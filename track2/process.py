import os
import sys

# Imports necessary modules for API interaction, multiprocessing, and callbacks
from codeinterpreterapi import CodeInterpreterSession, settings
from multiprocessing import Pool, current_process
from langchain.callbacks import get_openai_callback
from functools import partial

import jsonlines
import json
import re
import time

# Set API key and model parameters for OpenAI GPT-4
settings.OPENAI_API_KEY = "sk-XXX"
settings.MODEL = 'gpt-4-1106-preview'
settings.MAX_RETRY = 3
settings.MAX_ITERATIONS = 4

# Define the base prompts for the AI model
base_prompt = "Solve the problem and put your answer in\\boxed{}. The problem is:"
after_prompt = "Please put your final answer to the problem in \\boxed{}."

# Regex pattern to extract the answer from the model's response
pattern = r'\\boxed\{(.*?(?:\{.*?\}.*?)*?)\}'
def get_answer(content):
    """
    Extracts the answer from the AI model's response using regex.
    """
    match = re.findall(pattern, content, re.DOTALL)
    return match

def call_gpt4_api(line):
    """
    Calls the GPT-4 API to solve a given problem and returns the solution.
    """
    problem = line['problem']
    with get_openai_callback() as cb:
        with CodeInterpreterSession(verbose=True) as session:
            # Generate a response based on user input
            response = session.generate_response(base_prompt + problem)
            match = get_answer(response.content)
            
            # Retry with a different prompt if no answer found
            if len(match) == 0:
                response = session.generate_response(after_prompt)
                match = get_answer(response.content)
            # If still no answer, return empty match
            if len(match) == 0:
                match = [""]
        
        # Print out the token usage and cost details
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

    return {'queId': line['queId'], 'difficulty': line['difficulty'], 'response': match[-1]}

def process_prompt(result_path, line):
    """
    Processes each problem by calling the GPT-4 API and saves the results to a file.
    """
    queid = line['queId']
    stdout_backup = sys.stdout  # Backup the current stdout
    with open(f'{result_path}/{queid}.txt', 'w', encoding='UTF-8') as f:
        sys.stdout = f  # Redirect stdout to file
        try:
            result = call_gpt4_api(line)
            print(json.dumps(result))  # Printing results will be written to a file
        except Exception as exc:
            sys.stdout = stdout_backup
            print(f'{queid} generated an exception: {exc}')
            time.sleep(60)
        else:
            sys.stdout = stdout_backup  # Recover stdout
            print(json.dumps(result))
    time.sleep(1)

def main():
    """
    Main function to process a dataset of problems using multiprocessing.
    """
    file_name = './dataset/TAL-SAQ6K-EN.jsonl'
    result_path = './results/code_interpreter/'
    partial_func = partial(process_prompt, result_path)
    lines = []
    
    # Read problems from a JSON lines file
    with open(file_name, "r", encoding='utf-8') as f:
        for line in jsonlines.Reader(f):
            lines.append(line)

    # Use multiprocessing to process each problem
    with Pool(4) as pool:
        pool.map(partial_func, lines)

if __name__ == '__main__':
    main()
