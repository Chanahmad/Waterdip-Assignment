from flask import Flask, request, jsonify
app = Flask(__name__)
tasks = []
def generate_task_id():
    return len(tasks) + 1

@app.route('/v1/tasks', methods=['POST'])
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

@app.route('/v1/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify(tasks)

@app.route('/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((i for i in tasks if i['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

@app.route('/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [i for i in tasks if i['id'] != task_id]
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/v1/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    title = data.get('title')
    completed = data.get('completed')

    task = next((i for i in tasks if i['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    if title is not None:
        task['title'] = title
    if completed is not None:
        task['completed'] = completed

    return jsonify(task)

@app.route('/v1/tasks/bulk', methods=['POST'])
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

@app.route('/v1/tasks/bulk', methods=['DELETE'])
def bulk_delete_tasks():
    data = request.get_json()
    task_ids = data.get('task_ids')
    if not isinstance(task_ids, list):
        return jsonify({'error': 'Invalid data format'}), 400

    global tasks
    tasks = [i for i in tasks if i['id'] not in task_ids]

    return jsonify({'message': 'Bulk tasks deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
