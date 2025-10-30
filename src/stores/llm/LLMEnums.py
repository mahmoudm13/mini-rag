from enum import Enum

class LLMEnums(Enum):    
    OPENAI = "OPENAI"
    COHERE = "COFERE"

class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
