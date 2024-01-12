import re
import os

# Regular expression pattern to find matches of the form '{"queId": ...'
pattern = r'\{"queId": (.*)\n'
def find_matches(filename):
    # Reads the file and finds all matches of the pattern
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()
        matches = re.findall(pattern, data)
    return matches

# Regular expression pattern for finding the 'queId' field in a line
ans_pattern = r'"queId":\s*"(.*?)"'
def find_answer(line):
    # Finds all matches for the 'queId' field in the line
    matches =  re.findall(ans_pattern, line)
    return matches[0]  # Returns the first match

# To fill up
absolute_path = './'

# Path to the results directory
result_path = absolute_path + 'results/API/'
# List all directories in the results path
result_files = os.listdir(result_path)
result_dict = {}

# Writing results to a text file
with open('result.txt', "w") as wf:
    # Iterating over each file in the current directory
    for result_file in result_files:
        file_name = result_path + result_file
        # Finding matches in the current file
        matches = find_matches(file_name)
        # Processing each match
        for match in matches:
            result = '{"queId": ' + match
            ID = find_answer(result)
            result_dict[ID] = result
    
    # Writing the contents of the result dictionary to the file
    for key in result_dict.keys():
        wf.write(result_dict[key] + '\n')
