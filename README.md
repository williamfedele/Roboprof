# Roboprof Project README

Roboprof is an intelligent agent designed to answer questions related to university courses and students by leveraging a knowledge graph and natural language processing techniques. It can handle queries like, “What is course COMP 474 about?”, “Which topics is Jane competent in?” or “Which courses at Concordia teach deep learning?”

## Getting Started

### Initial Setup
1. Ensure you have Poetry installed on your computer.
2. Clone the repository and navigate to the project directory.
3. Run the following commands to set up the environment:
   ```
   poetry install
   poetry shell
   python -m spacy download en_core_web_sm
   ```

### Main Script Execution
Run the main script using:
```
python main.py
```
This initiates the tasks: `fuseki-server`, `build_graph`, `setup_database`.

### Individual Task Instructions

#### Set up Fuseki Server
- Run the Fuseki server via:
  ```
  python main.py fuseki-server
  ```
  or follow the detailed setup instructions in the SPARQL server setup section below.

#### Generate Graph Output Files
- Ensure correct file structure as specified in the GitHub repository to avoid errors.
- Download `CATALOG.csv` and `CU_SR_OPEN_DATA_CATALOG.csv` from:
  ```
  https://opendata.concordia.ca/datasets/
  ```
- Generate graph output by running:
  ```
  python main.py build_graph
  ```

#### Upload TTL Files to SPARQL Database
- Confirm that the Fuseki server is active at localhost:3030.
- Execute:
  ```
  python main.py setup_database
  ```

#### Running Multiple Tasks
- If ttl files are pre-generated, you can run:
  ```
  python main.py fuseki-server setup_database
  ```

### Development Guidelines
- Add new packages via:
  ```
  poetry add <package_name>
  ```
- Keep this README updated with any significant changes.

## Project Organization

### Directories
- `data`: Holds datasets from Concordia (downloadable [here](https://opendata.concordia.ca/datasets/)), and CSVs for student and course data.
- `content`: Contains lecture materials for selected courses.
- `queries`: Stores SPARQL queries and their results from project part 1.
- `queries2`: Contains additional SPARQL queries for project part 2.
- `rasa`: Includes all Rasa related files for the chatbot implementation.

### Scripts Overview
- `academic_builder.py`: Parses academic-related CSVs and builds RDF triples.
- `content_builder.py`: Parses educational content for RDF graph construction.
- `course_builder.py`: Handles the parsing of Concordia University's course catalogs.
- `graph_builder.py`: Consolidates graphs from various parsers into a unified RDF graph.
- `topic_processor.py`: Implements named entity recognition and linking to Wikidata.
- `constants.py`: Maintains consistent URIs across scripts.
- `helpers.py`: Provides reusable utility functions.
- `sparql_api.py`: Manages connections to the Fuseki SPARQL server.
- `main.py`: Central script initiating the Fuseki server, graph building, and database setup.

### SPARQL Server Setup
Refer to detailed instructions for setting up the SPARQL server on Mac or Windows as specified below in the README.

### Rasa Setup
- Ensure Python version between 3.7 and 3.10.
- Navigate to the `rasa` directory and run:
  ```
  rasa train
  rasa run actions
  rasa shell
  ```
This setup trains the Rasa model, runs the actions server, and opens a shell for interaction.