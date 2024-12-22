import sys
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.agents import initialize_agent

from commands import chrome_click_on_link, chrome_get_the_links_on_the_page, chrome_open_url, chrome_read_the_page, computer_applescript_action, say_text, hello_world, open_main_py, bring_vs_code_to_foreground

# Load environment variables
load_dotenv()

def main(command):
    llm = OpenAI(temperature=0)  # Ensure API key is set in .env or passed directly

    tools = [
        computer_applescript_action,
        chrome_open_url,
        chrome_get_the_links_on_the_page,
        chrome_click_on_link,
        chrome_read_the_page, 
        hello_world, 
        open_main_py,
        bring_vs_code_to_foreground

    ]

    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

    result = agent.run(command)

    if result:
        say_text(f'The result is {result}')
    else:
        say_text(f'Finished doing {command}')

if __name__ == "__main__":
    command = sys.argv[1]
    if not command:
        print("Please provide a command to execute e.g. python main.py 'Open the calculator app'")
        exit(1)

    main(command)
