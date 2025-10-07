# Python Backend Application - API creation using Flask Framework and MongoDB
Your task for the project will be implement an entire backend application by
creating an API using Flask framework and MongoDB.
## Project Instructions
### Model
Task model must have the following attributes:
- createdByUid -> string
- createdByName -> string
- assignedToUid -> string
- assignedToName -> string
- description -> string
- done -> bool
The constructor of this Model must initialize the attribute “done” as false.
### Endpoints:
You will need to implement the following endpoints in your new task view:
- Create task: “/tasks/” -> method: POST
- Get tasks created by the user: “/tasks/createdby/” -> method: GET
- Get tasks assigned to the user: “/tasks/assignedto/” -> method: GET
- Update task: “/tasks/<taskUid>” -> method: PATCH
- Delete task: “/tasks/<taskUid>” -> method: DELETE

### 1. Create Task
Create task must receive a token in the request, task description and
assigned to id.
Ex.
```
{
  "description": "New Task",
  "assignedToUid": "635b561d52c61766f0874c7c"
}
```
The view should check if the token is valid using the function created in
class “validateJWT”
- In case of the function returns 400:<br>
``` 
return jsonify({"error": 'Token is missing in the request, please try again'}), 401
```
- In case of the function returns 401:<br>
```
return jsonify({"error": 'Invalid authentication token, please login again'}), 403
```
- If there is token, verify if the keys description and assignedToUid are inside the
request data. If not:<br>
```
raise ValueError('Error validating form')
```
Inside the task controller, create a new function that will receive the token and
data request. You can take from the token the user that is doing the request, this
user will be the “createdBy” user.<br><br>
Access the Database and you can take the createBy user and assignedTo user,
because the assigned to is inside the request data.<br><br>
When you have all the information you can create a new task by with all the
information, remember, the attribute done is always false on creation.<br><br>
This endpoint must return the id of the task created, the ID we will use the one
created by MONGO.
```
return jsonify({'id': str(createdTask.inserted_id)})
```
Please, put your code inside try / except:
```
except ValueError as err:
        return jsonify({"error": str(err)}), 400
```
### 2. Get Tasks Created By User
Get tasks created by the user, you will return all the tasks created by the
user that is doing the request.<br><br>
To do that, you will need to validate if the token is in the request by using the
function validadeJWT:
- In case of the function returns 400:
```
return jsonify({"error": 'Token is missing in the request, please try again'}), 401
```
- In case of the function returns 401:
```
return jsonify({"error": 'Invalid authentication token, please login again'}), 403
```
Your endpoint must return a list of tasks that were created by the user, you can
access the user from the token information.<br>
 
Please, put your code inside try / except.

**Example of output: Imagine that the user Daniel is trying to check all the tasks he
created:**
```
[
    {
        "assignedToName": "testUser",
        "assignedToUid": "635b560052c61766f0874c7a",
        "createdByName": "daniel",
        "createdByUid": "635b561d52c61766f0874c7c",
        "description": "daniel task",
        "done": true,
        "taskUid": "635b567452c61766f0874c7d"
    },
    {
        "assignedToName": "daniel",
        "assignedToUid": "635b561d52c61766f0874c7c",
        "createdByName": "daniel",
        "createdByUid": "635b561d52c61766f0874c7c",
        "description": "testUser task",
        "done": false,
        "taskUid": "635e12f85ae9e534bb0a99d5"
    }
]
```
Please, respect those keys when you create the output.

### 3. Get Tasks Assigned to User
Get tasks assigned to the user, you will return all the tasks assigned to the
user that is doing the request.<br><br>
To do that, you will need to validate if the token is in the request by using the
function validadeJWT:<br>
- In case of the function returns 400:
```
return jsonify({"error": 'Token is missing in the request, please try again'}), 401
```
- In case of the function returns 401:
```
return jsonify({"error": 'Invalid authentication token, please login again'}), 403
```
Your endpoint must return a list of tasks that were created by the user, you can
access the user from the token information.

Please, put your code inside try/except.

**Example of output: Imagine that the user Daniel is trying to check all the tasks he
has been assigned to:**
```
[
    {
        "assignedToName": "daniel",
        "assignedToUid": "635b561d52c61766f0874c7c",
        "createdByName": "daniel",
        "createdByUid": "635b561d52c61766f0874c7c",
        "description": "testUser task",
        "done": false,
        "taskUid": "635e12f85ae9e534bb0a99d5"
    }
]
```
Please, respect those keys when you create the output.

### 4. Update Task
Update a task will have a small restriction: only the user that is assigned to
that task will be able to update the task.<br><br>
You can check the user from the token, you will need to validate if the request has
token using the function validadeJWT:<br>
- In case of the function returns 400:
```
return jsonify({"error": 'Token is missing in the request, please try again'}), 401
```
- In case of the function returns 401:
```
return jsonify({"error": 'Invalid authentication token, please login again'}), 403
```
You will need to check if inside the data request there is the key “done”.<br><br>
In case of task is not in the body:
```
return jsonify({"error": 'Status done not found in the request'}), 400
```
In your endpoint, you can add a parameter that will be the taskUid:
```
@task.route("/tasks/<taskUid>", methods=["PATCH"])
def updateTask(taskUid):
```
This will allow you to take information from the url of the request so you will be able to access the taskUid that needs to be updated from the
variable taskUid.<br><br>
If you try to find the task inside the dabase and you cant find it:
```
raise Exception('Task not found')
```
You will need to check if the assignedToUid for that task inside the database is the
same of the user Uid that is doing the request, if not you should pop the error:
```
raise Exception('Users can only change status when task is assigned to them.')
```
Always put the code of your controller inside try/except.

### 5. Delete Task
Delete a task will have a small restriction: only the user that created that
task will be able to delete it.<br><br>
You can check the user from the token, you will need to validate if the request has
token using the function validadeJWT:
- In case of the function returns 400:
```
return jsonify({"error": 'Token is missing in the request, please try again'}), 401
```
- In case of the function returns 401:
```
return jsonify({"error": 'Invalid authentication token, please login again'}), 403
```
Your delete endpoint will work exactly as the update, the taskUid will be sent inthe
request URL:
```
@task.route("/v1/tasks/<taskUid>", methods=["DELETE"])
def deleteTask(taskUid):
```
You will need to check if the createdByUid for that task inside the database is the
same of the user Uid that is doing the request, if not you should pop the error:
```
raise Exception('Users can only delete when task is created by them.')
```
Always put the code of your controlled inside try/except.

In case of the deletion is succeed, return the amount of tasks affected:
```
{
    "tasksAffected": 1
}
```
You can take this information from the Mongo response when you delete the
task:
```
return jsonify({'tasksAffected': taskDeleteAttempt.deleted_count}), 200
```
