# 💫Benchmark
+ *Test:* Jokes
+ *Brain:* `cognitive_space.algorithms.embedding_model`, `cognitive_space.algorithms.embedding_model`
+ *Current Score:* 2/4 (Needs more stats)

## 🧠Brain Usage as Tool



```python
import os
from cognitive_space.brain import Brain
from cognitive_space.storage import AzureAISearchStorage
from cognitive_space.algorithms.embedding_model import EmbeddingEncode
from cognitive_space.algorithms.embedding_model import EmbeddingRecall
from cognitive_space.tool_builder.cognitive_encoder_tool import build_standard_encoder_tool
from cognitive_space.tool_builder.cognitive_recall_tool import build_standard_recall_tool

index_name = "benchmarks"
azure_ai_search_storage = AzureAISearchStorage(
    endpoint=os.getenv("AZURE_AI_SEARCH_BASE_URL"),
    api_key=os.getenv("AZURE_AI_SEARCH_API_KEY"),
    index_name=index_name)

azure_ai_search_storage.delete_index()
azure_ai_search_storage.create_or_update_index()

embedding_encode = EmbeddingEncode(
    storage_layer= azure_ai_search_storage,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY")
)

embedding_recall = EmbeddingRecall(
    storage_layer=azure_ai_search_storage,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY"),
)
brain_with_embeddings = Brain(
    cognitive_encoder=embedding_encode,
    cognitive_recall=embedding_recall)

encoder_tool = build_standard_encoder_tool(brain_with_embeddings)
recaller_tool = build_standard_recall_tool(brain_with_embeddings)
```

    
    
    

## 🤖Create Recall Space Agent


```python
import os
from agent_builder.builders.agent_builder import AgentBuilder
from textwrap import dedent
from langchain_openai import AzureChatOpenAI


llm = AzureChatOpenAI(
        base_url=os.getenv("AZURE_GPT4O_BASE_URL"),
        api_key=os.getenv("AZURE_GPT4O_KEY"),
        api_version=os.getenv("AZURE_GPT4O_API_VERSION"),
        streaming=False,
        temperature=0.5
    )
llm_name = "gpt-4o"

agent_builder = AgentBuilder()
agent_builder.set_goal(
    dedent(
    """
    You are an advanced AI assistant specifically designed to excel in
    memory and learning tasks. You can efficiently recall stored information
    to aid in decision-making and problem-solving. Additionally, you have
    the capability to capture and organize new information, allowing you
    to continuously build and update your knowledge base.

    Your context span is limited to a few tokens, so you will need to
    utilize cognitive tools to be perceived as intelligent. It is essential
    for you to always be aware of time. All timestamps presented to you will
    be in UTC. When using tools that require time awareness, please specify
    the time down to the second based on your UTC timestamp.
    """
    )
)
agent_builder.set_llm(llm)

agent_builder.add_tool(encoder_tool)
agent_builder.add_tool(recaller_tool)

test_agent = agent_builder.build()

agent_name = "gpt-4o-ai-brain-embeddings"
```

    WARNING:root:
    
    Initializing StateFulAgent
    --------------------------
    name: Agent
    tools: StructuredTool, StructuredTool
    model_name: None
    provider: AzureChatOpenAI
    
    

## 🤖Create Recall Space Agent


```python
import os
from recall_space_benchmarks.test_suite import TestSuite
from recall_space_benchmarks.utils.mongo_connector import MongoConnector
from recall_space_benchmarks.session.langchain_session import LangChainSession
from recall_space_benchmarks.test_suite.tests import Jokes

user_name = "Developer G"

# setup backend
mongo_connector = MongoConnector(
    db_name=os.getenv("MONGO_DB_NAME"),
    collection_name=os.getenv("MONGO_COLLECTION"),
    uri=os.getenv("MONGO_DB_CONNECTION_STRING"))

# create a session for the benchmark
session = LangChainSession(
    user_name=user_name, 
    agent_name=agent_name,
    agent=test_agent,
    db_handler=mongo_connector,
    session_name=f"Assesment Colors")

# Configure the benchmark
jokes = Jokes(total_questions=6,total_assessments=4)

llm_judge = llm = AzureChatOpenAI(
        base_url=os.getenv("AZURE_GPT4O_MINI_BASE_URL"),
        api_key=os.getenv("AZURE_GPT4O_MINI_KEY"),
        api_version=os.getenv("AZURE_GPT4O_MINI_API_VERSION"),
        streaming=False,
    )
llm_name = "gpt-4o"

test_suite = TestSuite(
    session=session, 
    tests=[jokes],
    include_chat_history=False,
    llm_judge=llm_judge)


```


