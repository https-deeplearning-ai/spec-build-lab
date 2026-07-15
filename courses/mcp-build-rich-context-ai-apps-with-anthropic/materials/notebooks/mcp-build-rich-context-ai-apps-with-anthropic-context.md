# MCP: Build Rich-Context AI Apps with Anthropic

---

## Lesson Map

- L3/L3.ipynb → Lesson 6: Creating an MCP Client
- L4/L4.ipynb → Lesson 7: Connecting the MCP Chatbot to Reference Servers
- L5/L5.ipynb → Lesson 8: Adding Prompt and Resource Features
- L6/L6.ipynb → Lesson 10: Creating and Deploying Remote Servers

---

## Lesson 6: Creating an MCP Client — L3/L3.ipynb

[markdown] cell 0

# Lesson 3: Chatbot Example

[markdown] cell 1

In this lesson, you will familiarize yourself with the chatbot example you will work on during this course. The example includes the tool definitions and execution, as well as the chatbot code. Make sure to interact with the chatbot at the end of this notebook.

[markdown] cell 2

## Import Libraries

[code] cell 3

import arxiv
import json
import os
from typing import List
from dotenv import load_dotenv
import anthropic

[markdown] cell 4

## Tool Functions

[code] cell 5

PAPER_DIR = "papers"

[markdown] cell 6

The first tool searches for relevant arXiv papers based on a topic and stores the papers' info in a JSON file (title, authors, summary, paper url and the publication date). The JSON files are organized by topics in the `papers` directory. The tool does not download the papers.  

[code] cell 7

def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Search for papers on arXiv based on a topic and store their information.
    
    Args:
        topic: The topic to search for
        max_results: Maximum number of results to retrieve (default: 5)
        
    Returns:
        List of paper IDs found in the search
    """
    
    # Use arxiv to find the papers 
    client = arxiv.Client()

    # Search for the most relevant articles matching the queried topic
    search = arxiv.Search(
        query = topic,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.Relevance
    )

    papers = client.results(search)
    
    # Create directory for this topic
    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    
    file_path = os.path.join(path, "papers_info.json")

    # Try to load existing papers info
    try:
        with open(file_path, "r") as json_file:
            papers_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}

    # Process each paper and add to papers_info  
    paper_ids = []
    for paper in papers:
        paper_ids.append(paper.get_short_id())
        paper_info = {
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'summary': paper.summary,
            'pdf_url': paper.pdf_url,
            'published': str(paper.published.date())
        }
        papers_info[paper.get_short_id()] = paper_info
    
    # Save updated papers_info to json file
    with open(file_path, "w") as json_file:
        json.dump(papers_info, json_file, indent=2)
    
    print(f"Results are saved in: {file_path}")
    
    return paper_ids

[code] cell 8

search_papers("computers")

[markdown] cell 9

The second tool looks for information about a specific paper across all topic directories inside the `papers` directory.

[code] cell 10

def extract_info(paper_id: str) -> str:
    """
    Search for information about a specific paper across all topic directories.
    
    Args:
        paper_id: The ID of the paper to look for
        
    Returns:
        JSON string with paper information if found, error message if not found
    """
 
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {file_path}: {str(e)}")
                    continue
    
    return f"There's no saved information related to paper {paper_id}."

[code] cell 11

extract_info('1312.3300v1')

[markdown] cell 12

## Tool Schema

[markdown] cell 13

Here are the schema of each tool which you will provide to the LLM.

[code] cell 14

tools = [
    {
        "name": "search_papers",
        "description": "Search for papers on arXiv based on a topic and store their information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to search for"
                }, 
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to retrieve",
                    "default": 5
                }
            },
            "required": ["topic"]
        }
    },
    {
        "name": "extract_info",
        "description": "Search for information about a specific paper across all topic directories.",
        "input_schema": {
            "type": "object",
            "properties": {
                "paper_id": {
                    "type": "string",
                    "description": "The ID of the paper to look for"
                }
            },
            "required": ["paper_id"]
        }
    }
]

[markdown] cell 15

## Tool Mapping

[markdown] cell 16

This code handles tool mapping and execution.

[code] cell 17

mapping_tool_function = {
    "search_papers": search_papers,
    "extract_info": extract_info
}

def execute_tool(tool_name, tool_args):
    
    result = mapping_tool_function[tool_name](**tool_args)

    if result is None:
        result = "The operation completed but didn't return any results."
        
    elif isinstance(result, list):
        result = ', '.join(result)
        
    elif isinstance(result, dict):
        # Convert dictionaries to formatted JSON strings
        result = json.dumps(result, indent=2)
    
    else:
        # For any other type, convert using str()
        result = str(result)
    return result

[markdown] cell 18

## Chatbot Code

[markdown] cell 19

The chatbot handles the user's queries one by one, but it does not persist memory across the queries.

[code] cell 20

load_dotenv() 
client = anthropic.Anthropic()

[markdown] cell 21

### Query Processing

[markdown] cell 22

> **⚠️ Deprecation Notice**
> The model `claude-3-7-sonnet-20250219` was deprecated in February 2026 and is no longer supported. All code in this notebook has been updated to use `claude-sonnet-4-6` to ensure everything runs as expected.

[code] cell 23

def process_query(query):
    
    messages = [{'role': 'user', 'content': query}]
    
    response = client.messages.create(max_tokens = 2024,
                                  #model = 'claude-3-7-sonnet-20250219', #deprecated model
                                  model = 'claude-sonnet-4-6', 
                                  tools = tools,
                                  messages = messages)
    
    process_query = True
    while process_query:
        assistant_content = []

        for content in response.content:
            if content.type == 'text':
                
                print(content.text)
                assistant_content.append(content)
                
                if len(response.content) == 1:
                    process_query = False
            
            elif content.type == 'tool_use':
                
                assistant_content.append(content)
                messages.append({'role': 'assistant', 'content': assistant_content})
                
                tool_id = content.id
                tool_args = content.input
                tool_name = content.name
                print(f"Calling tool {tool_name} with args {tool_args}")
                
                result = execute_tool(tool_name, tool_args)
                messages.append({"role": "user", 
                                  "content": [
                                      {
                                          "type": "tool_result",
                                          "tool_use_id": tool_id,
                                          "content": result
                                      }
                                  ]
                                })
                response = client.messages.create(max_tokens = 2024,
                                  #model = 'claude-3-7-sonnet-20250219', #deprecated model
                                  model = 'claude-sonnet-4-6', 
                                  tools = tools,
                                  messages = messages) 
                
                if len(response.content) == 1 and response.content[0].type == "text":
                    print(response.content[0].text)
                    process_query = False

[markdown] cell 24

### Chat Loop

[code] cell 25

def chat_loop():
    print("Type your queries or 'quit' to exit.")
    while True:
        try:
            query = input("\nQuery: ").strip()
            if query.lower() == 'quit':
                break
    
            process_query(query)
            print("\n")
        except Exception as e:
            print(f"\nError: {str(e)}")

[markdown] cell 26

Feel free to interact with the chatbot. Here's an example query: 

- Search for 2 papers on "LLM interpretability"

To access the `papers` folder: 1) click on the `File` option on the top menu of the notebook and 2) click on `Open` and then 3) click on `L3`.

[code] cell 27

chat_loop()

[markdown] cell 28

<p style="background-color:#f7fff8; padding:15px; border-width:3px; border-color:#e0f0e0; border-style:solid; border-radius:6px"> 🚨
&nbsp; <b>Different Run Results:</b> The output generated by AI chat models can vary with each execution due to their dynamic, probabilistic nature. Don't be surprised if your results differ from those shown in the video.</p>

[markdown] cell 29

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b> To Access the <code>requirements.txt</code> file or the <code>papers</code> folder: </b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em> and finally 3) click on <em>"L3"</em>.
</div>

[markdown] cell 30

In the next lessons, you will take out the tool definitions to wrap them in an MCP server. Then you will create an MCP client inside the chatbot to make the chatbot MCP compatible.  

[markdown] cell 31

## Resources

[Guide on how to implement tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview#how-to-implement-tool-use)

[markdown] cell 32

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">


<p> ⬇ &nbsp; <b>Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>

</div>

---

## Lesson 7: Connecting the MCP Chatbot to Reference Servers — L4/L4.ipynb

[markdown] cell 0

# Lesson 4: Creating an MCP Server

[markdown] cell 1

In this lesson, you will wrap the tools of the chatbot of the previous lesson, to build an MCP server that exposes 2 tools. You will use here the `stdio` transport and run the server in the provided local environment. You will learn more about remote servers in another lesson.

[markdown] cell 2

## How can you create an MCP Server? - *Additional Note*

[markdown] cell 3

Let's take the example of a server that exposes tools. This server needs to handle two main requests from the client:
- listing all the tools
  
   <img src="images/server_list_tools.png" width="400">

- executing a particular tool
  
  <img src="images/server_call_tool.png" width="400">

[markdown] cell 4

There are two ways for creating an MCP server:
- **low-level implementation**: in this approach, you directly define and handle the various types of requests (`ListToolsRequest` and `CallToolRequest`). This approach allows you to customize every aspect of your server.
- **high-level implementation using `FastMCP`**: `FastMCP` is a high-level interface that makes building MCP servers faster and simpler. In this approach, you just focus on defining the tools as functions, and`FastMCP` handles all the protocol details.
  
You will use in this lesson `FastMCP`. If you'd like to learn more about the low-level approach, you can check out the resources at the end of this notebook.

[markdown] cell 5

## Building your MCP Server using `FastMCP`

[markdown] cell 6

You will build the files needed for your MCP server in the folder `mcp_project`. You will incrementally add or update more files to this project folder in the upcoming lessons. The `mcp_project` folder is provided to you. You will first create the python file of the server `research_server.py` and save it in  `mcp_project` folder, then you'll prepare the environment to run the server.

[markdown] cell 7

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b> To Access the  <code>mcp_project</code> folder :</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em> and finally 3) click on <em>L4</em>.
</div>

[markdown] cell 8

To create your MCP server using `FastMCP`, you will initialize a `FastMCP` server labeled as `mcp` and decorating the functions with `@mcp.tool()`. `FastMCP` automatically generates the necessary MCP schema based on type hints and docstrings.


**Note**: The magic function `%%writefile mcp_project/research_server.py` will not execute the code but it will save the content of the cell to the server file `research_server.py` in the directory: `mcp_project`. If you remove the magic function and run the cell, the code won't run in Jupyter notebook. You will run the server from the terminal in the next section. 

[code] cell 9

%%writefile mcp_project/research_server.py

import arxiv
import json
import os
from typing import List
from mcp.server.fastmcp import FastMCP


PAPER_DIR = "papers"

# Initialize FastMCP server
mcp = FastMCP("research")

@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Search for papers on arXiv based on a topic and store their information.
    
    Args:
        topic: The topic to search for
        max_results: Maximum number of results to retrieve (default: 5)
        
    Returns:
        List of paper IDs found in the search
    """
    
    # Use arxiv to find the papers 
    client = arxiv.Client()

    # Search for the most relevant articles matching the queried topic
    search = arxiv.Search(
        query = topic,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.Relevance
    )

    papers = client.results(search)
    
    # Create directory for this topic
    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    
    file_path = os.path.join(path, "papers_info.json")

    # Try to load existing papers info
    try:
        with open(file_path, "r") as json_file:
            papers_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}

    # Process each paper and add to papers_info  
    paper_ids = []
    for paper in papers:
        paper_ids.append(paper.get_short_id())
        paper_info = {
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'summary': paper.summary,
            'pdf_url': paper.pdf_url,
            'published': str(paper.published.date())
        }
        papers_info[paper.get_short_id()] = paper_info
    
    # Save updated papers_info to json file
    with open(file_path, "w") as json_file:
        json.dump(papers_info, json_file, indent=2)
    
    print(f"Results are saved in: {file_path}")
    
    return paper_ids

