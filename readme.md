### How to run any agent python script?

```python
python3 -m venv venv
source venv/bin/activate # To exit venv, run just "deactivate"
pip install -r requirements.txt

python3 <agent_python_script_file.py> # python3 simple_agent.py or npm run simple_agent
```

### LLM

Use [LM Studio](https://lmstudio.ai/) to run any model locally. I've used [Deepseek coder v2-lite](https://lmstudio.ai/model/deepseek-coder-v2-lite-instruct) model.

_Suggestion: Never use bad or low quality llms._

### Prerequisites

1. Install python
2. Install npm
3. Run LLM locally in LM Studio

### Available agents

#### simple_agent

It's an LLM agent that can cater user queries related to 3 different things.

1. weather info
2. mathematical expression evaluation
3. greet a person

If any user query comes that's not related to above available tools, then LLM is expected to respond with `I don't know`.

#### railway_agent

WIP
