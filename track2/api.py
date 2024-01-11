# -*- coding: utf-8 -*-
import os
import sys

import time
import jsonlines
import json
import re
import time
from functools import partial

from openai import OpenAI

# API Settings

# 访问 https://platform.openai.com/assistants, and create an new assistant, 
# Set name="Math Tutor", 
# instructions="You are a personal math tutor. Write and run code to answer math questions.", 
# set code interpreter on and model = "gpt-4-1106-preview"
# copy and paste the assistant id in  variable assistant_id
# # Or you can execute the following code in this fileW:
# assistant = client.beta.assistants.create(
#     name="Math Tutor",
#     instructions="You are a personal math tutor. Write and run code to answer math questions.",
#     tools=[{"type": "code_interpreter"}],
#     model="gpt-4-1106-preview"
# )

OPENAI_API_KEY = "sk-xx"
client = OpenAI(api_key=OPENAI_API_KEY, timeout=180)
assistant_id = 'xx'


# Prompt
base_prompt = "Please solve the problem step by step and verify your answer using code, and put your final answer in\\boxed{}. The problem is:"



pattern = r'\\boxed\{(.*?(?:\{.*?\}.*?)*?)\}'
def get_answer(contents):
    for content in contents[::-1]:
        match = re.findall(pattern, content, re.DOTALL)
        if len(match) != 0:
            break
    return match


def call_gpt4_api(line):
    """
    run api

        Parameters
        ----------
        line: dict
        like {"queId": "559135fce0cc43d09bcdb784b6b68b16", "difficulty": "1", "problem": "", "knowledge_point_routes": }
    reference:
    https://platform.openai.com/docs/assistants/overview
    """
    problem = line['problem']

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=base_prompt + problem
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        timeout=180,
    )

    while run.status != 'completed':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run.status in ["cancelled", "failed", "expired"]:
            thread = client.beta.threads.delete(thread_id=thread.id)
            print(run)
            time.sleep(1)
            return {'queId': line['queId'], 'difficulty': line['difficulty'], 'response': run.status}

    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id
    )
    for run_step in run_steps:
        if run_step.step_details.type == 'tool_calls':
            for tool_call in run_step.step_details.tool_calls:
                print(tool_call.code_interpreter.input)
                for output in tool_call.code_interpreter.outputs:
                    print(output.logs)
    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        order='asc'
    )
    responses = []
    for final_message in messages:
        value = final_message.content[0].text.value
        print(value)
        responses.append(value)
    match = get_answer(responses)
    if len(match) == 0:
        match = [""]

    thread = client.beta.threads.delete(thread_id=thread.id)
    time.sleep(1)

    return {'queId': line['queId'], 'difficulty': line['difficulty'], 'response': match[-1]}


def process_prompt(result_path: str, line: dict):
    """
    run api and print text to result file

        Parameters
        ----------
        result_path : str
        line: dict

    """
    queid = line['queId']
    stdout_backup = sys.stdout  # Backup the current stdout
    with open(f'{result_path}/{queid}.txt', 'w', encoding='UTF-8') as f:
        sys.stdout = f  # redirect stdout to file
        try:
            result = call_gpt4_api(line)
            print(json.dumps(result))  # Printing results will be written to a file.
        except Exception as exc:
            sys.stdout = stdout_backup
            print(f'{queid} generated an exception: {exc}')
            time.sleep(60)
        else:
            sys.stdout = stdout_backup  # recover stdout
            print(json.dumps(result))
    time.sleep(1)


def main():

    absolute_path = ''
    result_pth = './results'
    file_name = './dataset/TAL-SAQ6K-EN.jsonl'

    lines = []
    with open(absolute_path + file_name, "r", encoding='utf-8') as f:
        for line in jsonlines.Reader(f):
            lines.append(line)
    
    partial_func = partial(process_prompt, result_pth)
    for line in lines:
        partial_func(line)


if __name__ == '__main__':

    main()