@mcp.tool()
def extract_info(paper_id: str) -> str:
    """
    Search for information about a specific paper across all topic directories.
    
    Args:
        paper_id: The ID of the paper to look for
        
    Returns:
        JSON string with paper information if found, error message if not found
    """
 
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {file_path}: {str(e)}")
                    continue
    
    return f"There's no saved information related to paper {paper_id}."



if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

[markdown] cell 10

## Setting up your Environment & Testing your Server

[markdown] cell 11

You'll now set up the environment that you will use to run and test the server. For that, you will use the `uv` tool, which helps you manage your Python environment: it automatically sets up the project files and manages the package dependencies.

[markdown] cell 12

**Terminal Instructions**

[markdown] cell 13

- To open the terminal, run the cell below.
- Navigate to the project directory and initiate it with `uv`:
    - `cd L4/mcp_project`
    - `uv init`
-  Create virtual environment and activate it:
    - `uv venv`
    - `source .venv/bin/activate`
- Install dependencies:
    - `uv add mcp arxiv`
- Launch the inspector:
    - `npx @modelcontextprotocol/inspector uv run research_server.py`
- You will get a message saying that the inspector is up and running at a specific address. To open the inspector, click on that given address. The inspector will open in another tab.
- In the inspector UI, make sure to follow the video. You would need to specify under configuration the `Inspector Proxy Address`. Please check the "Inspector UI Instructions" below and run the last cell (after the terminal) to get the `Inspector Proxy Address` for your configurations. 
- If you tested the tool and would like to access the `papers` folder: 1) click on the `File` option on the top menu of the notebook and 2) click on `Open` and then 3) click on `L4` -> `mcp_project`.
- Once you're done with the inspector UI, make sure to close the inspector by typing `Ctrl+C` in the terminal below.

[code] cell 14

# start a new terminal
import os
from IPython.display import IFrame

IFrame(f"{os.environ.get('DLAI_LOCAL_URL').format(port=8888)}terminals/1", 
       width=1024, height=768)

[markdown] cell 15

### Inspector UI Instructions

[markdown] cell 16

In the inspector UI, make sure you have:

<img src="images/inspector2.png" height="500">

1.  `uv` under command
2.  `run research_server.py` under arguments
3.  Under configuration, you have to specify the "Inspector Proxy Address":
      - Run the following cell and copy the output address and paste it under "Inspector Proxy Address" in the inspector UI. **Note**: if you're running the inspector locally on your machine, you don't need to worry about this step.

[code] cell 17

