from flask import Blueprint, jsonify, request
from controllers.task_controller import create_task, get_tasks_by_user, get_assigned_tasks, update_tasks, delete_task
from helpers.token_validation import validate_jwt
from models.task_model import Task

task = Blueprint("task", __name__)


@task.route('/tasks/', methods=['POST'])
def add_task():
    try:
        my_body = request.json
        token = validate_jwt()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 403
        
        if 'description' not in my_body:
            raise ValueError('Error validating form')
        if 'assignedToUid' not in my_body:
            raise ValueError('Error validating form')
        
        my_task = Task( createdByUid = "", createdByName="", assignedToUid = my_body["assignedToUid"], assignedToName= "", description = my_body["description"])
        
        createdTask = create_task(my_task, token)

        if not createdTask.inserted_id:
            return jsonify({'error': 'Something wrong happened when creating task!'}), 500
        
        return jsonify({"id": str(createdTask.inserted_id)})
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    
@task.route('/tasks/createdby/', methods=['GET'])
def get_task_by_user():
    try:
        token = validate_jwt()
        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 403
        return get_tasks_by_user(token)
    except:
        return jsonify({'error': 'Something wrong happened when getting all tasks'}), 500
    
@task.route('/tasks/assignedto/',  methods=['GET'])
def get_tasks_assigned_to_user():
    try:
        token = validate_jwt()
        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 403
        return get_assigned_tasks(token)
    except:
        return jsonify({'error': 'Something wrong happened when getting all tasks!'}), 500

@task.route('/tasks/<taskUid>', methods=["PATCH"])
def update_task(taskUid):
    try:
        token = validate_jwt()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 403
        if 'done' not in request.json:
            return jsonify({"error": 'Status "done" not found in the request'}), 400
        if not taskUid:
            raise Exception('Task not Found')
              
        done = request.json["done"]

        if done not in [True, False]:
            return jsonify({"error": 'Status done must be True or False'}), 400

        update_tasks(taskUid, token, done)
        
        return jsonify ({"taskUid": str(taskUid)})
    except Exception as err:
        return jsonify({"error": str(err)}), 400
    
@task.route('/v1/tasks/<taskUid>', methods=["DELETE"])
def deleteTask(taskUid):
    try:
        token = validate_jwt()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 403
        if not taskUid:
            raise Exception('Task not Found')
              
        taskDeleteAttempt = delete_task(taskUid, token)

        return jsonify({'tasksAffected': taskDeleteAttempt}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 400