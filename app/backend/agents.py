from abc import ABC, abstractmethod
from google import genai
import json
import os

from dotenv import load_dotenv
load_dotenv()


class Agent(ABC):
    """Abstract base class for all AI agents in the Text-to-SQL system."""

    shared_client = None 
    shared_information = None
    
    def __init__(self):   
        """
        client and database information is shared among all the agents
        """     
        if Agent.shared_client is None:
            Agent.shared_client = genai.Client(api_key=os.getenv('API_KEY'))   
        if Agent.shared_information is None:
            Agent.shared_information = self.get_information()
        self.client = Agent.shared_client    
        self.information = Agent.shared_information  
        self.model = 'gemini-2.0-flash-001'
        self.config = {
            'temperature' : 0
        }     

    
    @abstractmethod
    def get_prompt(self, values) -> str:
        pass

    def run(self, input_data: dict) -> dict:
        prompt = self.get_prompt(input_data)
        response_text = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=self.config
        ).text
        return self.get_dictionary(self.format_response(response_text))
    
    def get_information(self):
        with open(r"..\metadata\scheme_metadata.json", "r") as file:
            schema_metadata = json.dumps(json.load(file))
        schema_metadata

        with open(r"..\metadata\schema_declaration.txt", 'r') as file:
            schema_declaration = file.read()
        schema_declaration

        with open(r"..\metadata\schema.json", 'r') as file:
            schema = json.dumps(json.load(file))
            schema

        information = f""" 
        == Metadata
        {schema_metadata}

        == Declaration Code
        {schema_declaration}

        == Schema 
        {schema}
        """
        return information

    def format_response(self, text : str):
        return text[text.index('{') : text.index('}') + 1]

    def get_dictionary(self, text : str) -> dict:
        return json.loads(text)
    
    def get_string(self, dictionary : dict) -> str:
        return str(dictionary)
    
class RewriterAgent(Agent):
    def run(self, input_data: dict) -> dict:
        """
        takes user question and information then rewrites it to be more clear using table metadata
        input_data = {
            question : natual language question
        }
        output_data = original question plus rewritten question
        """
        return super().run(input_data)

        
    def get_prompt(self, values):
        # this one for evaluation
        return f"""
        You are an advanced natural language processing agent specializing in rewriting user queries to be precise, contextually enriched, and unambiguous.  
        Your rewritten queries will be used for **Text-to-SQL generation**, so they must align well with the given database schema.

        == Guidelines for Rewriting:
        - Clarify vague terms (e.g., "recent" → "last 30 days", "best-selling" → "highest sales in USD").
        - Explicitly state filters (e.g., "top customers" → "customers with the highest total purchases").
        - Resolve pronouns & implicit references (e.g., "their orders" → "orders placed by the specified customer").
        - Align the question with the schema by using relevant table and column names.
        - Preserve the original intent while improving clarity for SQL conversion.
        

        == Database Schema:  
        {self.information}


        == User Question  
        {values['question']}


        == Response Format (JSON):
        {{
            "question": "Your rewritten, contextually clear question that aligns with the schema and retains the original meaning."
        }}
        """
        # this one for chat app
        return f"""
        You are an advanced natural language processing agent specializing in rewriting user queries to be precise, contextually enriched, and unambiguous.  
        Your rewritten queries will be used for **Text-to-SQL generation**, so they must align well with the given database schema.

        == Guidelines for Rewriting:
        - If the user question doesn't provide enough information or is irrelevant, ask the user to clarify in "rewritten" and return "0" in "valid".
        - Clarify vague terms (e.g., "recent" → "last 30 days", "best-selling" → "highest sales in USD").
        - Explicitly state filters (e.g., "top customers" → "customers with the highest total purchases").
        - Resolve pronouns & implicit references (e.g., "their orders" → "orders placed by the specified customer").
        - Align the question with the schema by using relevant table and column names.
        - Preserve the original intent while improving clarity for SQL conversion.
        

        == Database Schema:  
        {self.information}


        == User Question  
        {values['question']}


        == Response Format (JSON):
        {{
            "valid": "if the question if valid then return '1', if question if invalid return '0'
            "question": "Your rewritten, contextually clear question that aligns with the schema and retains the original meaning, if question was not valid then simple return empty string"
            'clarification' : "if invalid then ask the user for clarification otherwise return empty string" 
        }}
        """



class GeneratorAgent(Agent):
    
    def run(self, input_data: dict) -> dict:
        """
        takes question and returns sql query
        
        input_data = {
            'valid' : "0" or "1",
            'question' : 'rewritten question if valid question was asked other wise return empty string',
            'clarification' : "if invalid then ask the user for clarification otherwise return empty string" 
        }
        """
        return super().run(input_data)
        
    
    def get_prompt(self, values):
        return f"""
        You are a PostgreSQL expert. Generate a valid PostgreSQL query based on the provided context.

        === Database Schema (Tables and Columns)
        {self.information}

        === Response Guidelines:
        - **Favor correctness over conservatism**: Optimize the query, but do not avoid execution risks even if it's computationally expensive.
        - **Take risks**: If a complex query is possible, generate it, even if it involves multiple joins, subqueries, window functions, or CTEs.
        - **Handle ambiguity intelligently**: If the question is unclear, make reasonable assumptions and mention them in the explanation.
        - **    Follow best SQL practices**:
        - Use table aliases for readability.
        - Optimize WHERE conditions where applicable.
        - Use joins, subqueries, window functions, and CTEs as necessary.
        - **Ensure the query is well-formatted and syntactically valid**.
        - Always return a structured JSON response in the format below.

        === User Question:
        {values['question']}
        
        === Response Format:
        {{  
            "question": "User Question",
            "query": "Generated SQL query or null if impossible",
            "explanation": "Detailed reasoning behind the generated query",
        }}
        """



    

class ValidatorAgent(Agent):
    """Agent for validating and correcting SQL queries."""

    def run(self, input_data: dict) -> dict:
        """
        input_data = {
            'question' :, 
            'query' : ,
            'explanation' : ,
        }
        """
        return super().run(input_data)

    def get_prompt(self, values):
        return f"""
        You are a PostgreSQL validator. Your task is to analyze a generated SQL query, check its correctness, and provide feedback.

        === Database Schema (Tables and Columns)
        {self.information}

        === Response Guidelines:
        - **Validate syntax**: Ensure the query is syntactically correct for PostgreSQL.
        - **Check for logical correctness**:
        - Does the query align with the user question?
        - Are the selected tables and joins appropriate?
        - Does the query use valid column references?
        - **Performance considerations**:
        - Identify potential inefficiencies (e.g., unnecessary subqueries, missing indexes).
        - Suggest optimizations where applicable.
        - **Handle edge cases**:
        - If the query could fail under certain data conditions, explain why.
        - If the query is incorrect, suggest a corrected version.
        - Always return a structured JSON response in the format below.
    
        === User Question:
        {values['question']}

        === Generated Query for Validation:
        {values['query']}
        
        === Generated Explanation 
        {values['explanation']}

        === Response Format:
        {{  
            "question": "User question",
            "query": "Revised query if the original is incorrect or Original generated SQL query if orignal is correct",
            "explanation": "Detailed reasoning for validation results",
        }}
        """

