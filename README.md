# Roboprof: Intelligent Agent for University Queries

Roboprof is an intelligent agent designed to answer university course- and student-related questions using a knowledge graph and natural language processing techniques. It can handle queries like, “What is course COMP 474 about?”, “Which topics is Jane competent in?” or “Which courses at Concordia teach deep learning?”

## Initial Setup
- **Poetry Installation**: Ensure Poetry is installed on your computer.
- **Dependency Installation**: After cloning the repo, execute `poetry install` to install dependencies, followed by `poetry shell` to activate the virtual environment.
- **SpaCy Model**: Run `python -m spacy download en_core_web_sm` within your environment to download a lightweight NLP model necessary for named entity disambiguation and Wikidata linking.

## Running the Main Script
Execute `python main.py` to perform the following tasks:
- Start the `fuseki-server`
- Build the knowledge graph with `build_graph`
- Set up the database with `setup_database`
You can also run these tasks individually or in combinations as needed.

## Specific Task Execution
### Set Up Fuseki Server
- Run directly in the terminal as per the SPARQL server setup instructions in this document.
- Alternatively, execute `python main.py fuseki-server`.

### Generate Output Files
**Warning**: The project requires a specific folder structure as outlined in the GitHub repository. Alterations may disrupt functionality.
- Ensure possession of `CATALOG.csv` and `CU_SR_OPEN_DATA_CATALOG.csv` from [Concordia Open Data](https://opendata.concordia.ca/datasets/).
- Execute `python main.py build_graph` to parse data, utilize various builders, merge graphs, and save them in the `output` directory. Expect to see `output/ntriples.ttl` and `output/turtles.ttl`.

### Upload ttl to SPARQL Database
- Confirm that the `fuseki-server` is operational on `localhost:3030`.
- Run `python main.py setup_database` to upload the ttl files.

## Development Tips
- Use `poetry add [package-name]` to install new packages.
- Regularly update this README to reflect changes or enhancements.

## Project Structure Overview
- **Data**: Located in the `data` folder, includes necessary datasets and CSV files like grades and students for creating Student classes and facilitating queries.
- **Content**: Contains course lectures and materials in the `content` folder.
- **Queries**: SPARQL queries and their outputs are stored in `queries` and `queries2` folders for different project parts.
- **Rasa**: Holds all Rasa-related files in the `rasa` folder. Note that models are not checked into git to conserve space.

## Script Descriptions
- **Builders**: `academic_builder.py`, `content_builder.py`, and `course_builder.py` parse various data files and create triples.
- **Graph Builder**: `graph_builder.py` executes the builders, consolidates graphs, and outputs them in multiple formats.
- **Topic Processor**: `topic_processor.py` uses Apache Tika and spaCy for document parsing and entity recognition.
- **Utilities**: `constants.py` and `helpers.py` provide namespace domains and reusable methods, respectively.
- **SPARQL API**: `sparql_api.py` manages connections to the fuseki server.
- **Main**: `main.py` is the entry point, managing server startup, graph construction, and database setup.

## SPARQL Server Setup
### Mac
- Install Apache Jena Fuseki via Homebrew: `brew install fuseki`.
- Verify installation with `fuseki-server --version`.
- Start the server using `fuseki-server` and access it at `http://localhost:3030/`.
- Upload ttl/nt files and execute SPARQL queries through the Fuseki interface.

### Windows
- Download and extract `apache-jena-fuseki-5.0.0-rc1.zip` from the [Apache Jena website](https://jena.apache.org/download/).
- Use Command Prompt to navigate to the extracted folder and verify installation with `fuseki-server.bat --version`.
- Start the server using `fuseki-server.bat` and access it at `http://localhost:3030/`.
- Upload ttl/nt files and execute SPARQL queries through the Fuseki interface.

## Rasa Setup
- Ensure Python version is one of 3.7, 3.8, 3.9, or 3.10.
- Navigate to the `rasa` directory.
- Train the Rasa model with `rasa train`.
- Start the actions server with `rasa run actions`.
- Interact with the trained model using `rasa shell`.