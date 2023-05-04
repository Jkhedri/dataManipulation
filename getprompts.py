import json

def get_dict_list():
    with open('main_run_data_jkhedri.json', "r") as f:
        dict_list = json.load(f)
    return dict_list

def get_prompts():
    dict_list = get_dict_list()
    prompts = []
    for i in range(len(dict_list)):
        if type(dict_list[i]) == list:
            print(dict_list[i])
        prompts.append(dict_list[i].get('prompt'))
    return prompts  

if __name__ == "__main__":
    prompts = get_prompts()
    with open('prompts.json', 'w') as f:
        f.write('[\n')
        for prompt in prompts:
            f.write("{\n" + "   \"prompt\": \"" + prompt + "\"\n},\n")
        f.write(']')