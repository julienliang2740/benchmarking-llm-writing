from grading_system import GradingSystem, load_pages
import csv
import ast

from pypdf import PdfReader



number_of_runs = 3
model = "gpt-4o-mini"
csv_file = "monke.csv"



def return_text_from_pdf(filepath):
    # creating a pdf reader object
    reader = PdfReader(filepath)
    final_output = ""
    for page in reader.pages:
        text = page.extract_text()
        final_output = final_output + text + "\n"

    return final_output

def judge_task(original_prompt: str, file_paths: list[str], task_outputs: dict[str,str], model: str) -> dict[str, list[int]]:
    judge = GradingSystem(original_prompt, file_paths, model)
    
    results = {}
    for sample_type, output in task_outputs.items():
        grades = judge.grade_output_distribution(output, number_of_runs)
        avg_grade = sum(grades) / number_of_runs
        results[sample_type] = avg_grade

    return results

def run():
    with open(csv_file, mode='r', newline='') as file:
        csv_dict_reader = csv.DictReader(file)
        for row in csv_dict_reader:
            task_prompt = row["task"]
            reference_file_paths = ast.literal_eval(row["files"])

            # get the task outputs from the file paths
            task_outputs = row
            del task_outputs['task']
            del task_outputs['files']
            for key,val in task_outputs.items():
                text_content = return_text_from_pdf(val)
                task_outputs[key] = text_content

            results = judge_task(task_prompt, reference_file_paths, task_outputs, model)
            
            print(results)



if __name__ == '__main__':
    run()
