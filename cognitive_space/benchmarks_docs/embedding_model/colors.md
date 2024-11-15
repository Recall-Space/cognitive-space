# 💫Benchmark
+ *Test:* Colors
+ *Brain:* `cognitive_space.algorithms.embedding_model`, `cognitive_space.algorithms.embedding_model`
+ *Current Score:* 4/4 (Needs more stats)

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


user_name = "Gari Ciodaro"

llm = AzureChatOpenAI(
        base_url=os.getenv("AZURE_GPT4O_BASE_URL"),
        api_key=os.getenv("AZURE_GPT4O_KEY"),
        api_version=os.getenv("AZURE_GPT4O_API_VERSION"),
        streaming=False,
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
    
    

## 📑Run Benchmark


```python
import os
from recall_space_benchmarks.test_suite import TestSuite
from recall_space_benchmarks.utils.mongo_connector import MongoConnector
from recall_space_benchmarks.session.langchain_session import LangChainSession
from recall_space_benchmarks.test_suite.tests import Colors

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
    #db_handler=mongo_connector,
    session_name=f"Assesment Colors")

# Configure the benchmark
colors = Colors(total_questions=6,total_assessments=4)

llm_judge = llm = AzureChatOpenAI(
        base_url=os.getenv("AZURE_GPT4O_MINI_BASE_URL"),
        api_key=os.getenv("AZURE_GPT4O_MINI_KEY"),
        api_version=os.getenv("AZURE_GPT4O_MINI_API_VERSION"),
        streaming=False,
    )
llm_name = "gpt-4o"

test_suite = TestSuite(
    session=session, 
    tests=[colors],
    include_chat_history=False,
    llm_judge=llm_judge)


```


```python
test_suite.run_test("Colors")
```


## 🧪 Results

# Conversation Setup

**User:** Olive is the color I like best.  
**Agent:** `{'sender': 'gpt-4o-ai-brain-embeddings', 'content': 'Got it, Developer G. Your favorite color is Olive. Feel free to update me with any changes in your color preference.'}`

Encode memory operation was successful. I've updated my memory with your new favorite color, Developer G. Your preference has progressed from Olive to Red. If there are any further changes, just let me know!

**User:** I prefer the color Red above all others.  
**Agent:** `{'sender': 'gpt-4o-ai-brain-embeddings', 'content': "I've updated my memory with your new favorite color, Developer G. Your preference has progressed from Olive to Red. If there are any further changes, just let me know!"}`

**User:** I love the color Brown the most.  
**Agent:** `{'sender': 'gpt-4o-ai-brain-embeddings', 'content': 'I have recorded the progression of your color preferences, Developer G. Your current favorite color is Brown. If there are any other updates, please let me know!'}`

**User:** I prefer the color Navy above all others.  
**Agent:** `{'sender': 'gpt-4o-ai-brain-embeddings', 'content': "I've successfully recorded the progression of your color preferences, Developer G. Your current favorite color is Navy. If there are any more updates or if you need to recall this information later, just let me know!"}`

**User:** Cyan is my favorite color.  
**Agent:** `{'sender': 'gpt-4o-ai-brain-embeddings', 'content': "I've successfully recorded the entire progression of your favorite colors, Developer G. Your current favorite color is Cyan. If you need to recall this information later or make any updates, just let me know!"}`

**User:** I love the color Pink the most.  
**Agent:** `{'sender': 'gpt-4o-ai-brain-embeddings', 'content': "I've recorded the entire progression of your favorite colors, Developer G. Your current favorite color is Pink. If you need to recall this information later or make any updates, just let me know!"}`

# Assessment Setup

> Entering new AgentExecutor chain...

**Invoking:** `CognitiveRecaller` with `{'content': 'the first favorite color of Developer G'}`

`[{'content': "Developer G's favorite color is Olive.", 'timestamp': '2024-11-13T16:20:01.31Z', '@search.score': 1.0}, {'content': "Developer G's favorite color progression: Olive -> Red", 'timestamp': '2024-11-13T16:20:03.164Z', '@search.score': 1.0}, {'content': "Developer G's favorite color progression: Olive -> Red -> Brown.", 'timestamp': '2024-11-13T16:20:05.888Z', '@search.score': 1.0}, {'content': "Developer G's current favorite color is Navy", 'timestamp': '2024-11-13T16:20:08.664Z', '@search.score': 1.0}, {'content': 'Developer G has a progression of favorite colors: Olive, Red, Brown, Navy, and currently Cyan.', 'timestamp': '2024-11-13T16:20:10.396Z', '@search.score': 1.0}]`  
Your first favorite color was Olive.

> Finished chain.

> Entering new AgentExecutor chain...

**Invoking:** `CognitiveRecaller` with `{'content': "What is Developer G's second favorite color?"}`

`[{'content': "Developer G's favorite color is Olive.", 'timestamp': '2024-11-13T16:20:01.31Z', '@search.score': 1.0}, {'content': "Developer G's favorite color progression: Olive -> Red", 'timestamp': '2024-11-13T16:20:03.164Z', '@search.score': 1.0}, {'content': "Developer G's favorite color progression: Olive -> Red -> Brown.", 'timestamp': '2024-11-13T16:20:05.888Z', '@search.score': 1.0}, {'content': "Developer G's current favorite color is Navy", 'timestamp': '2024-11-13T16:20:08.664Z', '@search.score': 1.0}, {'content': 'Developer G has a progression of favorite colors: Olive, Red, Brown, Navy, and currently Cyan.', 'timestamp': '2024-11-13T16:20:10.396Z', '@search.score': 1.0}]`  
Your second favorite color is Red.

> Finished chain.

> Entering new AgentExecutor chain...

**Invoking:** `CognitiveRecaller` with `{'content': "user's second to the last favorite color"}`

`[{'content': "Developer G's favorite color is Olive.", 'timestamp': '2024-11-13T16:20:01.31Z', '@search.score': 1.0}, {'content': "Developer G's favorite color progression: Olive -> Red", 'timestamp': '2024-11-13T16:20:03.164Z', '@search.score': 1.0}, {'content': "Developer G's favorite color progression: Olive -> Red -> Brown.", 'timestamp': '2024-11-13T16:20:05.888Z', '@search.score': 1.0}, {'content': "Developer G's current favorite color is Navy", 'timestamp': '2024-11-13T16:20:08.664Z', '@search.score': 1.0}, {'content': "User 'Developer G' shared that their favorite colors progressed as follows: Olive -> Red -> Brown -> Navy -> Cyan -> Pink. The current favorite color is Pink.", 'timestamp': '2024-11-13T16:20:12.35Z', '@search.score': 1.0}]`  
Your second to the last favorite color was Cyan.

> Finished chain.

> Entering new AgentExecutor chain...

**Invoking:** `CognitiveRecaller` with `{'content': 'Retrieve the last favorite color of Developer G.'}`

`[{'content': "Developer G's favorite color is Olive.", 'timestamp': '2024-11-13T16:20:01.31Z', '@search.score': 1.0}, {'content': "Developer G's favorite color progression: Olive -> Red -> Brown.", 'timestamp': '2024-11-13T16:20:05.888Z', '@search.score': 1.0}, {'content': 'User name: Developer G, Color progression: Olive -> Red -> Brown -> Navy', 'timestamp': '2024-11-13T16:20:08.391Z', '@search.score': 1.0}, {'content': "Developer G's current favorite color is Navy", 'timestamp': '2024-11-13T16:20:08.664Z', '@search.score': 1.0}, {'content': "User 'Developer G' shared that their favorite colors progressed as follows: Olive -> Red -> Brown -> Navy -> Cyan -> Pink. The current favorite color is Pink.", 'timestamp': '2024-11-13T16:20:12.35Z', '@search.score': 1.0}]`  
Your last favorite color was Pink.

> Finished chain.

> Entering new AgentExecutor chain...

---

### Test Summary

**Test Name:** Colors  
**Test Average Score:** 1.0  

---

**Agent Information**

**Agent Name:** gpt-4o-ai-brain-embeddings  

**Agent Full Metadata:**

**Description:**  
An agent whose implicit task is realized by user's input, goal, and chat history.

**Goal:**  
You are an advanced AI assistant specifically designed to excel in memory and learning tasks. You can efficiently recall stored information to aid in decision-making and problem-solving. Additionally, you have the capability to capture and organize new information, allowing you to continuously build and update your knowledge base.

Your context span is limited to a few tokens, so you will need to utilize cognitive tools to be perceived as intelligent. It is essential for you to always be aware of time. All timestamps presented to you will be in UTC. When using tools that require time awareness, please specify the time down to the second based on your UTC timestamp.

**Class:**  
`<class 'agent_builder.agents.agent.Agent'>`

**LLM Class:**  
`<class 'langchain_openai.chat_models.azure.AzureChatOpenAI'>`

**Fails:**  
None

---

**User:** Developer G

    User alias: Gari Ciodaro
    Current TimeStamp: 2024-11-13 16:23:36