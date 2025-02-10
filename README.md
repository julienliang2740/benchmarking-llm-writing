# benchmarking-llm-writing
A tool to compare different text outputs for a task meant especially for benchmarking LLM writing capabilities.

## Usage
Clone repo and make the necessary directories
```
git clone https://github.com/julienliang2740/benchmarking-llm-writing
cd benchmarking-llm-writing
mkdir documents
```

Create a .env file and put your openai api key in there.
Put the writing outputs (must be in PDF format) in the documents folder.

In main.py, change the configurations as desired:
```
# number of times to evaluate each task output
number_of_runs = 1
# model to use for evaluation
model = "gpt-4o-mini"
# csv file with the task names and task output file paths
task_outputs_csv_file = "task_outputs.csv"
# csv file with the grades for the task outputs of each task
grades_csv_file = "grades.csv"
```

In the csv file you designate as task_outputs_csv_file, fill it out as:
```
task,method1,method2,method3,files
original task prompt,./documents/path/to/method1/output.pdf,./documents/path/to/method2/output.pdf,./documents/path/to/method3/output.pdf,["./rubric/files/for/task.pdf", "./another/rubric/files/for/task.pdf"]
...
```
- The first column "task" is a string representation of the prompt for the task
- The middle columns are the different output versions for the same task to be graded. Strings representing the file paths to the task output go in there. The column titles and number of columns can vary as needed.
- The last row "files" is a string representation that is converted in the code to a list of strings, each string representing a file path to files that are referenced when judging the task outputs. If no such files exist, just leave it as "[]"

To get a grades csv file just run main.py:
```
python main.py
```

The results should appear in a file with the same name as grades_csv_file.
