from grading_system import JudgeAgent, load_pages
import csv
import ast
import os


from pypdf import PdfReader

# note: task outputs must be pdf documents

# number of times each Judge Agent evaluates each task output
number_of_runs = 1
# models to use for evaluation -> each model becomes a judge agent
models = ["gpt-4o-2024-08-06", "gpt-4o-mini-2024-07-18"]
# models = ["gpt-4o-mini"]

# csv file with the task names and task output file paths
task_outputs_csv_file = "monke.csv"
# csv file with the grades for the task outputs of each task
grades_csv_file = "grades.csv"

def return_text_from_pdf(filepath):
    # creating a pdf reader object
    reader = PdfReader(filepath)
    final_output = ""
    for page in reader.pages:
        text = page.extract_text()
        final_output = final_output + text + "\n"

    return final_output

# Builds the individual LLM Judge Agent (aka Councl Member) and returns its result
def judge_task(original_prompt: str, file_paths: list[str], task_outputs: dict[str,str], model: str) -> dict[str, list[int]]:
    judge = JudgeAgent(original_prompt, file_paths, model)
    
    results = {}
    for sample_type, output in task_outputs.items():
        grades = judge.grade_output_distribution(output, number_of_runs)
        avg_grade = sum(grades) / number_of_runs
        results[sample_type] = avg_grade

    return results

# Averages out the results of the judge_task(...) calls of the Judge Agents
# Input looks like: [{'sample1': 84.6, 'sample2': 77.5, 'sample3': 86.8}, ...]
def average_out_judges_verdicts(list_results: list[dict[str, list[int]]]) -> list[dict[str, list[int]]]:
    final_results = {}
    n = len(list_results)
    for result in list_results:
        for k,v in result.items():
            if k not in final_results.keys():
                final_results[k] = (v/n)
            else:
                final_results[k] += (v/n)

    return final_results

# Handles reading and preparing the files
# Builds all the LLM Judge Agents and runs the Council for judging
def run(task_outputs_csv_file, grades_csv_file):
    # Check if the grades CSV file already exists
    file_exists = os.path.exists(grades_csv_file)
    
    # Open the input CSV file for reading
    with open(task_outputs_csv_file, mode='r', newline='') as infile:
        csv_dict_reader = csv.DictReader(infile)
        
        # Build the header for the grades file:
        # Copy all field names from the input file except "files"
        out_fieldnames = [field for field in csv_dict_reader.fieldnames if field != "files"]
        
        # Open the grades CSV file in append mode if it exists, otherwise in write mode.
        mode_flag = 'a' if file_exists else 'w'
        with open(grades_csv_file, mode=mode_flag, newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=out_fieldnames)
            
            # Write the header if we're creating a new file
            if not file_exists:
                writer.writeheader()
            
            # Process each row in the input CSV
            for row in csv_dict_reader:
                task_prompt = row["task"]
                reference_file_paths = ast.literal_eval(row["files"])
                
                # Create a copy of the row for processing outputs
                task_outputs = row.copy()
                # Remove keys that are not part of the task outputs
                del task_outputs["task"]
                del task_outputs["files"]
                
                # For each output file, get the text content from the PDF
                for key, val in task_outputs.items():
                    text_content = return_text_from_pdf(val)
                    task_outputs[key] = text_content
                
                ##### MAKE THE LLM COUNCIL #####
                # Call judge_task to obtain results (assumed to be a dict)
                results = []
                for model in models:
                    result_per_judge = judge_task(task_prompt, reference_file_paths, task_outputs, model)
                    results.append(result_per_judge)
                    print(f"Results (judge - {model}):")
                    print(result_per_judge)

                final_results = average_out_judges_verdicts(results)
                print(f"{task_prompt}:\n{final_results}")
                
                # Add the task name to the results so it gets written into the grades CSV
                final_results["task"] = task_prompt
                
                # Write the results as a new row in the grades CSV file
                writer.writerow(final_results)
    
    print(f"Grading written to {grades_csv_file}")




if __name__ == '__main__':
    run(task_outputs_csv_file, grades_csv_file)
