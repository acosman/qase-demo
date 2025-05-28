import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
QASE_API_TOKEN = os.getenv("QASE_API_TOKEN")
QASE_API_BASE_URL = "https://api.qase.io/v1"  # This is the standard base URL

if not QASE_API_TOKEN:
    print("Error: QASE_API_TOKEN not found in environment variables.")
    print("Please create a .env file with QASE_API_TOKEN='your_api_key'")
    exit(1)

headers = {
    "Token": QASE_API_TOKEN,
    "Content-Type": "application/json"
}

# --- Example 1: Get all projects ---
def get_projects():
    print("\n--- Fetching Projects ---")
    url = f"{QASE_API_BASE_URL}/project"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        projects_data = response.json()
        if projects_data.get("status") and projects_data["status"] is True:
            print("Successfully fetched projects:")
            for project in projects_data["result"]["entities"]:
                print(f"  - {project['title']} (Code: {project['code']})")
        else:
            print(f"Error fetching projects: {projects_data.get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")

# --- Example 2: Create a simple test case ---
def create_test_case(project_code, title="My New Test Case from VS Code"):
    print(f"\n--- Creating Test Case in Project '{project_code}' ---")
    url = f"{QASE_API_BASE_URL}/case/{project_code}"
    payload = {
        "title": title,
        "description": "This is a test case created via Qase API from VS Code.",
        "suite_id": None,
        "severity": 3,
        "priority": 1,
        "status": 0,
        "steps": [
            {"action": "Step 1: Do something", "expected_result": "Something happens"},
            {"action": "Step 2: Do something else", "expected_result": "Something else happens"}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        test_case_data = response.json()
        if test_case_data.get("status") and test_case_data["status"] is True:
            print(f"Successfully created test case: {test_case_data['result']['id']}")
        else:
            print(f"Error creating test case: {test_case_data.get('error', 'Unknown error')}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")

# --- Main execution ---
if __name__ == "__main__":
    print("Qase test automation script starting...")  # 👈 added line
    get_projects()
    create_test_case("QTD", "Test Case from VS Code")