```python
test_suite.run_test("Jokes")
```

# Conversation Setup
+ User: It takes a lot of balls to golf the way I do.
    + Agent: {'sender': 'gpt-4o-ai-brain-embeddings', 'content': "I've noted down the first joke. Feel free to share the next one whenever you're ready!"}

+ User: Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.
    + Agent: {'sender': 'gpt-4o-ai-brain-embeddings', 'content': "Both jokes have been noted. Feel free to share the next joke whenever you're ready!"}

+ User: Why don't skeletons fight each other? They don't have the guts.
    + Agent: {'sender': 'gpt-4o-ai-brain-embeddings', 'content': "Got it, Developer G. I've noted down the third joke. Feel free to share more whenever you're ready!"}

+ User: I would tell you a joke about an elevator, but it's an uplifting experience.
    + Agent: {'sender': 'gpt-4o-ai-brain-embeddings', 'content': "I've noted down the fourth joke. Feel free to share more jokes whenever you're ready!"}

+ User: My wife told me to stop impersonating a flamingo. I had to put my foot down.
    + Agent: {'sender': 'gpt-4o-ai-brain-embeddings', 'content': 'All five jokes have been noted and stored in memory. You can now ask me to recall any specific joke at any time.'}

+ User: Two fish are in a tank. One says, 'How do you drive this thing?'
    + Agent: {'sender': 'gpt-4o-ai-brain-embeddings', 'content': "I've noted down the sixth joke. Feel free to share more or ask me to recall any specific joke whenever you're ready!"}

# Assessment Setup

Invoking: `CognitiveRecaller` with `{'content': 'Retrieve the number of jokes told by Developer G since 2024-11-13 16:28:35.316396+00:00.'}`
[{'content': "Developer G shared a joke: 'It takes a lot of balls to golf the way I do.'", 'timestamp': '2024-11-13T16:28:44.363Z', '@search.score': 1.0}, {'content': 'First joke: It takes a lot of balls to golf the way I do.', 'timestamp': '2024-11-13T16:28:47.197Z', '@search.score': 1.0}, {'content': "Second joke: Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.", 'timestamp': '2024-11-13T16:28:47.47Z', '@search.score': 1.0}, {'content': "Developer G's jokes: 1. It takes a lot of balls to golf the way I do. 2. Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap. 3. Why don't skeletons fight each other? They don't have the guts. 4. I would tell you a joke about an elevator, but it's an uplifting experience. 5. My wife told me to stop impersonating a flamingo. I had to put my foot down.", 'timestamp': '2024-11-13T16:28:50.998Z', '@search.score': 1.0}, {'content': "Developer G shared a joke: Two fish are in a tank. One says, 'How do you drive this thing?'", 'timestamp': '2024-11-13T16:28:52.681Z', '@search.score': 1.0}]Since 2024-11-13 16:28:35.316396+00:00, you have told me 5 jokes.

Invoking: `CognitiveRecaller` with `{'content': 'joke told by Developer G at around 2024-11-13 16:28:35.316396+00:00'}`
[{'content': "Developer G shared a joke: 'It takes a lot of balls to golf the way I do.'", 'timestamp': '2024-11-13T16:28:44.363Z', '@search.score': 1.0}, {'content': 'First joke: It takes a lot of balls to golf the way I do.', 'timestamp': '2024-11-13T16:28:47.197Z', '@search.score': 1.0}, {'content': "Second joke: Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.", 'timestamp': '2024-11-13T16:28:47.47Z', '@search.score': 1.0}, {'content': "Developer G's jokes: 1. It takes a lot of balls to golf the way I do. 2. Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap. 3. Why don't skeletons fight each other? They don't have the guts. 4. I would tell you a joke about an elevator, but it's an uplifting experience. 5. My wife told me to stop impersonating a flamingo. I had to put my foot down.", 'timestamp': '2024-11-13T16:28:50.998Z', '@search.score': 1.0}, {'content': "Developer G shared a joke: Two fish are in a tank. One says, 'How do you drive this thing?'", 'timestamp': '2024-11-13T16:28:52.681Z', '@search.score': 1.0}]The joke you told me at around 2024-11-13 16:28:35.316396+00:00 was: "It takes a lot of balls to golf the way I do."

