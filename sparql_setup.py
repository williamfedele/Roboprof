import subprocess
import requests
from constants import FUSEKI_BASE_URL, DATASET_NAME

def start_fuseki():
    command = "fuseki-server"
    subprocess.Popen(command, shell=True)

def delete_dataset(dataset_name):
    """
    Deletes a dataset in Apache Jena Fuseki.
    Args:
    dataset_name (str): The name of the dataset to delete.
    """
    admin_url = f"{FUSEKI_BASE_URL}$/datasets/{dataset_name}"
    response = requests.delete(admin_url)
    if response.status_code == 200:
        print(f"Dataset '{dataset_name}' deleted successfully.")
    elif response.status_code == 404:
        print(f"Dataset '{dataset_name}' was already non-existant.")
    else:
        raise Exception(f"Failed to delete dataset '{dataset_name}': {response.status_code} {response.text}")

def create_dataset(dataset_name):
    admin_url = f"{FUSEKI_BASE_URL}$/datasets"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = f'dbName={dataset_name}&dbType=tdb'
    response = requests.post(admin_url, data=data, headers=headers)
    if response.status_code == 200:
        print(f"Dataset '{dataset_name}' created successfully.")
    else:
        raise Exception(f"Failed to create dataset '{dataset_name}': {response.status_code} {response.text}")

def upload_turtle(file_path, dataset_name):
    with open(file_path, 'rb') as file:
        headers = {'Content-Type': 'text/turtle;charset=utf-8'}
        response = requests.post(f'{FUSEKI_BASE_URL}{dataset_name}/data?default', data=file, headers=headers)
        if response.status_code == 200:
            print("Data uploaded successfully!")
        else:
            raise Exception(f"Failed to upload data: {response.status_code} {response.text}")

def replace_dataset(file_path, dataset_name=DATASET_NAME):
    delete_dataset(dataset_name)
    create_dataset(dataset_name)
    upload_turtle(file_path, dataset_name)

# Example usage
#start_fuseki()  # Start Fuseki server if it's not already running
file_path = "./output/turtles.ttl"  # Specify the path to the Turtle file
replace_dataset(file_path)  # Replace the dataset with new data
