import requests
import random
import time

BASE_URL = "http://host.docker.internal:3002"

ROLES = ["MANAGER", "SPECIALIST", "TRAINER"]
DEPARTMENTS = ["FINAINC", "BUSINESS", "HR"]
GENDERS = ["MALE", "FEMALE"]

TASK_TITLES = [
    "Prepare financial report", "Review business case", "Train new employees",
    "Conduct payroll audit", "Analyze budget variance", "Onboard new HR staff",
    "Schedule training session", "Update internal policies", "Evaluate team performance"
]

TASK_DESCRIPTIONS = [
    "Task must be completed before the quarterly review.",
    "Coordinate with other departments for execution.",
    "Part of internal optimization project.",
    "Urgent task requested by upper management.",
    "Support ongoing strategic initiatives."
]

PRIORITIES = ["LOW", "MEDIUM", "HIGH"]
STATUSES = ["PENDING", "IN_PROGRESS", "COMPLETED"]
USERNAMES = ['waleed', 'mohammed', 'moayed', 'dahom']

NUM_USERS = 5
TASKS_PER_USER = 4


def register_user(index):
    email = f"user{index}@example.com"
    username = f"user{index}"
    payload = {
        "email": email,
        "password": "asd123",
        "full_name": f"User {index}",
        "username": username,
        "gender": random.choice(GENDERS),
        "department": random.choice(DEPARTMENTS),
        "role": random.choice(ROLES)
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print(f"[User {index}] Register:", response.status_code)
    return username


def login_user(username):
    payload = {
        "username": username,
        "password": "asd123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print(f"[{username}] Login:", response.status_code)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def create_task(token, user_index, task_index):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "title": random.choice(TASK_TITLES),
        "desription": random.choice(TASK_DESCRIPTIONS),
        "priority": random.choice(PRIORITIES),
        "status": random.choice(STATUSES)
    }
    response = requests.post(f"{BASE_URL}/task", json=payload, headers=headers)
    print(f"[User {user_index}] Task {task_index}: {response.status_code}")


def main():
    for i in range(1, NUM_USERS + 1):
        username = register_user(i)
        token = login_user(username)
        if token:
            for t in range(1, TASKS_PER_USER + 1):
                create_task(token, i, t)
                time.sleep(0.3)
        else:
            print(f"❌ Login failed for user {username}")


if __name__ == "__main__":
    main()