# Print the inspector proxy address
print("Inspector Proxy Address that you need to specify under configuration in the inspector UI:")
print(os.environ.get('DLAI_LOCAL_URL').format(port=6277)[:-1])

[markdown] cell 18

## Resources

[markdown] cell 19

- [Example of low-level server](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/servers/simple-tool/mcp_simple_tool/server.py)
- [Advanced usage low-level server](https://github.com/modelcontextprotocol/python-sdk/blob/main/README.md#advanced-usage)
- [MCP inspector](https://github.com/modelcontextprotocol/inspector)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Quickstart for server developpers](https://modelcontextprotocol.io/quickstart/server)

[markdown] cell 20

### How to replicate the work locally?

- First make sure you have `uv` installed. You can check the installation methods [here](https://docs.astral.sh/uv/getting-started/installation/#pypi).
- Second you need to make sure you have `Node.js` installed on your machine. This is needed to run packages written in  `Typescript` (like the MCP inspector and maybe other MCP servers that you may download to use in your app). For instructions, check [here](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

After you have these two installed, then you can create the `mcp_project` folder and follow the same steps. If you're using a `Windows` machine, the only step you need to modify is how to activate your virtual environment. Instead of `source .venv/bin/activate`, you would need to type: `.venv\Scripts\activate` without `source`.

[markdown] cell 21

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b> To Access the  <code>mcp_project</code> folder :</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em>.
<p> ⬇ &nbsp; <b>To Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>

<p> 📒 &nbsp; For more help, please see the <em>"Appendix – Tips, Help, and Download"</em> Lesson.</p>

</div>

---

## Lesson 8: Adding Prompt and Resource Features — L5/L5.ipynb

[markdown] cell 0

# Lesson 5: Creating an MCP Client 

[markdown] cell 1

In the previous lesson, you created an MCP research server that exposes 2 tools. In this lesson, you will make the chatbot communicate to the server through an MCP client. This will make the chatbot MCP compatible. You will continue from where you left off in lesson 4, i.e., you are provided again with the `mcp_project` folder that contains the `research_server.py` file. You'll add to it the MCP chatbot file and update the environment. 

[markdown] cell 2

<img src="images/lesson_progression.png" width="700">

[markdown] cell 3

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b> To Access the  <code>mcp_project</code> folder :</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em> and finally 3) click on <em>L5</em>.
</div>

[markdown] cell 4

## Back to the Chatbot Example

[markdown] cell 5

Here are the main code parts (`process_query`, `chat_loop`) from the chatbot example of lesson 3. Notice that the burden of tool definitions and execution is now shifted onto the MCP server, so the chatbot logic only contains code related to processing the user queries and to keeping the chat loop running until the user types `quit`.

[markdown] cell 6

> **⚠️ Deprecation Notice**
> The model `claude-3-7-sonnet-20250219` was deprecated in February 2026 and is no longer supported. All code in this notebook has been updated to use `claude-sonnet-4-6` to ensure everything runs as expected.

[code] cell 7

from dotenv import load_dotenv
import anthropic

load_dotenv()
anthropic = anthropic.Anthropic()

def process_query(query):
    messages = [{'role':'user', 'content':query}]
    response = anthropic.messages.create(max_tokens = 2024,
                                  #model = 'claude-3-7-sonnet-20250219', #deprecated model
                                  model = 'claude-sonnet-4-6',
                                  tools = tools,
                                  messages = messages)
    process_query = True
    while process_query:
        assistant_content = []
        for content in response.content:
            if content.type =='text':
                print(content.text)
                assistant_content.append(content)
                if(len(response.content)==1):
                    process_query= False
            elif content.type == 'tool_use':
                assistant_content.append(content)
                messages.append({'role':'assistant', 'content':assistant_content})
                tool_id = content.id
                tool_args = content.input
                tool_name = content.name

                print(f"Calling tool {tool_name} with args {tool_args}")
                
                # Call a tool
                result = execute_tool(tool_name, tool_args)
                messages.append({"role": "user", 
                                  "content": [
                                      {
                                          "type": "tool_result",
                                          "tool_use_id":tool_id,
                                          "content": result
                                      }
                                  ]
                                })
                response = anthropic.messages.create(max_tokens = 2024,
                                  #model = 'claude-3-7-sonnet-20250219', #deprecated model
                                  model = 'claude-sonnet-4-6', 
                                  tools = tools,
                                  messages = messages) 
                
                if(len(response.content)==1 and response.content[0].type == "text"):
                    print(response.content[0].text)
                    process_query= False


def chat_loop():
    print("Type your queries or 'quit' to exit.")
    while True:
        try:
            query = input("\nQuery: ").strip()
            if query.lower() == 'quit':
                break
    
            process_query(query)
            print("\n")
        except Exception as e:
            print(f"\nError: {str(e)}")

[markdown] cell 8

## Building your MCP Client

[markdown] cell 9

Now you will take the functions `process_query` and `chat_loop` and wrap them in a `MCP_ChatBot` class. To enable the chatbot to communicate to the server, you will add a method that connects to the server through an MCP client, which follows the structure given in this reference code:

[markdown] cell 10

### Reference Code
``` python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="uv",  # Executable
    args=["run example_server.py"],  # Command line arguments
    env=None,  # Optional environment variables
)

async def run():
    # Launch the server as a subprocess & returns the read and write streams
    # read: the stream that the client will use to read msgs from the server
    # write: the stream that client will use to write msgs to the server
    async with stdio_client(server_params) as (read, write): 
        # the client session is used to initiate the connection 
        # and send requests to server 
        async with ClientSession(read, write) as session:
            # Initialize the connection (1:1 connection with the server)
            await session.initialize()

            # List available tools
            tools = await session.list_tools()

            # will call the chat_loop here
            # ....
            
            # Call a tool: this will be in the process_query method
            result = await session.call_tool("tool-name", arguments={"arg1": "value"})


if __name__ == "__main__":
    asyncio.run(run())
`````

[markdown] cell 11

### Adding MCP Client to the Chatbot

[markdown] cell 12

The MCP_ChatBot class consists of the methods:
- `process_query`
- `chat_loop`
- `connect_to_server_and_run`
  
and has the following attributes:
- session (of type ClientSession)
- anthropic: Anthropic                           
- available_tools

In `connect_to_server_and_run`, the client launches the server and requests the list of tools that the server provides (through the client session). The tool definitions are stored in the variable `available_tools` and are passed in to the LLM in `process_query`.

<img src="images/tools_discovery.png" width="400">


In `process_query`, when the LLM decides it requires a tool to be executed, the client session sends to the server the tool call request. The returned response is passed in to the LLM. 

<img src="images/tool_invocation.png" width="400">

[markdown] cell 13

Here're the `mcp_chatbot` code.

[code] cell 14

%%writefile mcp_project/mcp_chatbot.py
from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List
import asyncio
import nest_asyncio

nest_asyncio.apply()

load_dotenv()

class MCP_ChatBot:

    def __init__(self):
        # Initialize session and client objects
        self.session: ClientSession = None
        self.anthropic = Anthropic()
        self.available_tools: List[dict] = []

    async def process_query(self, query):
        messages = [{'role':'user', 'content':query}]
        response = self.anthropic.messages.create(max_tokens = 2024,
                                      #model = 'claude-3-7-sonnet-20250219', #deprecated model
                                      model = 'claude-sonnet-4-6',
                                      tools = self.available_tools, # tools exposed to the LLM
                                      messages = messages)
        process_query = True
        while process_query:
            assistant_content = []
            for content in response.content:
                if content.type =='text':
                    print(content.text)
                    assistant_content.append(content)
                    if(len(response.content) == 1):
                        process_query= False
                elif content.type == 'tool_use':
                    assistant_content.append(content)
                    messages.append({'role':'assistant', 'content':assistant_content})
                    tool_id = content.id
                    tool_args = content.input
                    tool_name = content.name
    
                    print(f"Calling tool {tool_name} with args {tool_args}")
                    
                    # Call a tool
                    #result = execute_tool(tool_name, tool_args): not anymore needed
                    # tool invocation through the client session
                    result = await self.session.call_tool(tool_name, arguments=tool_args)
                    messages.append({"role": "user", 
                                      "content": [
                                          {
                                              "type": "tool_result",
                                              "tool_use_id":tool_id,
                                              "content": result.content
                                          }
                                      ]
                                    })
                    response = self.anthropic.messages.create(max_tokens = 2024,
                                      #model = 'claude-3-7-sonnet-20250219', #deprecated model
                                      model = 'claude-sonnet-4-6', 
                                      tools = self.available_tools,
                                      messages = messages) 
                    
                    if(len(response.content) == 1 and response.content[0].type == "text"):
                        print(response.content[0].text)
                        process_query= False

    
    
    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
        
                if query.lower() == 'quit':
                    break
                    
                await self.process_query(query)
                print("\n")
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def connect_to_server_and_run(self):
        # Create server parameters for stdio connection
        server_params = StdioServerParameters(
            command="uv",  # Executable
            args=["run", "research_server.py"],  # Optional command line arguments
            env=None,  # Optional environment variables
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session
                # Initialize the connection
                await session.initialize()
    
                # List available tools
                response = await session.list_tools()
                
                tools = response.tools
                print("\nConnected to server with tools:", [tool.name for tool in tools])
                
                self.available_tools = [{
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                } for tool in response.tools]
    
                await self.chat_loop()


async def main():
    chatbot = MCP_ChatBot()
    await chatbot.connect_to_server_and_run()
  

if __name__ == "__main__":
    asyncio.run(main())

[markdown] cell 15

## Running the MCP Chatbot

[markdown] cell 16

**Terminal Instructions**

[markdown] cell 17

- To open the terminal, run the cell below.
- Navigate to the `mcp_project` directory:
    - `cd L5/mcp_project`
- Activate the virtual environment:
    - `source .venv/bin/activate`
- Install the additional dependencies:
    - `uv add anthropic python-dotenv nest_asyncio`
- Run the chatbot:
    - `uv run mcp_chatbot.py`
- To exit the chatbot, type `quit`.
- If you run some queries and would like to access the `papers` folder: 1) click on the `File` option on the top menu of the notebook and 2) click on `Open` and then 3) click on `L5` -> `mcp_project`.

[code] cell 18

# start a new terminal
import os
from IPython.display import IFrame

IFrame(f"{os.environ.get('DLAI_LOCAL_URL').format(port=8888)}terminals/2", width=1024, height=768)

[markdown] cell 19

<p style="background-color:#f7fff8; padding:15px; border-width:3px; border-color:#e0f0e0; border-style:solid; border-radius:6px"> 🚨
&nbsp; <b>Different Run Results:</b> The output generated by AI chat models can vary with each execution due to their dynamic, probabilistic nature. Don't be surprised if your results differ from those shown in the video.</p>

[markdown] cell 20

## Resources

[markdown] cell 21

- [Quick Start for Client Developpers](https://modelcontextprotocol.io/quickstart/client)
- [Writing MCP client](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py)
- [Another mcp chatbot example](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py)

[markdown] cell 22

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b> To Access the  <code>mcp_project</code> folder :</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em> and then 3) on "L5".
<p> ⬇ &nbsp; <b>To Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>

<p> 📒 &nbsp; For more help, please see the <em>"Appendix – Tips, Help, and Download"</em> Lesson.</p>

</div>

[markdown] cell 23

(empty)

---

## Lesson 10: Creating and Deploying Remote Servers — L6/L6.ipynb

[markdown] cell 0

# Lesson 6: Connecting the MCP Chatbot to Reference Servers 

[markdown] cell 1

You'll now extend the MCP chatbot capabilities by making it connect to any MCP server. You will integrate the tools of two official MCP servers in addition to the tools of the research server you built in a previous lesson. 

[markdown] cell 2

<img src="images/lesson_6.png" width="400">

[markdown] cell 3

## Open-Source MCP Servers

[markdown] cell 4

In this [repo](https://github.com/modelcontextprotocol/servers), you can find a collection of reference implementations for the MCP servers, as well as references to community built servers and additional resources. You will use two of the reference servers to integrate their tools in your MCP chatbot:
- [fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch): provides the `fetch` tool which fetches a URL from the internet and extracts its contents as markdown.
- [filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem): provides several tools for interacting with the files and directories within a directory that you specify.

You can check the readme file of each server to check the features they expose and how to run them.  

[markdown] cell 5

## Updating the MCP Chatbot - Optional Reading

[markdown] cell 6

Here are the updates you'll make to the chatbot. You're encouraged to read this section before or after you watch the video, if you'd like to learn more about the details of the code.

- Instead of hardcoding the server parameters in the chatbot, the chatbot will read the server configurations from a JSON file:
  ### Server Configuration
  In the `L6/mcp_project`, you can find the `server_config.json` configuration file that has the following structure.
    ``` json
    {
        "mcpServers": {
            
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "."
                ]
            },
            
            "research": {
                "command": "uv",
                "args": ["run", "research_server.py"]
            },
            
            "fetch": {
                "command": "uvx",
                "args": ["mcp-server-fetch"]
            }
        }
    }
    ```
    For the reference servers, the commands `npx` and `uvx` directly install the files of the servers to your local environment (you don't need to install them ahead of time). Note for the `filesystem`, the `.` is provided as the third argument and it means "current directory". This means that you're allowing for the `fetch` server to interact with the files and directories that are within the current directory.

[markdown] cell 7

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b> To Access the  <code>mcp_project</code> folder :</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em> and finally 3) click on <em>L6</em>.
</div>

[markdown] cell 8

- Here's a rough sketch of the diagram of the updated MCP_chatbot:
  
  <img src="images/updated_class.png" width="600">

  1. Instead of having one session, you now have a list of client sessions where each client session establishes a 1-to-1 connection to each server;
  2. `available_tools` includes the definitions of all the tools exposed by all servers that the chatbot can connect to.
  3. `tool_to_session` maps the tool name to the corresponding client session; in this way, when the LLM decides on a particular tool name, you can map it to the correct client session so you can use that session to send `tool_call` request to the right MCP server.
  4. `exit_stack` is a context manager that will manage the mcp client objects and their sessions and ensures that they are properly closed. In lesson 5, you did not use it because you used the `with` statement which behind the scenes uses a context manager. Here you could again use the `with` statement, but you may end up using multiple nested `with` statements since you have multiple servers to connect to. `exit_stack` allows you to dynamically add the mcp clients and their sessions as you'll see in the code below.
  5. `connect_to_servers` reads the server configuration file and for each single server, it calls the helper method `connect_to_server`. In this latter method, an MCP client is created and used to launch the server as a sub-process and then a client session is created to connect to the server and get a description of the list of the tools provided by the server.
  6. `cleanup` is a helper method that ensures all your connections are properly shut down when you're done with them. In lesson 5, you relied on the `with` statement to automatically clean up resources. This cleanup method serves a similar purpose, but for all the resources you've added to your exit_stack; it closes (your MCP clients and sessions) in the reverse order they were added - like stacking and unstacking plates. This is particularly important in network programming to avoid resource leaks.

[markdown] cell 9

## Updated Code for the MCP Chatbot

[markdown] cell 10

> **⚠️ Deprecation Notice**
> The model `claude-3-7-sonnet-20250219` was deprecated in February 2026 and is no longer supported. All code in this notebook has been updated to use `claude-sonnet-4-6` to ensure everything runs as expected.

[code] cell 11

%%writefile mcp_project/mcp_chatbot.py

from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List, Dict, TypedDict
from contextlib import AsyncExitStack
import json
import asyncio

load_dotenv()

class ToolDefinition(TypedDict):
    name: str
    description: str
    input_schema: dict

class MCP_ChatBot:

    def __init__(self):
        # Initialize session and client objects
        self.sessions: List[ClientSession] = [] # new
        self.exit_stack = AsyncExitStack() # new
        self.anthropic = Anthropic()
        self.available_tools: List[ToolDefinition] = [] # new
        self.tool_to_session: Dict[str, ClientSession] = {} # new


    async def connect_to_server(self, server_name: str, server_config: dict) -> None:
        """Connect to a single MCP server."""
        try:
            server_params = StdioServerParameters(**server_config)
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            ) # new
            read, write = stdio_transport
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            ) # new
            await session.initialize()
            self.sessions.append(session)
            
            # List available tools for this session
            response = await session.list_tools()
            tools = response.tools
            print(f"\nConnected to {server_name} with tools:", [t.name for t in tools])
            
            for tool in tools: # new
                self.tool_to_session[tool.name] = session
                self.available_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                })
        except Exception as e:
            print(f"Failed to connect to {server_name}: {e}")

    async def connect_to_servers(self): # new
        """Connect to all configured MCP servers."""
        try:
            with open("server_config.json", "r") as file:
                data = json.load(file)
            
            servers = data.get("mcpServers", {})
            
            for server_name, server_config in servers.items():
                await self.connect_to_server(server_name, server_config)
        except Exception as e:
            print(f"Error loading server configuration: {e}")
            raise
    
    async def process_query(self, query):
        messages = [{'role':'user', 'content':query}]
        response = self.anthropic.messages.create(max_tokens = 2024,
                                      #model = 'claude-3-7-sonnet-20250219', #deprecated model
                                      model = 'claude-sonnet-4-6',
                                      tools = self.available_tools,
                                      messages = messages)
        process_query = True
        while process_query:
            assistant_content = []
            for content in response.content:
                if content.type =='text':
                    print(content.text)
                    assistant_content.append(content)
                    if(len(response.content) == 1):
                        process_query= False
                elif content.type == 'tool_use':
                    assistant_content.append(content)
                    messages.append({'role':'assistant', 'content':assistant_content})
                    tool_id = content.id
                    tool_args = content.input
                    tool_name = content.name
                    
    
                    print(f"Calling tool {tool_name} with args {tool_args}")
                    
                    # Call a tool
                    session = self.tool_to_session[tool_name] # new
                    result = await session.call_tool(tool_name, arguments=tool_args)
                    messages.append({"role": "user", 
                                      "content": [
                                          {
                                              "type": "tool_result",
                                              "tool_use_id":tool_id,
                                              "content": result.content
                                          }
                                      ]
                                    })
                    response = self.anthropic.messages.create(max_tokens = 2024,
                                      #model = 'claude-3-7-sonnet-20250219', #deprecated model
                                      model = 'claude-sonnet-4-6', 
                                      tools = self.available_tools,
                                      messages = messages) 
                    
                    if(len(response.content) == 1 and response.content[0].type == "text"):
                        print(response.content[0].text)
                        process_query= False

    
    
    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
        
                if query.lower() == 'quit':
                    break
                    
                await self.process_query(query)
                print("\n")
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self): # new
        """Cleanly close all resources using AsyncExitStack."""
        await self.exit_stack.aclose()


