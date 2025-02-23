# Text-to-SQL 

A Flask-based web application that allows users to interact with the Paglia database on PostgreSQL using natural language queries based on AI agents to rewrite user questions, generate SQL queries, validate them, and display the results in a modern, chat-like interface. 

## Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/your-username/text-to-sql.git
cd text-to-sql
```

2. **Create and Activate a Virtual Environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables:** Create a `.env` file in the project root and add your Google Gemini API key:

```env
API_KEY=your_google_gemini_api_key
```

5. **Set up and Configure the Database:** Ensure PostgreSQL is running locally with the following credentials:

```bash
git clone https://github.com/devrimgunduz/pagila.git
docker-compose up
docker exec -it pagila psql -U postgres
```
- Host: localhost
- Port: 5432
- Database: postgres
- User: postgres
- Password: 123456

Modify `backend/database.py` if your configuration differs.

6. **Run the Application:**
```bash
cd app
python app.py
```

7. **Access the Web Interface:** Open a browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Development Process

1. Researched Existing Methods
2. *Metadata Generation* by extracting database metadata from PostgreSQL, and also fed that along with image diagram to Gemini to create descriptive data about tables, columns and their relationships.
3. *Data Retrieval* by creating a `Database` class that can connect and retrieve queries as Pandas Dataframes.
4. *Experimented with different approaches*, evaluated results and and settled on Agents.
5. Built *Custom AI Agents* for different aspects of query generation
   - *Rewriter Agent*: will check if the question makes sense and ask for clarifications, if it does then will generate a transformed detailed question that generator uses.
   - *Generator Agent*: uses rewritten question to transform into queries, and can take risks by creating long complex queries.
   - *Validator Agent*: checks for correctness of the generated query and optimizes.
6. Created a Flask based simple *Web App* that can be used to interact with the databse.
7. Evaluated all *evalution* questions and stored them in `.\evaluation_report.csv`

## Application Workflow

1. **Rewriting:** The RewriterAgent refines the user query for better SQL alignment and asks for clarification if needed.
2. **Generation:** The GeneratorAgent converts the refined query into a SQL statement.
3. **Validation:** The ValidatorAgent ensures the SQL query is correct and optimized.
4. **Execution:** The Database class executes the validated SQL query and returns the results.

## Technology Stack

- **Backend:** Flask, PostgreSQL
- **Frontend:** HTML, CSS, JavaScript 
- **AI Integration:** Google Gemini API



## Usage

1. Enter your natural language query in the chat box.
2. If prompted, provide additional clarification.
3. View the generated SQL query and the resulting data table.

## Potential Improvements
- Right now, it only works on Palgia Dataset but it could easily be generalized to work on any dataset, as metadata generation workflow can be automated.
- An additional RAG system could be built to retrieve the most relavant tables using the metadata, instead of relying on giving huge amounts of metadata to Agents in on go, using historical and previous SQL query logs on the database.
- Shorter and better Metadata should be generated, through emperical testing.
- Table Augmented Generation (TAG) can be implemented on top of this after the database is retrieved to give the user insights about the retrieved tables.
