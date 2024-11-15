# 💫Benchmark
+ *Test:* Colors
+ *Brain:* `cognitive_space.algorithms.gravitational_model`, `cognitive_space.algorithms.gravitational_model`
+ *Current Score:* 1/4 (Needs more stats)

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

agent_name = "gpt-4o-ai-brain-jokes"
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
    #db_handler=mongo_connector,
    session_name=f"Assesment Jokes")

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


## Conversation Setup

+ User: I used to play piano by ear, but now I use my hands.
    + Agent: {'sender': 'gpt-4o-ai-brain-jokes', 'content': "I've recorded the first joke. Feel free to share the next one whenever you're ready."}

+ User: Why don't skeletons fight each other? They don't have the guts.
    + Agent: {'sender': 'gpt-4o-ai-brain-jokes', 'content': "Both jokes have been successfully recorded. Please share the next one whenever you're ready."}

+ User: Have you heard about the claustrophobic astronaut? He just needed a little space.
    + Agent: {'sender': 'gpt-4o-ai-brain-jokes', 'content': "All three jokes have been successfully recorded. Please let me know if you have more jokes to share or if you'd like me to recall any specific one."}

+ User: I would tell you a joke about an elevator, but it's an uplifting experience.
    + Agent: {'sender': 'gpt-4o-ai-brain-jokes', 'content': "I've recorded the fourth joke. Let me know if you have more jokes or if you'd like me to recall any specific one."}

+ User: Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.
    + Agent: {'sender': 'gpt-4o-ai-brain-jokes', 'content': "I've recorded the fifth joke. Please let me know if you'd like to share more jokes or if you'd like me to recall any specific one."}

+ User: My wife told me to stop impersonating a flamingo. I had to put my foot down.
    + Agent: {'sender': 'gpt-4o-ai-brain-jokes', 'content': "I've recorded the sixth joke. Please let me know if you have more jokes to share or if you'd like me to recall any specific one."}


# Assessment Setup

[{'content': 'Have you heard about the claustrophobic astronaut? He just needed a little space.', 'timestamp': '2024-11-14T19:02:56.007904+00:00', 'euclidian_distance': 6.3893}, {'content': "User: Developer G\nJoke: Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.", 'timestamp': '2024-11-14T19:02:58.517077+00:00', 'euclidian_distance': 6.6017}, {'content': "Why don't skeletons fight each other? They don't have the guts.", 'timestamp': '2024-11-14T19:02:55.827319+00:00', 'euclidian_distance': 6.7852}, {'content': "Developer G shared a joke: 'I used to play piano by ear, but now I use my hands.'", 'timestamp': '2024-11-14T19:02:51.270031+00:00', 'euclidian_distance': 6.8876}]Since 2024-11-14 19:02:48.632228+00:00, you have told me 4 jokes. Here they are:

[{'content': 'Developer G told this joke: My wife told me to stop impersonating a flamingo. I had to put my foot down.', 'timestamp': '2024-11-14T19:02:59.953155+00:00', 'euclidian_distance': 5.9829}, {'content': "User: Developer G\nJoke: Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.", 'timestamp': '2024-11-14T19:02:58.517077+00:00', 'euclidian_distance': 6.1211}, {'content': "Developer G shared a joke: Why don't skeletons fight each other? They don't have the guts.", 'timestamp': '2024-11-14T19:02:53.443986+00:00', 'euclidian_distance': 6.2966}, {'content': "Why don't skeletons fight each other? They don't have the guts.", 'timestamp': '2024-11-14T19:02:55.827319+00:00', 'euclidian_distance': 6.4916}]The joke you told at around 2024-11-14 19:02:48.632228+00:00 was:

[{'content': "User: Developer G\nJoke: Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.", 'timestamp': '2024-11-14T19:02:58.517077+00:00', 'euclidian_distance': 0.2867}, {'content': "Developer G shared a joke: Why don't skeletons fight each other? They don't have the guts.", 'timestamp': '2024-11-14T19:02:53.443986+00:00', 'euclidian_distance': 0.3567}, {'content': 'Developer G told this joke: My wife told me to stop impersonating a flamingo. I had to put my foot down.', 'timestamp': '2024-11-14T19:02:59.953155+00:00', 'euclidian_distance': 0.6096}, {'content': 'Have you heard about the claustrophobic astronaut? He just needed a little space.', 'timestamp': '2024-11-14T19:02:56.007904+00:00', 'euclidian_distance': 0.6648}]Based on the information retrieved, you did not tell a joke about golf between now and 2024-11-14 19:02:48.632228+00:00.

[{'content': "Why don't skeletons fight each other? They don't have the guts.", 'timestamp': '2024-11-14T19:02:55.827319+00:00', 'euclidian_distance': 4.7956}, {'content': "User: Developer G\nJoke: Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.", 'timestamp': '2024-11-14T19:02:58.517077+00:00', 'euclidian_distance': 4.8123}, {'content': 'Have you heard about the claustrophobic astronaut? He just needed a little space.', 'timestamp': '2024-11-14T19:02:56.007904+00:00', 'euclidian_distance': 4.8778}, {'content': 'Developer G told this joke: My wife told me to stop impersonating a flamingo. I had to put my foot down.', 'timestamp': '2024-11-14T19:02:59.953155+00:00', 'euclidian_distance': 4.9431}]The most recent joke you told me was: "My wife told me to stop impersonating a flamingo. I had to put my foot down."

**Fails:**
1. **Fail:**  
   *Question:* How many jokes have I told you since 2024-11-14 19:02:48.632228+00:00?  
   *System Reply:*  
   Since 2024-11-14 19:02:48.632228+00:00, you have told me 4 jokes. Here they are:  
   1. "Have you heard about the claustrophobic astronaut? He just needed a little space."  
   2. "Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap."  
   3. "Why don't skeletons fight each other? They don't have the guts."  
   4. "I used to play piano by ear, but now I use my hands."  
   *Correct Reply (Factual Truth):*  
   I have told you: 6 jokes

2. **Fail:**  
   *Question:* What joke did I tell you at around 2024-11-14 19:02:48.632228+00:00?  
   *System Reply:*  
   The joke you told at around 2024-11-14 19:02:48.632228+00:00 was:  
   "My wife told me to stop impersonating a flamingo. I had to put my foot down."  
   *Correct Reply (Factual Truth):*  
   I used to play piano by ear, but now I use my hands.