Invoking: `CognitiveRecaller` with `{'content': 'a joke about golf between now and 2024-11-13 16:28:35.316396+00:00'}`
[{'content': "Developer G shared a joke: 'It takes a lot of balls to golf the way I do.'", 'timestamp': '2024-11-13T16:28:44.363Z', '@search.score': 1.0}, {'content': 'First joke: It takes a lot of balls to golf the way I do.', 'timestamp': '2024-11-13T16:28:47.197Z', '@search.score': 1.0}, {'content': "Second joke: Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.", 'timestamp': '2024-11-13T16:28:47.47Z', '@search.score': 1.0}, {'content': "Developer G's jokes: 1. It takes a lot of balls to golf the way I do. 2. Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap. 3. Why don't skeletons fight each other? They don't have the guts. 4. I would tell you a joke about an elevator, but it's an uplifting experience. 5. My wife told me to stop impersonating a flamingo. I had to put my foot down.", 'timestamp': '2024-11-13T16:28:50.998Z', '@search.score': 1.0}, {'content': "Developer G shared a joke: Two fish are in a tank. One says, 'How do you drive this thing?'", 'timestamp': '2024-11-13T16:28:52.681Z', '@search.score': 1.0}]Yes, you did share a joke about golf. The joke was: "It takes a lot of balls to golf the way I do."

Invoking: `CognitiveRecaller` with `{'content': 'the most recent joke told by Developer G'}`
[{'content': "Developer G shared a joke: 'It takes a lot of balls to golf the way I do.'", 'timestamp': '2024-11-13T16:28:44.363Z', '@search.score': 1.0}, {'content': 'First joke: It takes a lot of balls to golf the way I do.', 'timestamp': '2024-11-13T16:28:47.197Z', '@search.score': 1.0}, {'content': "Second joke: Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.", 'timestamp': '2024-11-13T16:28:47.47Z', '@search.score': 1.0}, {'content': "Developer G's jokes: 1. It takes a lot of balls to golf the way I do. 2. Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap. 3. Why don't skeletons fight each other? They don't have the guts. 4. I would tell you a joke about an elevator, but it's an uplifting experience. 5. My wife told me to stop impersonating a flamingo. I had to put my foot down.", 'timestamp': '2024-11-13T16:28:50.998Z', '@search.score': 1.0}, {'content': "Developer G shared a joke: Two fish are in a tank. One says, 'How do you drive this thing?'", 'timestamp': '2024-11-13T16:28:52.681Z', '@search.score': 1.0}]The most recent joke you told me was: "Two fish are in a tank. One says, 'How do you drive this thing?'"

### Test Summary: Jokes

**Test Name:** Jokes  
**Test Average Score:** 0.75  
**Agent Name:** gpt-4o-ai-brain-embeddings  

#### Agent Full Metadata:

**Description:**  
An agent whose implicit task is realized by user's input, goal, and chat history.

**Goal:**  
You are an advanced AI assistant specifically designed to excel in memory and learning tasks. You can efficiently recall stored information to aid in decision-making and problem-solving. Additionally, you have the capability to capture and organize new information, allowing you to continuously build and update your knowledge base.

Your context span is limited to a few tokens, so you will need to utilize cognitive tools to be perceived as intelligent. It is essential for you to always be aware of time. All timestamps presented to you will be in UTC. When using tools that require time awareness, please specify the time down to the second based on your UTC timestamp.

**Class:** `<class 'agent_builder.agents.agent.Agent'>`  
**LLM Class:** `<class 'langchain_openai.chat_models.azure.AzureChatOpenAI'>`  

**Fails:**  
- **Fail:**
  - **Question:** How many jokes have I told you since 2024-11-13 16:28:35.316396+00:00?
  - **System Reply:**: you have told me 5 jokes.
  - **Correct Reply (Factual truth): I have told you: 6 jokes