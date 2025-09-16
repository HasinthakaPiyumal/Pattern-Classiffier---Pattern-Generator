import os

def load_code_from_file(file_path:str)->str:
    with open(file_path,"r") as file:
        code = file.read()
    return code

def get_all_python_files(repo_path):
    python_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"): 
                python_files.append(os.path.join(root, file))              
    return python_files

def get_folders(repo_path):
    directories = os.walk(repo_path)
    directories = [i[1] for i in directories][0]
    return directories