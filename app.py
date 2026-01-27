import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# FILE PATH: This is where we will store our data
DB_FILE = 'tasks.json'

# --- HELPER FUNCTIONS (To keep code clean) ---

def load_tasks_from_file():
    """
    Reads the list of tasks from the JSON file.
    If the file doesn't exist, it returns an empty list.
    """
    if not os.path.exists(DB_FILE):
        return []  # Return empty list if file is new
    
    try:
        with open(DB_FILE, 'r') as file:
            data = json.load(file)
            return data
    except (json.JSONDecodeError, ValueError):
        # If file is corrupt or empty, return empty list to avoid crash
        return []

def save_tasks_to_file(tasks):
    """
    Writes the list of tasks back to the JSON file.
    """
    with open(DB_FILE, 'w') as file:
        json.dump(tasks, file, indent=4) # indent=4 makes the file readable for humans

# --- ROUTES (The API Endpoints) ---

@app.route('/')
def home():
    """
    Serves the frontend HTML page.
    """
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    API: Returns all tasks to the frontend.
    """
    tasks = load_tasks_from_file()
    return jsonify(tasks)

@app.route('/add-task', methods=['POST'])
def add_task():
    """
    API: Receives a new task and saves it.
    Expects JSON data: { "task": "Your task name" }
    """
    # 1. Get the data sent from Frontend
    data = request.get_json()
    new_task_text = data.get('task')

    # 2. Validation: Ensure user actually typed something
    if not new_task_text:
        return jsonify({"error": "Task cannot be empty"}), 400

    # 3. Load existing tasks
    current_tasks = load_tasks_from_file()

    # 4. Add new task (We create a simple dictionary object)
    # We add an ID to make it easier to track (optional but good practice)
    new_task = {
        "id": len(current_tasks) + 1,
        "text": new_task_text,
        "completed": False
    }
    current_tasks.append(new_task)

    # 5. Save back to file
    save_tasks_to_file(current_tasks)

    return jsonify({"message": "Task added successfully!", "task": new_task})

# --- RUN SERVER ---
if __name__ == '__main__':
    # debug=True allows the server to auto-reload when you change code
    app.run(debug=True)