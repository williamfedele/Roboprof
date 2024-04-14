import sys
import subprocess
import time
from graph_builder import build_graph
from sparql_fuseki_manager import FusekiManager


def start_fuseki():
    print("Starting Fuseki server...")
    command = "fuseki-server"
    subprocess.Popen(command, shell=True)
    seconds_to_wait = 20
    print(f"Waiting {seconds_to_wait} seconds until server is ready...")
    time.sleep(seconds_to_wait)


def build_graph_wrapper():
    print("Building graph...")
    build_graph()


def setup_database():
    print("Setting up new database...")
    fm = FusekiManager()
    fm.setup_new_database()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if "start_fuseki" in sys.argv:
            start_fuseki()
        if "build_graph" in sys.argv:
            build_graph_wrapper()
        if "setup_database" in sys.argv:
            setup_database()
    else:
        print("No command-line arguments provided. Running only the graph upload to the database")
        setup_database()
