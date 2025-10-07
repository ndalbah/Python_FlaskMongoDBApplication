from flask import jsonify
from database.__init__ import database
from helpers.token_validation import validate_jwt
import app_config as config
from bson.objectid import ObjectId



def create_task(task, user_info):
    try:
        #Created by User 
        user_id = user_info["id"]
        user_name = user_info["name"]

        #Assigned to User Name
        collection = database.database[config.CONST_USER_COLLECTION]
        assigned_user = collection.find_one({'_id': ObjectId(task.assignedToUid)})

        if assigned_user is None:
            raise ValueError(f"No user found with ID: {task.assignedToUid}") 
        
        assigned_user_name = assigned_user["name"]


        task.createdByUid = user_id.lower()
        task.createdByName = user_name.lower()
        task.assignedToUid = task.assignedToUid.lower()
        task.assignedToName = assigned_user_name.lower()
        task.description = task.description.lower()

        print(task.__dict__)

        collection = database.database[config.CONST_TASK_COLLECTION]
        return collection.insert_one(task.__dict__)
    except:
        raise Exception("Error on creating task!")
    
def get_tasks_by_user(user_info):
    try:
        collection = database.database[config.CONST_TASK_COLLECTION]
        user_id = user_info["id"]

        tasks = []
        
        for task in collection.find({'createdByUid': user_id.lower()}):
            current_task = {
                'assignedToName': task['assignedToName'],
                'assignedToUid': task['assignedToUid'],
                'createdByName': task['createdByName'],
                'createdByUid': task['createdByUid'],
                'description': task['description'],
                'done': task['done']
            }
            tasks.append(current_task)
            return jsonify({'tasks': tasks})
    except:
        raise Exception("Error on fetching task!")

def get_assigned_tasks(user_info):
    try:
        collection = database.database[config.CONST_TASK_COLLECTION]
        user_id = user_info["id"]

        tasks = []
        
        for task in collection.find({'assignedToUid': user_id.lower()}):
            current_task = {
                'assignedToName': task['assignedToName'],
                'assignedToUid': task['assignedToUid'],
                'createdByName': task['createdByName'],
                'createdByUid': task['createdByUid'],
                'description': task['description'],
                'done': task['done']
            }
            tasks.append(current_task)
            return jsonify({'tasks': tasks})
    except:
        raise Exception("Error on fetching task!")

def update_tasks(task_id, user_info, done):
    try:
        taskCollection = database.database[config.CONST_TASK_COLLECTION]
        user_id = user_info["id"]
        task_to_update = taskCollection.find_one({"_id": ObjectId(task_id)})

        if user_id != str(task_to_update["assignedToUid"]):
            raise Exception("You are not authorized to update this task")
        
        result = taskCollection.update_one({"_id": ObjectId(task_id)}, {"$set": {"done": done}})

        if result.modified_count == 0:
            raise Exception("No updates were made")
        
        return {"taskUid": str(task_id), "done": done}
    except Exception as err:
        raise Exception(f"Failed to update task: {err}")


def delete_task(task_id, user_info):
    try:
        taskCollection = database.database[config.CONST_TASK_COLLECTION]
        user_id = user_info["id"]
        task_to_delete = taskCollection.find_one({"_id": ObjectId(task_id)})

        if user_id != str(task_to_delete["createdByUid"]):
            raise Exception("You are not authorized to delete this task")
        
        result = taskCollection.delete_one({"_id": ObjectId(task_id)})

        if result.deleted_count == 0:
            raise Exception("No task was deleted")
        
        return result.deleted_count
    except Exception as err:
        raise Exception(f"Failed to delete task: {err}")