async def main():
    chatbot = MCP_ChatBot()
    try:
        # the mcp clients and sessions are not initialized using "with"
        # like in the previous lesson
        # so the cleanup should be manually handled
        await chatbot.connect_to_servers() # new! 
        await chatbot.chat_loop()
    finally:
        await chatbot.cleanup() #new! 


if __name__ == "__main__":
    asyncio.run(main())

[markdown] cell 12

## Running the MCP Chatbot

[markdown] cell 13

**Terminal Instructions**

[markdown] cell 14

- To open the terminal, run the cell below.
- Navigate to the `mcp_project` directory:
    - `cd L6/mcp_project`
- Activate the virtual environment:
    - `source .venv/bin/activate`
- Run the chatbot:
    - `uv run mcp_chatbot.py`
- To exit the chatbot, type `quit`.
- If you run some queries and would like to access the `papers` folder or any output files: 1) click on the `File` option on the top menu of the notebook and 2) click on `Open` and then 3) click on `L6` -> `mcp_project`.

[code] cell 15

# start a new terminal
import os
from IPython.display import IFrame

IFrame(f"{os.environ.get('DLAI_LOCAL_URL').format(port=8888)}terminals/3", width=1024, height=768)

[markdown] cell 16

Make sure to interact with the chatbot. Here are some query examples:
- Fetch the content of this website: https://modelcontextprotocol.io/docs/concepts/architecture and save the content in the file "mcp_summary.md", create a visual diagram that summarizes the content of "mcp_summary.md" and save it in a text file
- Fetch deeplearning.ai and find an interesting term. Search for 2 papers around the term and then summarize your findings and write them to a file called results.txt

