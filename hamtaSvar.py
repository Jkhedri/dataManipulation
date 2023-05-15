import json

def extract_answers(input_file, output_file, num_labels):
    with open(input_file, 'r') as f:
        data = json.load(f)

    extracted_labels = []
    for item in data[:num_labels]:
        extracted_labels.append(item['g_answer'])

    extracted_data = {'labels': extracted_labels}

    with open(output_file, 'w') as f:
        json.dump(extracted_data, f, indent=4)

# Example usage
input_file = 'main_run_data_jkhedri.json'
output_file = 'chatgptbra.json'
num_labels = 900

extract_answers(input_file, output_file, num_labels)