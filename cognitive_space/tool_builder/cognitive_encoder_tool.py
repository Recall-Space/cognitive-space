from textwrap import dedent
from pydantic import BaseModel, Field
from agent_builder.builders.tool_builder import ToolBuilder
from cognitive_space.brain import Brain


def build_standard_encoder_tool(brain: Brain):
    # Define your schema as a subclass of BaseModel
    # Schema for the information that will be encoded in memory
    class CognitiveEncoderSchema(BaseModel):
        content: str = Field(description="Information to be encoded in memory. ")

    # Instantiate the tool builder.
    tool_builder = ToolBuilder()
    # Define name of tool.
    tool_builder.set_name(name="CognitiveEncoder")
    # Set the function for the tool.
    tool_builder.set_function(function=brain.encode)
    # Provide the description for tool
    tool_builder.set_description(
        description=dedent(
            """
        The Cognitive Encoder Tool is responsible for encoding information into memory, 
        simulating the human learning process. This tool captures and organizes new data,
        experiences, and knowledge, storing them effectively for future use. It mimics the 
        cognitive process of encoding, where information from the environment is transformed 
        into a format that can be stored in long-term memory. This tool ensures that the agent 
        can learn from interactions, adapt to new information, and build a comprehensive 
        knowledge base over time.
                    """
        )
    )
    # Add the tool schema
    tool_builder.set_schema(schema=CognitiveEncoderSchema)
    # Build and get the tool
    cognitive_encoder_tool = tool_builder.build()
    return cognitive_encoder_tool