[markdown] cell 17

<p style="background-color:#f7fff8; padding:15px; border-width:3px; border-color:#e0f0e0; border-style:solid; border-radius:6px"> 🚨
&nbsp; <b>Different Run Results:</b> The output generated by AI chat models can vary with each execution due to their dynamic, probabilistic nature. Don't be surprised if your results differ from those shown in the video.</p>

[markdown] cell 18

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> ⬇ &nbsp; <b>To Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>

<p> 📒 &nbsp; For more help, please see the <em>"Appendix – Tips, Help, and Download"</em> Lesson.</p>

</div>

[markdown] cell 19

## Final Notes

[markdown] cell 20

You are encouraged to refactor the code of `MCP_ChatBot` if you'd like:

- how to connect to servers asynchronously
- what if tools from different servers have the same name
- revisit the attributes
  
And maybe any other idea you may think of.

[markdown] cell 21

(empty)

---

## L7/L7.ipynb

[markdown] cell 0

# Lesson 7: Adding Prompt & Resource Features

[markdown] cell 1

In the previous lessons, you created an MCP server that provides only tools. In this lesson, you are provided with an updated file for the research server file which now provides a prompt template and 2 resources features in addition to the 2 tools. You are also provided with an updated file for the mcp chatbot file where the MCP client exposes the prompt and resources for the user to use. The files are provided in the `mcp_project` folder.

