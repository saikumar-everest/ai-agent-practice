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
  return f"Temperature at {location} is currently 20°C. It's little bit cloudy."

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
  return f"Hello, {name}!\nHow are you doing today?"


# Tool registry
TOOLS = {
  "weather_tool": weather_tool,
  "math_tool": math_tool,
  "greeting_tool": greeting_tool
}

# Invoke the LLM with tools
def invoke_llm_with_tools(user_query):
  print(f'user_query: {user_query}')

  prompt = f"""
  You are an AI Agent having accessible tools to address user queries.
  Available tools:
  - weather_tool: Fetches weather information for a given location.
  - math_tool: Evaluates a mathematical expression.
  - greeting_tool: Generates a greeting message.

  If the question is related to the tools, DO NOT modify the response. Just respond with whatever the tool returns.
  If the question is not related to the provided tools, answer it directly "I don't know".
  If there's no matching tool to respond, answer it directly "I don't know".

  User's question: {user_query}
  """

  human_message = HumanMessage(content=prompt)
  print(f'\n: {human_message}')

  messages = [human_message]

  llm_with_tools = llm.bind_tools(TOOLS.values())
  ai_message = llm_with_tools.invoke(messages)

  print(f'\n: {ai_message}')
  print(f'tool_calls: {ai_message.tool_calls}')

  if ai_message.tool_calls.__len__() == 0:
    print("No tool calls found.")
    return ai_message.content.strip()

  messages.append(ai_message)

  for tool_call in ai_message.tool_calls:
    selected_tool = TOOLS[tool_call["name"].lower()]
    tool_message = selected_tool.invoke(tool_call)
    print(f'\n: {tool_message}')
    messages.append(tool_message)

  ai_response = llm_with_tools.invoke(messages)
  print(f'\n: {ai_response}')

  return ai_response.content.strip()

# AI agent runner
def run_agent(user_query):
  ai_response_using_tools = invoke_llm_with_tools(user_query)
  print(f"\nAnswer: {ai_response_using_tools}")

# Test it
# run_agent("What’s the weather in Delhi?") # -> Success
# run_agent("Say hi to Saikumar") # -> Success
# run_agent("What is 3 + 5 * 7 ?") # -> Success
# run_agent("Are you a human?") # -> Failed. It didn't return "I don't know"
# run_agent("How do you like to greet my mother?") # -> Success
run_agent("What do you do in free time?") # -> Success
