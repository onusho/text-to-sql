import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from database import *
load_dotenv()

import json
with open("../metadata/scheme_metadata.json", "r") as file:
    schema_metadata = json.dumps(json.load(file))
schema_metadata

with open("../metadata/schema_definition.txt", 'r') as file:
    schema_definition = ""
    for line in file.readlines():
        schema_definition += line
schema_definition

information = schema_metadata + '\n' + schema_definition


def get_client():
    return genai.Client(api_key=os.getenv('API_KEY'))
def get_response(contents, client, model = 'gemini-2.0-flash-001'):
    text = client.models.generate_content(model=model, contents=contents, config={'temperature' : 0}).text
    # first brackets
    return json.loads(text[text.index('{'): text.index('}') + 1]) 
    
def get_prompt(question, metadata = None, definition = None):
    if metadata and definition:
        prompt_template = """
        You are a PostgreSQL expert. Think step by step and generate a valid PostgreSQL query based on the provided information.
        === Tables Metadata 
        {metadata}
        
        === Tables Definition
        {definition}

        === Response Guidelines:
        1. If there's enough information, generate the correct query.  
        2. If they question doesn't make sense then return "null" in "query", .  
        3. If the metadata is insufficient, explain why.  
        4. Use the most relevant table(s).  
        5. Format the query properly before responding.  
        6. Always respond with a valid JSON object in the format below.  

        === Response Format:
        ** If a valid query can be generated:
        {{  
            "question": "original user question",
            "query": "generated sql query answering user question",
            "explanation": "explaining why the query works or doesn't work"
        }}

        === Question:
        {question}
        """
        values = {
            "metadata": metadata,
            "definition": definition,
            "question": question
        }
    else:
        data = metadata if metadata else definition
        prompt_template = """
        You are a PostgreSQL expert. Generate a valid PostgreSQL query based on the provided context.
        === Tables Information 
        {data}
        
        === Response Guidelines:
        1. If there's enough context, generate the correct query.  
        2. If they question doesn't make sense then return "null" in "query", .  
        3. If the metadata is insufficient, explain why.  
        4. Use the most relevant table(s).  
        5. Format the query properly before responding.  
        6. Always respond with a valid JSON object in the format below.  

        === Response Format:
        ** If a valid query can be generated:
        {{  
            "question": "original user question",
            "query": "generated sql query answering user question",
            "explanation": "explaining why the query works or doesn't work"
        }}

        === Question:
        {question}
        """

        values = {
            "data": data,
            "question": question
        }
    return prompt_template.format(**values)
