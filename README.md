# Text-to-SQL Application for Paglia Database

A Flask-based web application that allows users to interact with the Paglia database using natural language queries based on AI agents to rewrite user questions, generate SQL queries, validate them, and display the results in a modern, chat-like interface.

## Development Process

1. Researched Existing Methods
2. Metadata Generation
3. Created a Database class that can connect and retrieve queries as Pandas Dataframes.
4. Experimented with a Simple Approach and evaluated results.
5. Built Custom AI Agents for different aspects of query generation
   - Rewriter Agent : will check if the question makes sense and ask for clarifications, if it does then will generate a transformed detailed question that generator uses.
   - Generator Agent : uses rewritten question to transform into queries, and can take risks by creating long complex queries.
   - Validator Agent : checks for correctness of the generated query and optimizes.
   - 

## Application Workflow

1. **Rewriting:** The RewriterAgent refines the user query for better SQL alignment.
2. **Generation:** The GeneratorAgent converts the refined query into a SQL statement.
3. **Validation:** The ValidatorAgent ensures the SQL query is correct and optimized.
4. **Execution:** The Database class executes the validated SQL query and returns the results.

## Technology Stack

- **Backend:** Flask, PostgreSQL
- **Frontend:** HTML, CSS, JavaScript 
- **AI Integration:** Google Gemini API

## Folder Structure

```
root
│
├── backend
│   ├── agents.py
│   ├── database.py
│  
│
├── metadata
│   ├── schema.json
│   ├── schema_metadata.json
│   └── schema_declaration.txt
│
├── templates
│   └── index.html
│
├── app.py
├── README.md
└── .env
```

## Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/your-username/text-to-sql-app.git
cd text-to-sql-app
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

5. **Configure the Database:** Ensure PostgreSQL is running locally with the following credentials:

- Host: localhost
- Port: 5432
- Database: postgres
- User: postgres
- Password: 123456

Modify `backend/database.py` if your configuration differs.

6. **Run the Application:**

```bash
python app.py
```

7. **Access the Web Interface:** Open a browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage

1. Enter your natural language query in the chat box.
2. If prompted, provide additional clarification.
3. View the generated SQL query and the resulting data table.

## Example Query

**Input:** "Show the top 5 products by sales in the last month."

**Output:**

- SQL Query: `SELECT product_name, SUM(sales_amount) AS total_sales FROM sales WHERE sale_date >= CURRENT_DATE - INTERVAL '30 days' GROUP BY product_name ORDER BY total_sales DESC LIMIT 5;`
- Result: Displayed as an interactive table.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

