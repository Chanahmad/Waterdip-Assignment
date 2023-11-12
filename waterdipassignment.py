from flask import Flask, request, jsonify
app = Flask(__name__)
tasks = []
#Function to generate a unique ID for tasks
def generate_task_id():
    return len(tasks) + 1

#Route to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    if title is None:
        return jsonify({'error': 'Title is required'}), 400

    new_task = {
        'id': generate_task_id(),
        'title': title,
        'completed': False
    }
    tasks.append(new_task)
    return jsonify(new_task)

#Route to list all tasks
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify(tasks)

#Route to get a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

#Route to delete a specific task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Task deleted successfully'})

#Route to edit a specific task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    title = data.get('title')
    completed = data.get('completed')

    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    if title is not None:
        task['title'] = title
    if completed is not None:
        task['completed'] = completed

    return jsonify(task)

#Bulk add multiple tasks
@app.route('/tasks/bulk', methods=['POST'])
def bulk_add_tasks():
    data = request.get_json()
    new_tasks = data.get('tasks')
    if not isinstance(new_tasks, list):
        return jsonify({'error': 'Invalid data format'}), 400

    for task_data in new_tasks:
        title = task_data.get('title')
        if title is not None:
            new_task = {
                'id': generate_task_id(),
                'title': title,
                'completed': False
            }
            tasks.append(new_task)

    return jsonify({'message': 'Bulk tasks added successfully'})

#Bulk delete multiple tasks
@app.route('/tasks/bulk', methods=['DELETE'])
def bulk_delete_tasks():
    data = request.get_json()
    task_ids = data.get('task_ids')
    if not isinstance(task_ids, list):
        return jsonify({'error': 'Invalid data format'}), 400

    global tasks
    tasks = [t for t in tasks if t['id'] not in task_ids]

    return jsonify({'message': 'Bulk tasks deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
