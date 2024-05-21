#!/usr/bin/python3
import requests
import sys

def get_employee_todo_progress(employee_id):
    """
    Fetches and displays the TODO list progress of an employee given their ID.

    Args:
        employee_id (int): The ID of the employee.

    The function will output the employee's name and the number of completed tasks
    along with the total number of tasks. It will also list the titles of the completed tasks.
    """
    # Base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Fetch employee data
    user_url = f"{base_url}/users/{employee_id}"
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print("Error: Unable to fetch user data.")
        return
    
    user_data = user_response.json()
    employee_name = user_data.get("name")

    # Fetch TODO list for the employee
    todos_url = f"{base_url}/todos?userId={employee_id}"
    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print("Error: Unable to fetch TODO list data.")
        return

    todos = todos_response.json()

    # Calculate the number of completed and total tasks
    total_tasks = len(todos)
    done_tasks = [task for task in todos if task.get("completed")]
    number_of_done_tasks = len(done_tasks)

    # Print the TODO list progress
    print(f"Employee {employee_name} is done with tasks({number_of_done_tasks}/{total_tasks}):")
    for task in done_tasks:
        print(f"\t {task.get('title')}")

if __name__ == "__main__":
    """
    Main entry point of the script. Expects one command-line argument: the employee ID.
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Error: Employee ID must be an integer.")
        sys.exit(1)

    get_employee_todo_progress(employee_id)
