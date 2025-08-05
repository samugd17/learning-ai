from openai import OpenAI
from dotenv import load_dotenv
from colorama import Fore, Style, init
import os

init(autoreset=True)

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

TASK_DESCRIPTION = 'Create a web application to book tables at a restaurant.'


def generate_initial_plan(task: str) -> str:
    prompt = f"""
    Task: {task}

    Break down this task into a detailed step-by-step plan to accomplish it. Be specific.
    """
    response = client.chat.completions.create(
        model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': prompt}]
    )

    initial_plan = response.choices[0].message.content
    return initial_plan


def reflect_on_plan(plan: str, task: str) -> str:
    reflection_prompt = f"""
    The following plan was created for the task: "{task}"

    Current plan:
    {plan}

    Reflect critically: Does this plan correctly cover all necessary steps? Are there any missing details or unnecessary steps? Improve the plan if needed.
    """
    response = client.chat.completions.create(
        model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': reflection_prompt}]
    )

    reflection_plan = response.choices[0].message.content
    return reflection_plan


def reflection_loop(task: str, iterations: int = 3) -> None:
    current_plan = generate_initial_plan(task)

    for i in range(iterations):
        print(Fore.BLUE + Style.BRIGHT + f'\n--- Iteration {i + 1} ---')
        print(f'Current plan:\n{current_plan}')

        reflection = reflect_on_plan(current_plan, task)
        print(Fore.GREEN + Style.BRIGHT + f'\nReflection and improvement:\n{reflection}')

        current_plan = reflection


if __name__ == '__main__':
    reflection_loop(TASK_DESCRIPTION)
