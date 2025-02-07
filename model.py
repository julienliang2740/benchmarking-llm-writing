import os
from dotenv import load_dotenv
import getpass

from pydantic import BaseModel
from openai import OpenAI

from logger import setup_logger

load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

# Setup logging
logger = setup_logger("model_input_output")
def do_logging(func, prompt, output):
    logger.info("\n"*6)

    logger.info(func.__name__)
    logger.info("="*90)
    logger.info("PROMPT" + "="*84)
    logger.info("="*90)

    logger.info(prompt)
    
    logger.info("="*90)
    logger.info("OUTPUT" + "="*84)
    logger.info("="*90)

    logger.info(output)

    logger.info("\n"*6)



class Metric(BaseModel):
    metric: str
    description: str

class Grading_Metrics(BaseModel):
    metrics: list[Metric]

class Metric_Grade(BaseModel):
    metric: str
    metric_grade: int

class All_Grades(BaseModel):
    grades: list[Metric_Grade]
    
client = OpenAI()

def run_gpt_structured_output(system_prompt, user_prompt, response_format_class, model="gpt-4o-mini", temperature= 0.0) -> str:
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format=response_format_class,
        temperature=temperature
    )
    return_value = completion.choices[0].message.parsed
    
    do_logging(run_gpt_structured_output, f"******SYSTEM PROMPT******\n{system_prompt}\n\n\n******USER PROMPT******\n{user_prompt}\n\n\n", return_value)
    return return_value





if __name__ == '__main__':
    system_prompt = "You are a metric creating agent for a given type of essay. Come up with a list of metrics to grade an essay based off, give the metric and then a brief description of what you're looking for"
    user_prompt = "History Essay"
    response_format_class = Grading_Metrics

    monkebruga = run_gpt_structured_output(system_prompt, user_prompt, response_format_class)
    monke = monkebruga.model_dump()

    print(type(monke))
    print(monke)
    print("\n\n\n\n")

    for thing in monke:
        print(type(thing))
        print(thing)
        break