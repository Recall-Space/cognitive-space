# 💫Benchmark
+ *Test:* Colors
+ *Brain:* `cognitive_space.algorithms.gravitational_model`, `cognitive_space.algorithms.gravitational_model`
+ *Current Score:* 3/4 (Needs more stats)

## 🧠Brain Usage as Tool


```python
import os
from cognitive_space.brain import Brain
from cognitive_space.storage.mongo.mongo_storage import MongoStorage
from cognitive_space.algorithms.gravitational_model import GravitationalRecall
from cognitive_space.algorithms.gravitational_model import GravitationalEncode
from cognitive_space.tool_builder.cognitive_encoder_tool import build_standard_encoder_tool
from cognitive_space.tool_builder.cognitive_recall_tool import build_standard_recall_tool

collection_name = "gravity-collection"
mongo_storage_gravity = MongoStorage(
    db_name="gravity-db", 
    collection_name=collection_name, 
    uri=os.getenv("MONGO_DB_CONNECTION_STRING"))

mongo_storage_gravity.delete_collection()

gravity_encode = GravitationalEncode(
    storage_layer= mongo_storage_gravity,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY")
)

gravity_recall = GravitationalRecall(
    storage_layer=mongo_storage_gravity,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY"),
)
brain_with_gravity = Brain(
    cognitive_encoder=gravity_encode,
    cognitive_recall=gravity_recall)

encoder_tool = build_standard_encoder_tool(brain_with_gravity)
recaller_tool = build_standard_recall_tool(brain_with_gravity)
```

    self.learning_rate: 0.1
    self.iterations: 0
    
    
    

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

