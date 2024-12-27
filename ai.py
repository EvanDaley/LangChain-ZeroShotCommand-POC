import sys
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.agents import initialize_agent
from langchain.prompts import PromptTemplate

from commands import chrome_click_on_link, chrome_get_the_links_on_the_page,chrome_open_url, chrome_read_the_page, say_text, hello_world, open_vs_code_file_by_name_search, bring_vs_code_to_foreground, select_lines_in_vs_code, switch_to_project

# Load environment variables
load_dotenv()

def ai(command):
    print("Running AI with input:")
    print(command)
    llm = OpenAI(temperature=0)  # Ensure API key is set in .env or passed directly

    tools = [
        chrome_open_url,
        chrome_get_the_links_on_the_page,
        chrome_click_on_link,
        chrome_read_the_page, 
        hello_world, 
        open_vs_code_file_by_name_search,
        select_lines_in_vs_code,
        switch_to_project
    ]
 #         bring_vs_code_to_foreground,

    custom_prompt = PromptTemplate(
        template="""
        You are a helpful assistant that can perform actions and answer user commands.
        When you've completed all necessary actions, summarize your final result with the phrase:
        'Task completed: {output}'.
        
        Always respond concisely and accurately.

        {input}
        """
    )

    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True, prompt=custom_prompt)

    # agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

    result = agent.run(command)

    # if result:
    #     say_text(f'The result is {result}')
    # else:
    #     say_text(f'Finished doing {command}')

if __name__ == "__main__":
    command = sys.argv[1]
    if not command:
        print("Please provide a command to execute e.g. python ai.py 'Open the calculator app'")
        exit(1)

    ai(command)
