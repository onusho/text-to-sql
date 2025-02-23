from flask import Flask, render_template, request, jsonify
from backend.database import Database
from backend.agents import RewriterAgent, GeneratorAgent, ValidatorAgent

app = Flask(__name__)

database = Database()
rewriter = RewriterAgent()
generator = GeneratorAgent()
validator = ValidatorAgent()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_question = data.get('question', '')
    rewriter_response = rewriter.run({'question': user_question})

    if int(rewriter_response['valid']) == 0:
        return jsonify({'clarification': rewriter_response['clarification'], 'query': None, 'result': None})

    generator_response = generator.run(rewriter_response)
    validator_response = validator.run(generator_response)
    query = validator_response['query']
    result_df = database.get_data(query)

    result_html = result_df.to_html(classes='table table-striped table-bordered', index=False) if result_df is not None else "No results found."

    return jsonify({
        'clarification': '',
        'query': query,
        'result': result_html
    })


if __name__ == "__main__":
    app.run(debug=True)
