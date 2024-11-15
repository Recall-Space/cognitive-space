from textwrap import dedent
from pydantic import BaseModel, Field
from agent_builder.builders.tool_builder import ToolBuilder
from cognitive_space.brain import Brain


def build_standard_recall_tool(brain: Brain):
    # Define your schema as a subclass of BaseModel
    # Schema for the information that will be encoded in memory
    class CognitiveRecallerSchema(BaseModel):
        content: str = Field(description="Detailed instructions to recall the memory")

    # Instantiate the tool builder.
    tool_builder = ToolBuilder()
    # Define name of tool.
    tool_builder.set_name(name="CognitiveRecaller")
    # Set the function for the tool.
    tool_builder.set_function(function=brain.recall)
    # Provide the description for tool
    tool_builder.set_description(
        description=dedent(
        """
        The Cognitive Recall Tool is designed to retrieve stored information from memory,
        emulating the cognitive process of recalling. This tool accesses encoded knowledge,
        experiences, and data, bringing relevant information back into active use when needed.
        It supports decision-making, problem-solving, and reasoning by providing timely access
        to previously learned information. The Cognitive Recall Tool ensures that the agent can
        efficiently utilize its memory to respond to queries, perform tasks, and adapt to new
        situations by referencing past knowledge.
        """
        )
    )
    # Add the tool schema
    tool_builder.set_schema(schema=CognitiveRecallerSchema)
    # Build and get the tool
    cognitive_recaller_tool = tool_builder.build()
    return cognitive_recaller_tool