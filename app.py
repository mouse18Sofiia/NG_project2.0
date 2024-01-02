# app.py
from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

novels_path = 'templates/novels'
novels = {}

# Load all JSON novels
for novel_file in os.listdir(novels_path):
    if novel_file.endswith('.json'):
        with open(os.path.join(novels_path, novel_file), 'r', encoding='utf-8') as file:
            novel_data = json.load(file)
            novels[novel_file[:-5]] = novel_data

current_novel = None

@app.route('/')
def index():
    return render_template('index.html', novels=novels)

@app.route('/choose_novel/<novel_name>')
def choose_novel(novel_name):
    global current_novel
    current_novel = novel_name
    return render_template('novel.html', step=novels[current_novel]['start'], current_novel=current_novel)

@app.route('/make_choice', methods=['POST'])
def make_choice():
    global current_novel
    choice = request.json['choice']
    next_step_key = novels[current_novel].get(choice, None)

    if next_step_key:
        next_step = novels[current_novel][next_step_key]
        return jsonify({"step": next_step})
    else:
        return jsonify({"step": None})

if __name__ == '__main__':
    app.run(debug=True)