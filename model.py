import os
from dotenv import load_dotenv
import getpass

from pydantic import BaseModel
from openai import OpenAI

load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

client = OpenAI()


# class Step(BaseModel):
#     explanation: str
#     output: str

# class MathReasoning(BaseModel):
#     steps: list[Step]
#     final_answer: str

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
    return return_value





if __name__ == '__main__':
    # system_prompt = "You are a answering bot, answer the user question"
    # user_prompt = "whats 9 plus ten"
    # response_format_class = Grading

    # monke = run_gpt_structured_output(system_prompt, user_prompt, response_format_class)

    # print(type(monke))
    # print(monke)

    # print(type(monke.grade))
    # print(monke.grade)




    system_prompt = "You are a metric creating agent for a given type of essay. Come up with a list of metrics to grade an essay based off, give the metric and then a brief description of what you're looking for"
    user_prompt = "History Essay"
    response_format_class = Grading_Metrics

    monke = run_gpt_structured_output(system_prompt, user_prompt, response_format_class)

    print(type(monke))
    print(monke)