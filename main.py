# from grading_system import GradingSystem
import csv



# number_of_runs = 3

# def judge_task(original_prompt: str, file_paths: list[str], task_outputs: dict[str,str]) -> dict[str, list[int], model: str]:
#     judge = GradingSystem(original_prompt, file_paths, model)
    
#     results = {}
#     for output_method, output in task_outputs:
#         grades = judge.grade_output_distribution(output, number_of_runs)
#         avg_grade = sum(grades) / number_of_runs
#         results[output_method] = avg_grade









if __name__ == '__main__':
    with open('task_outputs.csv', mode='r', newline='') as file:
        csv_dict_reader = csv.DictReader(file)
    
        for row in csv_dict_reader:
            print(row)
