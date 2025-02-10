from grading_system import GradingSystem, load_pages
import csv
import ast
import os


from pypdf import PdfReader

# note: task outputs must be pdf documents

# number of times to evaluate each task output
number_of_runs = 1
# model to use for evaluation
model = "gpt-4o-mini"
# csv file with the task names and task output file paths
task_outputs_csv_file = "task_outputs.csv"
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

def judge_task(original_prompt: str, file_paths: list[str], task_outputs: dict[str,str], model: str) -> dict[str, list[int]]:
    judge = GradingSystem(original_prompt, file_paths, model)
    
    results = {}
    for sample_type, output in task_outputs.items():
        grades = judge.grade_output_distribution(output, number_of_runs)
        avg_grade = sum(grades) / number_of_runs
        results[sample_type] = avg_grade

    return results

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
                
                # Call judge_task to obtain results (assumed to be a dict)
                results = judge_task(task_prompt, reference_file_paths, task_outputs, model)
                print(f"{task_prompt}:\n{results}")
                
                # Add the task name to the results so it gets written into the grades CSV
                results["task"] = task_prompt
                
                # Write the results as a new row in the grades CSV file
                writer.writerow(results)
    
    print(f"Grading written to {grades_csv_file}")




if __name__ == '__main__':
    run(task_outputs_csv_file, grades_csv_file)
