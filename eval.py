import json
from datetime import datetime

employee_data = "org_database/employee.json"
manager_data = "org_database/manager.json"
office_staff_data = "org_database/office_staff.json"


def load_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def punch(user_id, action):
    time = get_current_time()
    user_data = load_data(employee_data)
    user = next((emp for emp in user_data if emp["id"] == user_id), None)
    if user:
        if action == "punch_in":
            user["punch_logs"].append(f"Punched in at {time}")
        elif action == "punch_out":
            user["punch_logs"].append(f"Punched out at {time}")
        save_data(employee_data, user_data)
    else:
        print("User not found!")


def approve_leave_request(office_staff_id):
    manager = load_data(manager_data)
    office_staff = load_data(office_staff_data)
    leave_request = [r for r in office_staff if r["id"] == office_staff_id][0]
    manager["leave_requests"].append(leave_request)
    save_data(manager_data, manager)




def assign_task(office_staff_id, task):
    manager = load_data(manager_data)
    office_staff = load_data(office_staff_data)
    office_staff_user = next((o for o in office_staff if o["id"] == office_staff_id), None)
    if office_staff_user:
        office_staff_user["tasks"].append(task)
        manager["assigned_tasks"].append({"user_id": office_staff_id, "task": task})
        save_data(office_staff_data, office_staff)
        save_data(manager_data, manager)
    else:
        print("Office staff not found!")


def complete_task(office_staff_id, task_index):
    office_staff = load_data(office_staff_data)

    if 0 <= task_index < len(office_staff[office_staff_id]["tasks"]):
        for search in office_staff:
            if(office_staff_id == search['id']):
                del search['tasks'][task_index]
                save_data(office_staff_data, office_staff)


def view_punch(id):
    employee = load_data(employee_data)
    for search in employee:
        if(id == search["id"]):
            print(search['punch_logs'])


def apply_leave(office_staff_id, leave_request):
    office_staff = load_data(office_staff_data)
    office_staff_user = next((o for o in office_staff if o["id"] == office_staff_id), None)
    if office_staff_user:
        office_staff_user["leave_requests"].append(leave_request)
        save_data(office_staff_data, office_staff)
    else:
        print("Office staff not found!")


def display_emp(id):
    print(f"Welcome Employee id:{id}")
    print("What would you like to do today")
    print("1. Punch in \n 2. Punch out \n 3. Exit")
    action = int(input(">> "))
    if(action == 1):

        punch(id,"punch_in")
    elif(action == 2):
        punch(id, "punch_out")
    else:
        pass


def display_man():
    print("Welcome Manager")
    print("What would you like to do today")
    print("1. Approve Leave request \n 2. Assign task \n 3. View Punch log \n 4. Exit")
    actions= int(input(">> "))
    print(type(actions))
    if(actions == 1):
        staff = int(input("Enter the office staff id: "))
        approve_leave_request(staff)
    elif(actions == 2):
        staff = int(input("Enter the office staff id: "))
        task = input("Enter the task: ")
        assign_task(staff, task)
    elif(actions == 3):
        emp = int(input("Enter the employee id: "))
        view_punch(emp)


def display_staff(id):
    print(f"Welcome Staff id: {id}")
    print("What would you like to do today")
    print("1. Request for leave  \n 2. Complete task \n 3. Exit")
    action = input(">> ")
    if(action == 1):
        reason = input("Reason for leave: ")
        apply_leave(id, reason)
    elif action == 2:
        complete_task(id, 0)


if __name__ == "__main__":
    display_man()
    employee = load_data(employee_data)
    staffs = load_data(office_staff_data)
    managers = load_data(manager_data)
    print("Welcome to organisation")
    print("What do you want to login as?")
    print("1. Employee")
    print("2. Manager")
    print(("3. Office Staff"))

    choice = int(input(">> "))

    if(choice == 1):
        print("Employee Login")
        id = int(input("ID: "))
        password = input("Password")
        for emp in  employee:
            if(id == emp['id'] and password == emp['password']):
                display_emp(id)
    elif(choice == 2):
        print("Manager Login")
        password = input("Password")

        if(password == managers["password"]):
            display_man()
    elif(choice == 3):
        print("Office Staff Login")
        id = int(input("ID: "))
        password = input("Password: ")
        for staff in staffs:
            if(id == staff['id'] and password == staff['password']):
                display_staff(id)
