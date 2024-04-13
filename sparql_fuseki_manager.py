from constants import FUSEKI_BASE_URL, DATASET_NAME
import requests

# This class is a singleton class that manages the Apache Fuseki server
class FusekiManager:
    _instance = None

    def __new__(cls, base_url=FUSEKI_BASE_URL, dataset_name=DATASET_NAME):
        if not cls._instance:
            cls._instance = super(FusekiManager, cls).__new__(cls)
            # Initialization only if the instance is not already created
            cls._instance.base_url = base_url
            cls._instance.dataset_name = dataset_name
        return cls._instance

    def delete_dataset(self):
        admin_url = f"{self.base_url}$/datasets/{self.dataset_name}"
        response = requests.delete(admin_url)
        if response.status_code == 200:
            print(f"Dataset '{self.dataset_name}' deleted successfully.")
        elif response.status_code == 404:
            print(f"Dataset '{self.dataset_name}' was already non-existent.")
        else:
            raise Exception(f"Failed to delete dataset '{self.dataset_name}': {response.status_code} {response.text}")

    def create_dataset(self):
        admin_url = f"{self.base_url}$/datasets"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'dbName={self.dataset_name}&dbType=tdb'
        response = requests.post(admin_url, data=data, headers=headers)
        if response.status_code == 200:
            print(f"Dataset '{self.dataset_name}' created successfully.")
        else:
            raise Exception(f"Failed to create dataset '{self.dataset_name}': {response.status_code} {response.text}")

    def upload_turtle(self, file_path):
        with open(file_path, 'rb') as file:
            headers = {'Content-Type': 'text/turtle;charset=utf-8'}
            response = requests.post(f'{self.base_url}{self.dataset_name}/data?default', data=file, headers=headers)
            if response.status_code == 200:
                print("Data uploaded successfully!")
            else:
                raise Exception(f"Failed to upload data: {response.status_code} {response.text}")

    def setup_new_database(self, file_path="./output/turtles.ttl"):
        self.delete_dataset()
        self.create_dataset()
        self.upload_turtle(file_path)

    def query(self, sparql_query, prefixes=""):
        full_query = prefixes + sparql_query
        print("now really querying...")
        response = requests.get(f"{self.base_url}{self.dataset_name}/query", params={'query': full_query})
        print("response status:", response.status_code)
        return response