[markdown] cell 2

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b> To Access the  <code>mcp_project</code> folder :</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em> and finally 3) click on <em>L7</em>.
</div>

[markdown] cell 3

## Defining Resources and Prompts in the MCP Server - Optional Reading

[markdown] cell 4

Feel to read this section before or after you watch the video. You can always skip and go to the end of the notebook to run the updated chatbot. 

[markdown] cell 5

**Resources**

[markdown] cell 6

You learned from lesson 3 that the research server saves the information of the researched papers in a `json` file called `papers_info.json`, which is stored under a folder labeled with the topic name. All the topics are stored under the `papers` directory. If you check the `papers` folder provided to you under `mcp_project`, you will find two folders labeled `ai_interpretability` and `llm_reasoning`, and in each folder, you have `papers_info.json` file. 

Resources are read-only data that an MCP server can expose to the LLM application. Resources are similar to GET endpoints in a REST API - they provide data but shouldn't perform significant computation or have side effects. For example, the resource can be a list of folders within a directory or the content of a file within a folder. Here, the MCP server provides two resources:
- list of available topic folders under the papers directory;
- the papers' information stored under a topic folder.

Here's a code snippet that shows how resources are defined in the MCP server again using `FastMCP` (with the use of the decorator `@mcp.resource(uri)`). You can find the complete code in the `mcp_project` folder. The URI defined inside `@mcp.resource()` is used to uniquely identify the resource and, as a server developer, you can customize the URI. But in general, it follows this scheme:
`sth://xyz/xcv` . In this example, two types of URI were used:
- static URI: `papers://folders` (which represents the list of available topics)
- dynamic URI: `papers://{topic}` (which represents the papers' information under the topic specified by the client during runtime)

[markdown] cell 7

``` python
@mcp.resource("papers://folders")
def get_available_folders() -> str:
    """
    List all available topic folders in the papers directory.
    
    This resource provides a simple list of all available topic folders.
    """
    folders = []
    
    # Get all topic directories
    if os.path.exists(PAPER_DIR):
        for topic_dir in os.listdir(PAPER_DIR):
            topic_path = os.path.join(PAPER_DIR, topic_dir)
            if os.path.isdir(topic_path):
                papers_file = os.path.join(topic_path, "papers_info.json")
                if os.path.exists(papers_file):
                    folders.append(topic_dir)
    
    # Create a simple markdown list
    content = "# Available Topics\n\n"
    if folders:
        for folder in folders:
            content += f"- {folder}\n"
        content += f"\nUse @{folder} to access papers in that topic.\n"
    else:
        content += "No topics found.\n"
    
    return content

@mcp.resource("papers://{topic}")
def get_topic_papers(topic: str) -> str:
    """
    Get detailed information about papers on a specific topic.
    
    Args:
        topic: The research topic to retrieve papers for
    """
    topic_dir = topic.lower().replace(" ", "_")
    papers_file = os.path.join(PAPER_DIR, topic_dir, "papers_info.json")
    
    if not os.path.exists(papers_file):
        return f"# No papers found for topic: {topic}\n\nTry searching for papers on this topic first."
    
    try:
        with open(papers_file, 'r') as f:
            papers_data = json.load(f)
        
        # Create markdown content with paper details
        content = f"# Papers on {topic.replace('_', ' ').title()}\n\n"
        content += f"Total papers: {len(papers_data)}\n\n"
        
        for paper_id, paper_info in papers_data.items():
            content += f"## {paper_info['title']}\n"
            content += f"- **Paper ID**: {paper_id}\n"
            content += f"- **Authors**: {', '.join(paper_info['authors'])}\n"
            content += f"- **Published**: {paper_info['published']}\n"
            content += f"- **PDF URL**: [{paper_info['pdf_url']}]({paper_info['pdf_url']})\n\n"
            content += f"### Summary\n{paper_info['summary'][:500]}...\n\n"
            content += "---\n\n"
        
        return content
    except json.JSONDecodeError:
        return f"# Error reading papers data for {topic}\n\nThe papers data file is corrupted."
```

[markdown] cell 8

**Prompt Template**

[markdown] cell 9

Server can also provide a prompt template. You can define this feature in the MCP server using the decorator `@mcp.prompt()` as shown in the code snippet below. MCP will use `generate_search_prompt` as the prompt name, infer the prompt arguments from the function's argument and the prompt's description from the doc string.

[markdown] cell 10

```python
@mcp.prompt()
def generate_search_prompt(topic: str, num_papers: int = 5) -> str:
    """Generate a prompt for Claude to find and discuss academic papers on a specific topic."""
    return f"""Search for {num_papers} academic papers about '{topic}' using the search_papers tool. Follow these instructions:
    1. First, search for papers using search_papers(topic='{topic}', max_results={num_papers})
    2. For each paper found, extract and organize the following information:
       - Paper title
       - Authors
       - Publication date
       - Brief summary of the key findings
       - Main contributions or innovations
       - Methodologies used
       - Relevance to the topic '{topic}'
    
    3. Provide a comprehensive summary that includes:
       - Overview of the current state of research in '{topic}'
       - Common themes and trends across the papers
       - Key research gaps or areas for future investigation
       - Most impactful or influential papers in this area
    
    4. Organize your findings in a clear, structured format with headings and bullet points for easy readability.
    
    Please present both detailed information about each paper and a high-level synthesis of the research landscape in {topic}."""
```

[markdown] cell 11

## Using Resources and Prompts in the MCP Chatbot - Optional Reading

[markdown] cell 12

The chatbot is updated to enable users to interact with the prompt using the slash command:
- Users can use the command `/prompts` to list the available prompts
- Users can use the command `/prompt <name> <arg1=value1>` to invoke a particular prompt
  
The chatbot also enables users to interact with the resources using the `@` character:
- Users can use the command `@folders` to see available topics
- Users can use the command `@topic` to get papers info under that topic

[markdown] cell 13

Make sure to check the updated code in the `mcp_project` folder. There's a couple of newly added methods (`get_resource`, `execute_prompt`, `list_prompts`). Here's a brief summary of the updates added to the chatbot:

[markdown] cell 14

- In `connect_to_server`: the client requests from the server to list the resources and prompt templates they provide (in addition to the tools request). The resource URIs and the prompt names are stored in the MCP chatbot.
   
    <img src="images/resource_discovery.png" width="400">


    <img src="images/prompt_discovery.png" width="400">


[markdown] cell 15

- In `chat_loop`: the user's input is checked to see if the user has used any of the slash commands or @ options.

- If the user types: `@folders` or `@topic` then the newly added method `get_resource` is called where the request is sent to the server.
   
    <img src="images/resource_invocation.png" width="400">

[markdown] cell 16

- If the user types: `/prompts`, then the newly added method `list_prompts` is called.
   
- If the user types: `/prompt <name> <arg1=value1>`, then the newly added method `execute_prompt` is called where the request is sent to the server:
   
   <img src="images/prompt_invocation.png" width="400">
   
   and the prompt is passed to the LLM. 
- Otherwise the query is processed by the LLM.

[markdown] cell 17

## Running the MCP Chatbot

[markdown] cell 18

**Terminal Instructions**

[markdown] cell 19

- To open the terminal, run the cell below.
- Open the terminal below.
- Navigate to the `mcp_project` directory:
    - `cd L7/mcp_project`
- Activate the virtual environment:
    - `source .venv/bin/activate`
- Run the chatbot:
    - `uv run mcp_chatbot.py`ot.py`
- To exit the chatbot, type `quit`.
- If you run some queries and would like to access the `papers` folder or any output files: 1) click on the `File` option on the top menu of the notebook and 2) click on `Open` and then 3) click on `L7` -> `mcp_project`.

[code] cell 20

# start a new terminal
import os
from IPython.display import IFrame

IFrame(f"{os.environ.get('DLAI_LOCAL_URL').format(port=8888)}terminals/4", width=1024, height=768)

[markdown] cell 21

Make sure to interact with the chatbot. Here are some query examples:
- **@folders**
- **@ai_interpretability**
- **/prompts**
- **/prompt prompt_research_paper topic=history num_papers=2**

[markdown] cell 22

<p style="background-color:#f7fff8; padding:15px; border-width:3px; border-color:#e0f0e0; border-style:solid; border-radius:6px"> 🚨
&nbsp; <b>Different Run Results:</b> The output generated by AI chat models can vary with each execution due to their dynamic, probabilistic nature. Don't be surprised if your results differ from those shown in the video.</p>

[markdown] cell 23

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> ⬇ &nbsp; <b>To Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>

<p> 📒 &nbsp; For more help, please see the <em>"Appendix – Tips, Help, and Download"</em> Lesson.</p>

</div>

---

## L9/L9.ipynb

[markdown] cell 0

# Lesson 9: Creating and Deploying Remote Servers 

[markdown] cell 1

In the previous lessons, you worked with servers running locally using `stdio` transport. In this lesson, you will learn how to create a remote server using `FastMCP`, test it using MCP inspector and then learn how to deploy it on `render.com`.

You will focus on the `sse` transport. When the course was filmed, the python `sdk` for `Streamable HTTP` was in active development. However, this lesson will still give you insights into what a remote server is. We included notes for how the server implementation would be different with `Streamable HTTP` (slight changes since `FastMCP` provides you with a high-level interface).

[markdown] cell 2

## Creating an SSE Remote Server

[markdown] cell 3

With `FastMCP`, it's also easy to create an SSE remote server. You just need to specify that the transport is `sse` when running the server. You can also specify the port number when initializing the FastMCP server. The remaining tool, prompt and resource definitions are all the same. So the following code for the MCP server is the same code you saw in Lesson 7. The transport is specified at the end, and the port number of `8001` is specified in the `FastMCP` constructor (you may also decide to choose the default port as well). 

[code] cell 4

%%writefile mcp_project/research_server.py
import arxiv
import json
import os
from typing import List
from mcp.server.fastmcp import FastMCP

PAPER_DIR = "papers"

# Initialize FastMCP server
mcp = FastMCP("research", port=8001)

@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Search for papers on arXiv based on a topic and store their information.
    
    Args:
        topic: The topic to search for
        max_results: Maximum number of results to retrieve (default: 5)
        
    Returns:
        List of paper IDs found in the search
    """
    
    # Use arxiv to find the papers 
    client = arxiv.Client()

    # Search for the most relevant articles matching the queried topic
    search = arxiv.Search(
        query = topic,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.Relevance
    )

    papers = client.results(search)
    
    # Create directory for this topic
    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    
    file_path = os.path.join(path, "papers_info.json")

    # Try to load existing papers info
    try:
        with open(file_path, "r") as json_file:
            papers_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}

    # Process each paper and add to papers_info  
    paper_ids = []
    for paper in papers:
        paper_ids.append(paper.get_short_id())
        paper_info = {
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'summary': paper.summary,
            'pdf_url': paper.pdf_url,
            'published': str(paper.published.date())
        }
        papers_info[paper.get_short_id()] = paper_info
    
    # Save updated papers_info to json file
    with open(file_path, "w") as json_file:
        json.dump(papers_info, json_file, indent=2)
    
    print(f"Results are saved in: {file_path}")
    
    return paper_ids

@mcp.tool()
def extract_info(paper_id: str) -> str:
    """
    Search for information about a specific paper across all topic directories.
    
    Args:
        paper_id: The ID of the paper to look for
        
    Returns:
        JSON string with paper information if found, error message if not found
    """
 
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {file_path}: {str(e)}")
                    continue
    
    return f"There's no saved information related to paper {paper_id}."



@mcp.resource("papers://folders")
def get_available_folders() -> str:
    """
    List all available topic folders in the papers directory.
    
    This resource provides a simple list of all available topic folders.
    """
    folders = []
    
    # Get all topic directories
    if os.path.exists(PAPER_DIR):
        for topic_dir in os.listdir(PAPER_DIR):
            topic_path = os.path.join(PAPER_DIR, topic_dir)
            if os.path.isdir(topic_path):
                papers_file = os.path.join(topic_path, "papers_info.json")
                if os.path.exists(papers_file):
                    folders.append(topic_dir)
    
    # Create a simple markdown list
    content = "# Available Topics\n\n"
    if folders:
        for folder in folders:
            content += f"- {folder}\n"
        content += f"\nUse @{folder} to access papers in that topic.\n"
    else:
        content += "No topics found.\n"
    
    return content

@mcp.resource("papers://{topic}")
def get_topic_papers(topic: str) -> str:
    """
    Get detailed information about papers on a specific topic.
    
    Args:
        topic: The research topic to retrieve papers for
    """
    topic_dir = topic.lower().replace(" ", "_")
    papers_file = os.path.join(PAPER_DIR, topic_dir, "papers_info.json")
    
    if not os.path.exists(papers_file):
        return f"# No papers found for topic: {topic}\n\nTry searching for papers on this topic first."
    
    try:
        with open(papers_file, 'r') as f:
            papers_data = json.load(f)
        
        # Create markdown content with paper details
        content = f"# Papers on {topic.replace('_', ' ').title()}\n\n"
        content += f"Total papers: {len(papers_data)}\n\n"
        
        for paper_id, paper_info in papers_data.items():
            content += f"## {paper_info['title']}\n"
            content += f"- **Paper ID**: {paper_id}\n"
            content += f"- **Authors**: {', '.join(paper_info['authors'])}\n"
            content += f"- **Published**: {paper_info['published']}\n"
            content += f"- **PDF URL**: [{paper_info['pdf_url']}]({paper_info['pdf_url']})\n\n"
            content += f"### Summary\n{paper_info['summary'][:500]}...\n\n"
            content += "---\n\n"
        
        return content
    except json.JSONDecodeError:
        return f"# Error reading papers data for {topic}\n\nThe papers data file is corrupted."

@mcp.prompt()
def generate_search_prompt(topic: str, num_papers: int = 5) -> str:
    """Generate a prompt for Claude to find and discuss academic papers on a specific topic."""
    return f"""Search for {num_papers} academic papers about '{topic}' using the search_papers tool. 

    Follow these instructions:
    1. First, search for papers using search_papers(topic='{topic}', max_results={num_papers})
    2. For each paper found, extract and organize the following information:
       - Paper title
       - Authors
       - Publication date
       - Brief summary of the key findings
       - Main contributions or innovations
       - Methodologies used
       - Relevance to the topic '{topic}'
    
    3. Provide a comprehensive summary that includes:
       - Overview of the current state of research in '{topic}'
       - Common themes and trends across the papers
       - Key research gaps or areas for future investigation
       - Most impactful or influential papers in this area
    
    4. Organize your findings in a clear, structured format with headings and bullet points for easy readability.
    
    Please present both detailed information about each paper and a high-level synthesis of the research landscape in {topic}."""

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')

[markdown] cell 5

**Streamable HTTP**: 
You can also use FastMCP to create a remote server using the transport "Streamable HTTP". The code would be again the same for tool, resource and prompt definitions. But when you run the server, you specify the transport as:

```python
mcp.run(transport="streamable-http")
```
 And when you initiate the FastMCP server you have two options:

```python
# Stateful server (maintains session state)
mcp = FastMCP("research")

# Stateless server (no session persistence)
mcp = FastMCP("research", stateless_http=True)
```

Stateless can be used when you want the server to handle simple, independent requests (no memory of previous interactions with the same client). Stateful can be used when you want the server to handle multiple requests that are part of a workflow and you want the server to remember the Client information and context across multiple requests.

[markdown] cell 6

## Testing the SSE Remote Server

[markdown] cell 7

After you create the python file for your remote server, you can test it using the MCP inspector or the simple chatbot of lesson 5, you can also integrate it with the chatbot of lesson 7. In order to test it, you first need to launch it to get its `URL` and then provide the `URL` to the chatbot or MCP inspector. 

**Note**: A server using the `stdio` transport is launched as a subprocess by the MCP client. On the other hand, a remote server is an independent processes running separately from the client and needs to be already running before the MCP client connects to it.

[markdown] cell 8


### How to run and test it on your local machine? - Optional Reading

[markdown] cell 9

You would need first to create and prepare a separate environment for the remote server. You can follow the same steps you learned about in the previous lessons:
- initiate the folder using `uv init`,
- create a virtual environment and activate it,
- add the required dependencies (`uv add arxiv mcp`).

You can then open a terminal and run your server using (`uv run research_server.py`), you'd need to keep the terminal open for the server to keep on running. You'll get a message in the terminal that the server is running at a given address. The `URL` that you would need to provide to the inspector or chatbot is that address with the appended `/sse` at the end. In a second terminal, you can launch the MCP inspector or your chatbot. Please check the comments below on how you can update the MCP chatbot. 

**Streamable HTPP**: same process for everything. For the `URL`, you would need to append `/mcp/` instead of `/sse`.

[markdown] cell 10

### Testing the server with MCP Inspector in this Lab

[markdown] cell 11

#### URL Link to the Remote server

[markdown] cell 12

In this lesson, you won't need to launch the remote server on your own. It's already provided to you; the remote server is already up and running in a separate container at port 8001. Run the next cell to get its URL. You'd need to use this URL to test the server in the MCP inspector. 

**Note**: If you'd like to learn how to run the MCP server in a docker container, please check the Appendix at the end of this course.

[code] cell 13

import os 
print("Remote server is running at:")
print(os.environ.get('DLAI_LOCAL_URL').format(port=8001)+"sse")

[markdown] cell 14

#### Testing the Provided Remote Server using MCP Inspector

[markdown] cell 15

**Terminal Instructions**

[markdown] cell 16

- To open the terminal, run the cell below.
  - The terminal might show the `work` directory or `L4/mcp_project`. You can stay in any directory, you don't need to navigate to `L9/mcp_project`. That's because you'll test a remote server that is already up and running, so you can launch the inspector from any directory.
  - If the terminal shows `L4/mcp_project` and you still have the inspector open from L4, you can close it by typing `CTRL+C` and then launch it again.
- To launch the inspector, type in the terminal: `npx @modelcontextprotocol/inspector`
- You will get a message saying that the inspector is up and running at a specific address. To open the inspector, click on that given address. The inspector will open in another tab.
- Please check the "Inspector UI Instructions" below.
- Once you're done with the inspector UI, make sure to close the inspector by typing `Ctrl+C` in the terminal below.

[markdown] cell 17

**Note**: The server is running in a different environment, and there are no topics saved under papers in the server's environment, so when you check the resources in the MCP inspector, you will get that there are no resources. 

[code] cell 18

# start a new terminal
from IPython.display import IFrame

IFrame(f"{os.environ.get('DLAI_LOCAL_URL').format(port=8888)}terminals/1", width=1024, height=768)

[markdown] cell 19

**Inspector UI Instructions**

[markdown] cell 20

In the inspector UI, make sure you have:

<img src="images/inspector2.png" height="500">

1.  `SSE` under `Transport Type`
2.  The URL of the remote server under `URL` (this is the link that ends with `sse`, the output of the cell you run before the terminal)
3.  Under configuration, you have to specify the "Inspector Proxy Address":
      - Run the following cell and copy the output address and paste it under "Inspector Proxy Address" in the inspector UI. Note: if you're running the inspector locally on your machine, you don't need to worry about this step.

[code] cell 21

# Print the inspector proxy address
print("Inspector Proxy Address that you need to specify under configuration in the inspector UI:")
print(os.environ.get('DLAI_LOCAL_URL').format(port=6277)[:-1])

[markdown] cell 22

#### Optional Note - How to Update the MCP chatbot so it can connect to a remote server?

[markdown] cell 23

You used `stdio_client` from the Python sdk to connect to the local server over `stdio`. The Python sdk provides another client `sse_client` that you can use to connect to a remote server over `sse`.  
First, you'd need to import `sse_client`:
```python
from mcp.client.sse import sse_client

```

Then in `connect_to_server`, you can use the same code, but instead of using `stdio_client`, you can use `sse_client` and pass to it the server url.

```python
sse_transport = await self.exit_stack.enter_async_context(
                   sse_client(url= "server_url/sse" )
                )
read, write = sse_transport 
```
The rest of the code should be the same.

**Stremable http client**

And if your remote server is running over `streamable http`, then you can similarly use the `streamablehttp_client`

``` python
from mcp.client.streamable_http import streamablehttp_client
streamable_transport = await self.exit_stack.enter_async_context(
                   streamablehttp_client(url= "server_url/mcp/" )
                )
read, write = streamable_transport 
```


[markdown] cell 24

## Optional - Deploying an SSE Server Using Render.com 

[markdown] cell 25

This part is optional and for you to explore on your local machine. If you'd like to try it, you can follow the instructions in the video. Make sure first to create an account at render [here](https://dashboard.render.com/login) using your Github account. 

[markdown] cell 26

## Resources

[markdown] cell 27

- Deploy Remote MCP servers on CloudFlare [link](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)
- Streamable HTTP transport [link](https://github.com/modelcontextprotocol/python-sdk/blob/main/README.md#streamable-http-transport)
- For low level server with Streamable HTTP implementations, see:
    - Stateful server: [examples](https://github.com/modelcontextprotocol/python-sdk/tree/main/examples/servers/simple-streamablehttp)
    - Stateless server: [examples](https://github.com/modelcontextprotocol/python-sdk/tree/main/examples/servers/simple-streamablehttp-stateless)