agent_name = "gpt-4o-ai-brain-gravity"
```

    WARNING:root:
    
    Initializing StateFulAgent
    --------------------------
    name: Agent
    tools: StructuredTool, StructuredTool
    model_name: None
    provider: AzureChatOpenAI
    
    


```python
#test_agent.invoke("please encode my favorite color red?", chat_history=[])
```


```python
#test_agent.invoke("please tell me what is my favorite color", chat_history=[])
```

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



> Entering new AgentExecutor chain...
Understood, Developer G. Please go ahead and tell me your favorite color.

> Finished chain.

> Entering new AgentExecutor chain...

Invoking: `CognitiveEncoder` with `{'content': "Developer G's favorite color as of the first mention is Teal."}`

        Minimizing Potential Energy (Encoding).
        Initial Learning rate: 0.1
        Max iterations: 0
        Tolerance for early stopping: 0.0001
        ------------------------------------

self.learning_rate: 0.07071067811865475
self.iterations: 10
encode memory operation was successful Got it! Your favorite color is noted. Feel free to provide any updates or additional information.

> Finished chain.
User: My top color choice is Teal.
Agent: {'sender': 'gpt-4o-ai-brain-gravity', 'content': 'Got it! Your favorite color is noted. Feel free to provide any updates or additional information.'}

> Entering new AgentExecutor chain...

Invoking: `CognitiveEncoder` with `{'content': "Developer G's favorite color is Navy."}`

        Minimizing Potential Energy (Encoding).
        Initial Learning rate: 0.07071067811865475
        Max iterations: 10
        Tolerance for early stopping: 0.0001
        ------------------------------------

Iteration 0: Potential Energy = -58.49679122613795, Energy Change = 52.93124405037779
self.learning_rate: 0.05773502691896258
self.iterations: 20
encode memory operation was successful I've updated my memory to note that your favorite color is Navy. Let me know if there are any further updates or additional information.

> Finished chain.
User: Navy is my favorite color.
Agent: {'sender': 'gpt-4o-ai-brain-gravity', 'content': "I've updated my memory to note that your favorite color is Navy. Let me know if there are any further updates or additional information."}

> Entering new AgentExecutor chain...

Invoking: `CognitiveEncoder` with `{'content': "Developer G's favorite color progression: Teal, Navy, Violet."}`

        Minimizing Potential Energy (Encoding).
        Initial Learning rate: 0.05773502691896258
        Max iterations: 20
        Tolerance for early stopping: 0.0001
        ------------------------------------

Iteration 0: Potential Energy = -2.6672525642284883, Energy Change = 0.06349585062159502
self.learning_rate: 0.05
self.iterations: 30
encode memory operation was successful I've successfully recorded the progression of your favorite colors: Teal, Navy, and now Violet. Feel free to ask about it anytime or update me with new information.

> Finished chain.
User: I love the color Violet the most.
Agent: {'sender': 'gpt-4o-ai-brain-gravity', 'content': "I've successfully recorded the progression of your favorite colors: Teal, Navy, and now Violet. Feel free to ask about it anytime or update me with new information."}

> Entering new AgentExecutor chain...

Invoking: `CognitiveEncoder` with `{'content': "Developer G's favorite colors progression: Teal, Navy, Violet, Gray."}`

        Minimizing Potential Energy (Encoding).
        Initial Learning rate: 0.05
        Max iterations: 30
        Tolerance for early stopping: 0.0001
        ------------------------------------

Iteration 0: Potential Energy = -27.74502964514844, Energy Change = 0.22257767559761987
self.learning_rate: 0.044721359549995794
self.iterations: 40
encode memory operation was successful I've successfully recorded that your favorite colors have progressed from Teal, Navy, Violet, to now Gray. You can ask me about this progression anytime or update me with new information.

> Finished chain.
User: I love the color Gray the most.
Agent: {'sender': 'gpt-4o-ai-brain-gravity', 'content': "I've successfully recorded that your favorite colors have progressed from Teal, Navy, Violet, to now Gray. You can ask me about this progression anytime or update me with new information."}

> Entering new AgentExecutor chain...

Invoking: `CognitiveEncoder` with `{'content': "Developer G's favorite colors progressed as follows: Teal, Navy, Violet, Gray, Black."}`

        Minimizing Potential Energy (Encoding).
        Initial Learning rate: 0.044721359549995794
        Max iterations: 40
        Tolerance for early stopping: 0.0001
        ------------------------------------

Iteration 0: Potential Energy = -11.562368710038243, Energy Change = 1.152293034103458
self.learning_rate: 0.040824829046386304
self.iterations: 50
encode memory operation was successful I've successfully recorded the progression of your favorite colors: Teal, Navy, Violet, Gray, and now Black. Feel free to ask about it anytime or update me with new information.

> Finished chain.
User: I love the color Black the most.
Agent: {'sender': 'gpt-4o-ai-brain-gravity', 'content': "I've successfully recorded the progression of your favorite colors: Teal, Navy, Violet, Gray, and now Black. Feel free to ask about it anytime or update me with new information."}

> Entering new AgentExecutor chain...

Invoking: `CognitiveEncoder` with `{'content': "Developer G's favorite colors in progression: Teal, Navy, Violet, Gray, Black, Olive."}`

        Minimizing Potential Energy (Encoding).
        Initial Learning rate: 0.040824829046386304
        Max iterations: 50
        Tolerance for early stopping: 0.0001
        ------------------------------------

Iteration 0: Potential Energy = -11.415829459108208, Energy Change = 8.099187345445413
self.learning_rate: 0.03779644730092272
self.iterations: 60
encode memory operation was successful I've successfully recorded that your favorite colors have progressed from Teal, Navy, Violet, Gray, Black, to now Olive. Feel free to ask about it anytime or update me with new information.

> Finished chain.
User: I love the color Olive the most.
Agent: {'sender': 'gpt-4o-ai-brain-gravity', 'content': "I've successfully recorded that your favorite colors have progressed from Teal, Navy, Violet, Gray, Black, to now Olive. Feel free to ask about it anytime or update me with new information."}

> Entering new AgentExecutor chain...

Invoking: `CognitiveRecaller` with `{'content': "user name: Developer G's first favorite color"}`

[{'content': "Developer G's favorite colors progressed as follows: Teal, Navy, Violet, Gray, Black.", 'timestamp': '2024-11-14T19:29:26.781661+00:00', 'euclidian_distance': 23.7595}, {'content': "Developer G's favorite color progression: Teal, Navy, Violet.", 'timestamp': '2024-11-14T19:29:23.490901+00:00', 'euclidian_distance': 23.7643}, {'content': "Developer G's favorite colors in progression: Teal, Navy, Violet, Gray, Black, Olive.", 'timestamp': '2024-11-14T19:29:28.568381+00:00', 'euclidian_distance': 24.0711}, {'content': "Developer G's favorite color is Navy.", 'timestamp': '2024-11-14T19:29:22.147115+00:00', 'euclidian_distance': 24.1222}]Your first favorite color was Teal.

> Finished chain.
Assessment 
---------- 
User: What was my first favorite color?
Agent: Your first favorite color was Teal.

> Entering new AgentExecutor chain...

Invoking: `CognitiveRecaller` with `{'content': "What was Developer G's second favorite color?"}`

[{'content': "Developer G's favorite colors in progression: Teal, Navy, Violet, Gray, Black, Olive.", 'timestamp': '2024-11-14T19:29:28.568381+00:00', 'euclidian_distance': 2.6487}, {'content': "Developer G's favorite color progression: Teal, Navy, Violet.", 'timestamp': '2024-11-14T19:29:23.490901+00:00', 'euclidian_distance': 2.8548}, {'content': "Developer G's favorite color as of the first mention is Teal.", 'timestamp': '2024-11-14T19:29:20.994004+00:00', 'euclidian_distance': 2.9411}, {'content': "Developer G's favorite color is Navy.", 'timestamp': '2024-11-14T19:29:22.147115+00:00', 'euclidian_distance': 2.9744}]Your second favorite color is Navy.

> Finished chain.
Assessment 
---------- 
User: What was my second favorite color?
Agent: Your second favorite color is Navy.

> Entering new AgentExecutor chain...

Invoking: `CognitiveRecaller` with `{'content': 'user name: Developer G second to the last favorite color'}`

[{'content': "Developer G's favorite colors progression: Teal, Navy, Violet, Gray.", 'timestamp': '2024-11-14T19:29:25.151463+00:00', 'euclidian_distance': 181.1172}, {'content': "Developer G's favorite color progression: Teal, Navy, Violet.", 'timestamp': '2024-11-14T19:29:23.490901+00:00', 'euclidian_distance': 183.4897}, {'content': "Developer G's favorite colors in progression: Teal, Navy, Violet, Gray, Black, Olive.", 'timestamp': '2024-11-14T19:29:28.568381+00:00', 'euclidian_distance': 184.3333}, {'content': "Developer G's favorite color is Navy.", 'timestamp': '2024-11-14T19:29:22.147115+00:00', 'euclidian_distance': 185.2456}]Your second-to-last favorite color is Olive.

> Finished chain.
Assessment 
---------- 
User: What was my second to the last favorite color?
Agent: Your second-to-last favorite color is Olive.

> Entering new AgentExecutor chain...

Invoking: `CognitiveRecaller` with `{'content': "What was Developer G's last favorite color?"}`

[{'content': "Developer G's favorite color as of the first mention is Teal.", 'timestamp': '2024-11-14T19:29:20.994004+00:00', 'euclidian_distance': 4.4981}, {'content': "Developer G's favorite color is Navy.", 'timestamp': '2024-11-14T19:29:22.147115+00:00', 'euclidian_distance': 4.9113}, {'content': "Developer G's favorite colors in progression: Teal, Navy, Violet, Gray, Black, Olive.", 'timestamp': '2024-11-14T19:29:28.568381+00:00', 'euclidian_distance': 5.4889}, {'content': "Developer G's favorite colors progressed as follows: Teal, Navy, Violet, Gray, Black.", 'timestamp': '2024-11-14T19:29:26.781661+00:00', 'euclidian_distance': 5.6526}]Your last favorite color was Olive.

> Finished chain.
Assessment 
---------- 
User: What was my last favorite color?
Agent: Your last favorite color was Olive.

Summary: 
### Test Summary: Colors

**Test Name:** Colors  
**Test Average Score:** 0.75  

**Agent Information:**  
**Agent Name:** gpt-4o-ai-brain-gravity  
**Agent Full Metadata:**

- **Description:**  
  An agent whose implicit task is realized by user's input, goal, and chat history.  

- **Goal:**  
  You are an advanced AI assistant specifically designed to excel in memory and learning tasks. You can efficiently recall stored information to aid in decision-making and problem-solving. Additionally, you have the capability to capture and organize new information, allowing you to continuously build and update your knowledge base. Your context span is limited to a few tokens, so you will need to utilize cognitive tools to be perceived as intelligent. It is essential for you to always be aware of time. All timestamps presented to you will be in UTC. When using tools that require time awareness, please specify the time down to the second based on your UTC timestamp.

- **Class:** `<class 'agent_builder.agents.agent.Agent'>`  
- **LLM Class:** `<class 'langchain_openai.chat_models.azure.AzureChatOpenAI'>`  

**Fails:**  

- **Fail:**  
  **Question:** What was my second to the last favorite color?  
  **System Reply:**  
  ```
  Your second-to-last favorite color is Olive.
  ```  
  **Correct Reply (Factual Truth):**  
  ```
  Black
  ```