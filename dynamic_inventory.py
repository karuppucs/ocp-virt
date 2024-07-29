import requests
import json

# Replace these with appropriate values
TOWER_HOST = ""
TOWER_USERNAME = ""
TOWER_PASSWORD = ""
JOB_ID = "job-id-of-fetch-inventory"

def get_job_output(job_id):
    url = f"{TOWER_HOST}/api/v2/jobs/{job_id}/job_events/"
    response = requests.get(url, auth=(TOWER_USERNAME, TOWER_PASSWORD))
    response.raise_for_status()
    return response.json()

def extract_vm_names(job_output):
    vm_names = []
    for event in job_output['results']:
        if 'task' in event and event['task'] == 'Extract VM names':
            vm_names = event['event_data']['res']['ansible_facts']['vm_names']
            break
    return vm_names

def update_inventory(vm_names):
    inventory_data = {
        "all": {
            "hosts": vm_names
        }
    }
    with open('/path/to/dynamic_inventory.json', 'w') as f:
        json.dump(inventory_data, f)

def main():
    job_output = get_job_output(JOB_ID)
    vm_names = extract_vm_names(job_output)
    update_inventory(vm_names)

if __name__ == "__main__":
    main()
