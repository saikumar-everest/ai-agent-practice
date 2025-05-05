import os
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from browser_use import Agent, Browser, Controller
# Load environment variables
load_dotenv()
# Set OpenAI API key
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# Create controller
# controller = Controller()
# TODO: Define any custom actions for the controller if needed
async def railway_agent(user_query: str) -> Dict[str, Any]:
  """
  Railway agent that uses browser-use to check train availability
  Args:
  user_query: Natural language query about train availability
  Returns:
  Dictionary with structured train information
  """
  # TODO: Write system prompt with detailed instructions
  # TODO: Initialize LLM and create browser instance
  # Example:
  llm = ChatOpenAI(
    model_name="local-microsoft/phi-2", # This value doesn't matter for LMStudio
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="lmstudio", # Any value works
    max_tokens=4096,
    temperature=0.7,
  )
  browser = Browser()
  agent = Agent(
    task="Navigate to google.com and search for train availability to Delhi from Visakhapatnam",
    llm=llm,
    browser=browser
  )

  await agent.run()
  # TODO: Create and run the agent
  # TODO: Process the results into the required output format
  # This is just a placeholder - your implementation should replace this
  return {
    "source": "",
    "destination": "",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "class": "3A",
    "trains": []
  }

async def main():
  print("🚆 Welcome to the Talking Animals Zoo 🚆 ")
  print("I can help you introduce you to various talking animals.")
  print("Ask me questions like: 'Do you have a talking parrot?'")
  print("Type 'exit' to quit.")
  while True:
    user_query = input("\How can I help you today? (or 'exit' to quit): ")
    if user_query.lower() in ["exit", "quit", "bye"]:
      print("Thank you for your time. Enjoy! 👋 ")
      break
    print("\Analysing your request...")

    response = await railway_agent(user_query)
    print("\nResults:")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
  asyncio.run(main())