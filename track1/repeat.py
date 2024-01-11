import jsonlines
import json

def find_duplicate_values_in_dict(input_dict):
    """
    Find keys in the dictionary whose values are duplicated.

    :param input_dict: Dictionary to check for duplicate values
    :return: A dictionary where keys are the duplicate values and values are lists of keys that share that value
    """
    value_to_keys = {}
    for key, value in input_dict.items():
        value_to_keys.setdefault(value, []).append(key)

    return {value: keys for value, keys in value_to_keys.items() if len(keys) > 1}

def most_frequent_element(lst):
    """
    Find the element that appears most frequently in the list.
    """
    if not lst:  # Check if the list is empty
        return None

    frequency = {}  # Dictionary to keep track of element frequencies
    max_count = -1  # Variable to store the maximum frequency count
    most_frequent = None  # Variable to store the most frequent element

    for element in lst:
        # Increment the frequency of the element in the dictionary
        frequency[element] = frequency.get(element, 0) + 1

        # Update the most frequent element if necessary
        if frequency[element] > max_count:
            max_count = frequency[element]
            most_frequent = element

    return most_frequent, max_count

if __name__ == '__main__':
    
    result_dict = {}
    with open('TAL_SAQ6K_CN_prediction.json', "r", encoding='utf-8') as f:
        result_dict = json.load(f)

    CN_dict = {}
    file_jsonl_path = './dataset/TAL-SAQ7K-CN.jsonl'
    with open(file_jsonl_path, "r", encoding='utf-8') as f:
        for line in jsonlines.Reader(f):
            CN_dict[line['queId']] = line['problem']

    duplicated_dict = find_duplicate_values_in_dict(CN_dict)

    for key, values in duplicated_dict.items():
        duplicate_len = len(values)
        ans_set = []
        for item in values:
            ans_set.append(result_dict[item])
        most_frequent, max_count = most_frequent_element(ans_set)
        
        if max_count>1:
            if most_frequent!='':
                for item in values:
                    result_dict[item] = most_frequent

    with open('TAL_SAQ7K_CN_prediction.json', "w", encoding='utf-8') as wf:
        json_record = json.dumps(result_dict, ensure_ascii=False)
        wf.write(json_record + '\n')





