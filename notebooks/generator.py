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
with open('../metadata/summary.txt', 'r') as file:
    summary = ""
    for line in file.readlines():
        summary += line 
# summary = """
# 1️⃣ actor
# Description: Stores information about movie actors.
# Columns:
# actor_id (PK) - Unique identifier for each actor.
# first_name - Actor's first name.
# last_name - Actor's last name.
# last_update - Timestamp of the last update.
# Relationships:
# Many-to-Many with film via film_actor.
# 2️⃣ address
# Description: Stores customer and staff addresses.
# Columns:
# address_id (PK) - Unique identifier.
# address - Street address.
# address2 - Additional street address.
# district - District name.
# city_id (FK) - Links to city.city_id.
# postal_code - ZIP/postal code.
# phone - Contact number.
# last_update - Timestamp of last update.
# Relationships:
# Many-to-One with city (via city_id).
# One-to-Many with customer and staff.
# 3️⃣ category
# Description: Stores movie categories.
# Columns:
# category_id (PK) - Unique identifier.
# name - Category name.
# last_update - Timestamp of last update.
# Relationships:
# Many-to-Many with film via film_category.
# 4️⃣ city
# Description: Stores city information.
# Columns:
# city_id (PK) - Unique identifier.
# city - City name.
# country_id (FK) - Links to country.country_id.
# last_update - Timestamp of last update.
# Relationships:
# Many-to-One with country.
# One-to-Many with address.
# 5️⃣ country
# Description: Stores country names.
# Columns:
# country_id (PK) - Unique identifier.
# country - Country name.
# last_update - Timestamp of last update.
# Relationships:
# One-to-Many with city.
# 6️⃣ customer
# Description: Stores customer details.
# Columns:
# customer_id (PK) - Unique identifier.
# store_id (FK) - Links to store.store_id.
# first_name - Customer's first name.
# last_name - Customer's last name.
# email - Contact email.
# address_id (FK) - Links to address.address_id.
# activebool - Indicates if the customer is active.
# create_date - Date of customer creation.
# last_update - Timestamp of last update.
# active - Active status flag.
# Relationships:
# Many-to-One with store.
# Many-to-One with address.
# One-to-Many with rental.
# 7️⃣ film
# Description: Stores information about movies.
# Columns:
# film_id (PK) - Unique identifier.
# title - Movie title.
# description - Short description.
# release_year - Year of release.
# language_id (FK) - Links to language.language_id.
# original_language_id (FK) - Optional, links to language.language_id.
# rental_duration - Number of days a rental lasts.
# rental_rate - Cost per rental.
# length - Movie duration in minutes.
# replacement_cost - Cost of replacing the movie.
# rating - Movie rating (e.g., PG, R).
# special_features - Special features available.
# last_update - Timestamp of last update.
# Relationships:
# Many-to-Many with actor via film_actor.
# Many-to-Many with category via film_category.
# Many-to-One with language.
# One-to-Many with inventory.
# 8️⃣ film_actor
# Description: Links actors and films.
# Columns:
# actor_id (FK) - Links to actor.actor_id.
# film_id (FK) - Links to film.film_id.
# last_update - Timestamp of last update.
# Relationships:
# Many-to-Many bridge table between actor and film.
# 9️⃣ film_category
# Description: Links films and categories.
# Columns:
# film_id (FK) - Links to film.film_id.
# category_id (FK) - Links to category.category_id.
# last_update - Timestamp of last update.
# Relationships:
# Many-to-Many bridge table between film and category.
# 🔟 inventory
# Description: Represents copies of films available for rental.
# Columns:
# inventory_id (PK) - Unique identifier.
# film_id (FK) - Links to film.film_id.
# store_id (FK) - Links to store.store_id.
# last_update - Timestamp of last update.
# Relationships:
# Many-to-One with film.
# Many-to-One with store.
# One-to-Many with rental.
# 1️⃣1️⃣ language
# Description: Stores film languages.
# Columns:
# language_id (PK) - Unique identifier.
# name - Language name.
# last_update - Timestamp of last update.
# Relationships:
# One-to-Many with film.
# 1️⃣2️⃣ payment
# Description: Stores payment transactions.
# Columns:
# payment_id (PK) - Unique identifier.
# customer_id (FK) - Links to customer.customer_id.
# staff_id (FK) - Links to staff.staff_id.
# rental_id (FK) - Links to rental.rental_id.
# amount - Payment amount.
# payment_date - Date of payment.
# last_update - Timestamp of last update.
# Relationships:
# Many-to-One with customer.
# Many-to-One with staff.
# Many-to-One with rental.
# 1️⃣3️⃣ rental
# Description: Tracks movie rentals.
# Columns:
# rental_id (PK) - Unique identifier.
# rental_date - Date of rental.
# inventory_id (FK) - Links to inventory.inventory_id.
# customer_id (FK) - Links to customer.customer_id.
# return_date - Date of return.
# staff_id (FK) - Links to staff.staff_id.
# last_update - Timestamp of last update.
# Relationships:
# Many-to-One with inventory.
# Many-to-One with customer.
# Many-to-One with staff.
# One-to-Many with payment.
# 1️⃣4️⃣ staff
# Description: Represents store employees.
# Columns:
# staff_id (PK) - Unique identifier.
# first_name, last_name, email, active, etc.
# store_id (FK) - Links to store.store_id.
# address_id (FK) - Links to address.address_id.
# Relationships:
# Many-to-One with store.
# Many-to-One with address.
# 1️⃣5️⃣ store
# Description: Represents rental stores.
# Columns:
# store_id (PK) - Unique identifier.
# manager_staff_id (FK) - Links to staff.staff_id.
# address_id (FK) - Links to address.address_id.
# Relationships:
# One-to-Many with inventory.
# One-to-Many with customer.
# One-to-Many with staff.
# """

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
