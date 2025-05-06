from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import os

# Set OpenAI-compatible API to your local LM Studio instance
os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"  # LM Studio's default
os.environ["OPENAI_API_KEY"] = "not-needed"  # Dummy key, LM Studio ignores it

# Initialize the local LLM
llm = ChatOpenAI(
  model="deepseek coder v2-lite",  # You can give any name; LM Studio doesn't verify it
  temperature=0,
)

# Example toolset
@tool
def weather_tool(location: str):
  """
  Fetches weather information for a given location as input. Ex, "New York".
  """
  return f"Fetching weather for {location}."

@tool
def math_tool(expression: str):
  """
  Evaluates a mathematical expression which takes a mathematical expression as input. Ex, "2 + 2 * 3".
  """
  try:
    return eval(expression)
  except Exception as e:
    return f"Error: {e}"

@tool
def greeting_tool(name: str):
  """
  Generates a greeting message which takes a person name as input. Ex, "Alice".
  """
  return f"Hello, {name}!"


# Tool registry
TOOLS = {
  "weather_tool": weather_tool,
  "math_tool": math_tool,
  "greeting_tool": greeting_tool
}

# Invoke the LLM with tools
def invoke_llm_with_tools(user_query):
  print(f'user_query: {user_query}')

  messages = [HumanMessage(user_query)]

  llm_with_tools = llm.bind_tools(TOOLS.values())
  ai_message = llm_with_tools.invoke(messages)

  print(f'tool_calls: {ai_message.tool_calls}')

  messages.append(ai_message)

  for tool_call in ai_message.tool_calls:
    selected_tool = TOOLS[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

  ai_response = llm_with_tools.invoke(messages)

  return ai_response.content.strip()

# AI agent runner
def run_agent(user_query):
  ai_response_using_tools = invoke_llm_with_tools(user_query)
  print(f"\nAnswer: {ai_response_using_tools}")

# Test it
# run_agent("What’s the weather in Delhi?")
# run_agent("Say hi to Saikumar")
run_agent("What is 3 + 5 * 7 ?")
