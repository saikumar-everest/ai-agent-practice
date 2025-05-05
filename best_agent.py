from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os

# Set OpenAI-compatible API to your local LM Studio instance
os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"  # LM Studio's default
os.environ["OPENAI_API_KEY"] = "not-needed"  # Dummy key, LM Studio ignores it

# Initialize the local LLM
llm = ChatOpenAI(
    model="microsoft_-_phi-2",  # You can give any name; LM Studio doesn't verify it
    temperature=0,
)

# Example toolset
def weather_tool(location: str):
  """
  Fetches weather information for a given location.
  """
  return f"Fetching weather for {location}."

def math_tool(expression: str):
  """
  Evaluates a mathematical expression.
  """
  try:
    return eval(expression)
  except Exception as e:
    return f"Error: {e}"

def greeting_tool(name: str):
  """
  Generates a greeting message.
  """
  return f"Hello, {name}!"

# Tool registry
TOOLS = {
  "weather_tool": weather_tool,
  "math_tool": math_tool,
  "greeting_tool": greeting_tool
}

# LLM prompt builder
def choose_tool_with_llm(user_input):
  tool_descriptions = "\n".join([f"- {name}: {func.__doc__ or 'No description.'}" for name, func in TOOLS.items()])
  prompt = f"""
You are an AI agent. Based on the user's input, select the best tool.

Available tools:
{tool_descriptions}

User input: "{user_input}"
Respond with the name of the best tool to use.
IMPORTANT: Response should be a single line with the tool name only, no other text.
"""
  llm_with_tools = llm.bind_functions([weather_tool, math_tool, greeting_tool])
  response = llm_with_tools.invoke(prompt)
  return response.content.strip()

# Example runner
def run_agent(user_input):
  tool_name = choose_tool_with_llm(user_input)
  print(f"Selected tool or response: {tool_name}")
  # if tool_name in TOOLS:
  #   # Here, you’d normally parse and extract arguments for the tool
  #   # For simplicity, we'll hardcode or infer them
  #   if tool_name == "weather_tool":
  #     return TOOLS[tool_name]("New York")
  #   elif tool_name == "math_tool":
  #     return TOOLS[tool_name]("2 + 2 * 3")
  #   elif tool_name == "greeting_tool":
  #     return TOOLS[tool_name]("Alice")
  # else:
  #   return f"Tool '{tool_name}' not recognized."

# Test it
# print(run_agent("What’s the weather in NYC?"))
print(run_agent("Say hi to John"))
# print(run_agent("What is 10 + 20?"))
