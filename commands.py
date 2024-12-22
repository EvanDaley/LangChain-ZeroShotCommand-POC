import subprocess

from langchain.agents import tool
  
# TODO set preferred editor...
@tool(parse_docstring=True)
def open_vs_code_file_by_name_search(input):
    """
    Executing this will do a name search in VS Code on the given input.
    Nothing extra needs to be done. 
    This requires no validation.
    Don't do anything extra after this step.
    """
    # Escape the file name to handle special characters
    file_name_safe = input.replace('"', '\\"')  # Escape double quotes

    # Dynamically include the escaped file name
    script = f'''
    tell application "System Events"
        tell process "Code"
            delay 0.5
            key code 35 using {{command down}} -- Press Command+P
            delay 0.1
            keystroke "{file_name_safe}" -- Type the file name
            delay 0.1
            key code 36 -- Press Enter key
        end tell
    end tell
    '''

    run_applescript(script)
    
    return 'file name search completed'
 
@tool(parse_docstring=True)
def select_lines_in_vs_code(input):
    """
    Selects lines in Visual Studio Code based on the given input.
    The input should be a string in the format "start_line:end_line".
    This requires no additional validation or processing.
    """
    # Parse the input into start and end lines
    try:
        start_line, end_line = map(int, input.split(":"))
    except ValueError:
        return "Invalid input format. Please use 'start_line:end_line'."
    
    # Calculate the number of lines to select.
    lines_to_select = (end_line - start_line)

    # AppleScript to select lines in VS Code
    script = f'''
    tell application "Visual Studio Code"
        activate
    end tell

    delay 0.5

    tell application "System Events"
        tell process "Code"
            -- Open the 'Go to Line' dialog (Control+G in VS Code)
            keystroke "g" using {{control down}}
            delay 0.1

            -- Type the starting line number
            keystroke ({start_line} as string)
            delay 0.2
            keystroke return
            delay 0.2

            -- Expand the selection downwards by the number of lines
            repeat {lines_to_select} times
                key code 125 using {{shift down}} -- Down Arrow with Shift
                delay 0.05
            end repeat
        end tell
    end tell
    '''

    # Pass the arguments to the script
    run_applescript(script)

    return 'lines have been selected'


@tool(parse_docstring=True)
def bring_vs_code_to_foreground(input):
    """
    Bring VS Code to the foreground
    """
    script = f'''
    tell application "Visual Studio Code"
        activate
    end tell
    '''

    run_applescript(script)
    
    return 'vs code is now in the foreground'


@tool(parse_docstring=True)
def chrome_get_the_links_on_the_page(input):
    """
    Use this when you want to get the links on the current page.

    You should use this before clicking on anything
    """
    return run_javascript('Array.from(document.querySelectorAll("a")).map(x => x.innerText + ": " + x.href).join(" - ")')[:4000]

@tool(parse_docstring=True)
def chrome_click_on_link(link):
    """
    Use this when you want to go to a link. 
    
    The link should be a url from a previous observation
    """
    return run_javascript(f'window.location.href = "{link}"')[:4000]

@tool(parse_docstring=True)
def chrome_read_the_page(input):
    """
    Use this when you want to read the page.
    """

    return run_javascript('document.body.innerText')[:4000]

@tool(parse_docstring=True)
def chrome_open_url(url):
    """
    Use this tool to open a URL in Chrome. It is recommended to use this tool before doing any other actions on Chrome.
    
    The URL should be a string. For example: https://gmail.com
    """
    script = f'''
    tell application "Google Chrome"
        open location "{url}"
    end tell
    '''

    return run_applescript(script)

@tool(parse_docstring=True)
def hello_world(text):
    """
    Log hello world to the console
    """
    print('hello world')
    
def run_javascript(javascript):
    javascript = javascript.replace('"', '\\"')

    if javascript.startswith('open '):
        return "Invalid command, not javascript"

    script = f'''
    tell application "Google Chrome"
        tell active tab of front window
            execute javascript "{javascript}"
        end tell
    end tell
    '''
    
    return run_applescript(script)

def run_applescript(applescript):
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate(applescript.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    decoded_text = stdout.decode("utf-8")

    print('Step complete!')

    return decoded_text


def say_text(text):
    run_applescript(f'say "{text}"')
