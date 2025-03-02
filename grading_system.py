from model import *

import asyncio
import os
from typing import List
from os.path import basename

from langchain.document_loaders import PyPDFLoader

async def load_pages(loader):
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages

class JudgeAgent:
    def __init__(self, original_prompt, file_paths, model):
        self.original_prompt = original_prompt
        self.file_paths = file_paths
        self.model = model
        self.metrics_prompt_component = self.create_metrics_prompt_component()

    def read_files_concatenated(self) -> str:
        """
        Reads the contents of the provided files page by page and concatenates them into a single string.
        
        Args:
            self.file_paths (List[str]): List of file paths to read.

        Returns:
            str: Concatenated content of all files with page separation.
        """
        file_contents = "Below are the FULL files for reference:\n"
        for i, fp in enumerate(self.file_paths, 1):
            file_name = basename(fp)
            loader = PyPDFLoader(fp)
            pages = asyncio.run(load_pages(loader))
            file_contents += f"\n--- File {i}: {file_name} (Pages: {len(pages)}) ---\n"
            for idx, page in enumerate(pages, 1):
                file_contents += f"Page {idx}:\n{page.page_content}\n"

        return file_contents 

    # create a list of metrics
    def create_grading_metrics(self):
        with open("metric_creation_prompt.txt", "r", encoding="utf-8") as file:
            metric_agent_prompt = file.read()
        files_content = self.read_files_concatenated()
        task_specific_prompt = (
            f"Original Task: \n{self.original_prompt}\n\n"
            f"Instructional Files for to Reference: \n{files_content}\n"
        )

        metrics_raw = run_gpt_structured_output(metric_agent_prompt, task_specific_prompt, Grading_Metrics, self.model)
        metrics = (metrics_raw.model_dump())['metrics'] # this returns a list of dicts: [{'metric': '...', 'description': '...'}, ...]

        return metrics

    def create_metrics_prompt_component(self):
        metrics = self.create_grading_metrics()
        metrics_prompt = "Here are the metrics that you are to evaluate the task output based off of:\n"

        for metric in metrics:
            new_metric = f"{metric['metric']}: {metric['description']}\n"
            metrics_prompt += new_metric
        
        return metrics_prompt

    def grade_output(self, task_output: str) -> int:
        with open("judging_prompt.txt", "r", encoding="utf-8") as file:
            judging_agent_prompt = file.read()

        full_user_prompt = (
            f"This is the orignal task prompt: {self.original_prompt}\n"
            f"Below are the metrics you are to evaluate the task output based on:\n{self.metrics_prompt_component}\n"
            f"\n=================================================\n"
            f"This is the output for the task that you are to evaluate:\n{task_output}\n"
        )

        grades_raw = run_gpt_structured_output(judging_agent_prompt, full_user_prompt, All_Grades, self.model)
        grades = (grades_raw.model_dump())['grades']

        grades_sum = 0
        for metric in grades:
            grades_sum += metric['metric_grade']
        
        avg_grade = grades_sum / len(grades)
        return avg_grade
    
    def grade_output_distribution(self, task_output: str, sample_number: str) -> list[int]:
        list_of_grades = []
        for i in range(sample_number):
            grade = self.grade_output(task_output)
            list_of_grades.append(grade)
        return list_of_grades









if __name__ == '__main__':
    original_prompt = "write a report on the fall of the Ming Dynasty"

    mysys = JudgeAgent(original_prompt, [])