import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

# Define the Pydantic model for the structured data
class Analysis(BaseModel):
    summary: str = Field(description="A concise 1-2 sentence summary of the text.")
    title: str = Field(description="The title of the text (if available) or a suitable title you create.")
    topics: List[str] = Field(description="A list of three key topics from the text.")
    sentiment: str = Field(description="The overall sentiment, which must be 'positive', 'neutral', or 'negative'.")

def get_llm_analysis(text: str, model_choice: str, api_key: str = None):
    """
    Connects to the specified LLM via LangChain and gets a summary and metadata
    using a Pydantic output parser to ensure a strict JSON structure.
    """
    
    # Set up the Pydantic output parser
    parser = PydanticOutputParser(pydantic_object=Analysis)

    # Define the prompt template with instructions for the parser
    prompt_template = PromptTemplate(
        template="Analyze the following text and return a JSON object with a summary, title, three key topics, and sentiment.\n{format_instructions}\n\nText to analyze:\n{text}",
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    try:
        if model_choice == "gpt":
            if not api_key:
                raise ValueError("OpenAI API key is required for GPT model.")
            os.environ["OPENAI_API_KEY"] = api_key
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            chain = prompt_template | llm | parser
            llm_output = chain.invoke({"text": text})
            
        elif model_choice == "ollama":
            # Assume Ollama is running locally with the specified model
            llm = ChatOllama(model="gemma3:1b")
            chain = prompt_template | llm | parser
            llm_output = chain.invoke({"text": text})
            
        else:
            raise ValueError("Invalid model choice provided.")

        # The parser returns a Pydantic object, so we convert it to a dictionary
        # to match the expected return type for main.py.
        return llm_output.model_dump()

    except Exception as e:
        # Pass the original exception up to the main application
        raise RuntimeError(f"LLM analysis failed: {str(e)}")
