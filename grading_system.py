from model import *



# create a list of metrics
def create_grading_metrics(original_prompt, list_of_files, user_input):
    with open("metric_creation_prompt.txt", "r", encoding="utf-8") as file:
        file_content = file.read()