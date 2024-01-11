import re
import jsonlines
import json
from latex2sympy2 import latex2sympy

# Regular expression pattern for finding the 'response' field in a line
ans_pattern = r'"response":\s*"(.*?)"'
def find_answer(line):
    # Finds all matches for the 'response' field in the line
    matches =  re.findall(ans_pattern, line)
    return matches[0]  # Returns the first match

# Regular expression pattern for finding the 'queId' field in a line
ID_pattern = r'"queId":\s*"(.*?)"'
def find_ID(line):
    # Finds all matches for the 'queId' field in the line
    matches =  re.findall(ID_pattern, line)
    return matches[0]  # Returns the first match

def latex2float(line):
    # Converts LaTeX formatted fractions to float
    fraction_str = find_answer(line)
    match = re.search(r'\\frac{(\d+)}{(\d+)}', fraction_str)
    fraction_str = fraction_str.replace("\\\\", "\\")
    if match:
        expr = latex2sympy(fraction_str)
        print(fraction_str, '\t', format(expr.evalf(), '.2f'))
        return expr.evalf()  # Returns the evaluated expression
    else:
        return None   

absolute_path = ''

# Path to the JSONL file containing the dataset
CN_jsonl = './dataset/TAL-SAQ6K-EN.jsonl'
CN_lines = []
# Reading the JSONL file
with open(absolute_path + CN_jsonl, "r", encoding='utf-8') as f:
    for line in jsonlines.Reader(f):
        CN_lines.append(line)

result_dict = {}
# Reading a text file and storing the results in a dictionary
with open('result.txt', "r") as f:
    lines = f.readlines()
    for line in lines:
        answer = find_answer(line)
        if answer !='':
            ID = find_ID(line)
            result_dict[ID] = line

mid_dict = {}
# Writing the processed data to a JSON file
with open('TAL_SAQ6K_EN_prediction.json', "w", encoding='utf-8') as wf:
    for line in CN_lines:
        ID = line['queId']
        if ID in result_dict:
            ans = find_answer(result_dict[ID])
            match = re.search(r'\\frac{(\d+)}{(\d+)}', ans)
            if match:
                ans = ans.replace("\\\\", "\\")
                print(ID, '\t', ans)
                expr = latex2sympy(ans)
                ans = str(expr.evalf())
                print(expr, '\t', format(expr.evalf(), '.2f'))
            
            match = re.search(r'\\%', str(ans))
            if match:
                expr = latex2sympy(ans)
                ans = expr.evalf()
                print(expr, '\t', format(expr.evalf(), '.2f'))
            mid_dict[ID] = str(ans)
        else:
            mid_dict[ID] = "0"

    json_record = json.dumps(mid_dict, ensure_ascii=False)
    wf.write(json_record + '\n')
