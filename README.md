# Roboprof README

**Roboprof** is an intelligent agent designed to answer university course- and student-related questions using a knowledge graph and natural language processing technology. Roboprof can help provide insights into course details, student competencies, and course content across various academic subjects.

For instance, Roboprof can respond to queries like:
- "What is course COMP 474 about?"
- "Which topics is Jane competent in?"
- "Which courses at Concordia teach deep learning?"

---

### Initial Setup

1. Install Poetry on your system.
2. Clone the repository and run `poetry install` to set up dependencies.
3. Activate the environment with `poetry shell`.
4. Install spaCy's lightweight model for NLP with `python -m spacy download en_core_web_sm`.

### How to Run the Main Script

Execute `python main.py` to initiate:
- `fuseki-server`
- `build_graph`
- `setup_database`

You can also run specific functions as detailed below.

### Specific Task Execution

- **Fuseki Server Setup:**
  - Directly via terminal (refer to the SPARQL server setup section) or `python main.py fuseki-server`
  
- **Generating Output Files:**
  - Ensure proper directory structure as noted in the repository.
  - Acquire necessary `.csv` files from [Concordia OpenData](https://opendata.concordia.ca/datasets/).
  - Run `python main.py build_graph` to parse data and save as `.ttl` in the `output` directory.

- **Upload ttl to SPARQL Database:**
  - Ensure the `fuseki-server` is active at `localhost:3030`.
  - Run `python main.py setup_database`.

- **Combining Tasks:**
  - E.g., With existing `.ttl` files: `python main.py fuseki-server setup_database`.

### Development Tips

- Use `poetry add ...` to install new packages.
- Regularly update this README to reflect changes or enhancements.

### Project Structure

- `data`: Contains datasets and CSVs for students and courses.
- `content`: Holds lectures for selected courses.
- `queries` and `queries2`: Contain SPARQL queries and respective outputs for parts 1 and 2 of the project.
- `rasa`: Includes Rasa setup files for the chatbot (models excluded from git).

### Scripts Overview

- `*_builder.py`: Scripts for parsing and building graphs for academic data, content, and courses.
- `topic_processor.py`: Handles document parsing and entity recognition linking to Wikidata.
- `constants.py`: Maintains consistent namespace domains.
- `helpers.py`: Provides general-purpose methods.
- `sparql_api.py`: Manages Fuseki server connections.
- `main.py`: The primary script starting the fuseki-server and managing data processing tasks.

### SPARQL Server Setup Instructions

- **Mac:**
  - Install with Homebrew: `brew install fuseki`.
  - Start with: `fuseki-server`.
  - Access at `http://localhost:3030/` and upload `.ttl` files for query execution.

- **Windows:**
  - Download and set up Apache Jena Fuseki.
  - Start with `fuseki-server.bat`.
  - Access at `http://localhost:3030/` and manage uploads and queries.

### Rasa Setup

- Ensure Python version compatibility (3.7, 3.8, 3.9, 3.10).
- Navigate to `rasa` directory.
- Execute `rasa train` to prepare the model.
- Run `rasa run actions` and `rasa shell` to start the chat interface.

---

This structured and more visually appealing README aims to enhance user understanding and accessibility to project details, setup guidelines, and usage instructions.