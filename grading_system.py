from model import *

import asyncio
import os
from typing import List
from os.path import basename

async def read_files_concatenated(file_paths: List[str]) -> str:
    """
    Reads the contents of the provided files page by page and concatenates them into a single string.
    
    Args:
        file_paths (List[str]): List of file paths to read.

    Returns:
        str: Concatenated content of all files with page separation.
    """
    file_contents = "Below are the files for reference:\n"
    
    # Load all files asynchronously
    async with asyncio.TaskGroup() as tg:
        file_tasks = [tg.create_task(load_cached_pages(fp)) for fp in file_paths]
    
    # Process results
    for i, task in enumerate(file_tasks):
        pages = await task
        file_name = basename(file_paths[i])
        file_contents += f"*****File {i+1}: {file_name} (total pages: {len(pages)})*****\n"
        
        for idx, page in enumerate(pages, 1):
            file_contents += f"**page {idx}**\n{page.page_content}\n"
    
    return file_contents

# create a list of metrics
def create_grading_metrics(original_prompt, list_of_files):
    with open("metric_creation_prompt.txt", "r", encoding="utf-8") as file:
        metric_agent_prompt = file.read()
    files_content = read_files_concatenated(list_of_files)
    task_specific_prompt = (
        f"Original Task: \n{original_prompt}\n\n"
        f"Instructional Files for to Reference: \n{files_content}\n"
    )

    print("MONKE BRUGA")
    print(metric_agent_prompt)
    print("=========================================")
    print(task_specific_prompt)
    print("MONKE BRUGA")

    metrics = run_gpt(metric_agent_prompt, task_specific_prompt, Grading_Metrics)

    return metrics



if __name__ == '__main__':
    original_prompt = "write a report on the fall of the Ming Dynasty"
    metrics = create_grading_metrics(original_prompt, [])

    print(metrics)