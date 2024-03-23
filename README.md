Roboprof is an intelligent agent that can answer university course- and student-related questions, using a knowledge graph and natural language processing.
For example, Roboprof is able to answer questions such as, “What is course COMP
474 about?”, “Which topics is Jane competent in?” or “Which courses at Concordia
teach deep learning?”

## Initial Setup
- Ensure you have Poetry set up on your computer
- After cloning the repo, run `poetry install` to install dependencies then `poetry shell` to enter the shell environment.

## Generate output files
- Make sure you have `CATALOG.csv` and `CU_SR_OPEN_DATA_CATALOG.csv` from `https://opendata.concordia.ca/datasets/`
- Run `python main.py`, this will parse the model, use the `course_builder`, `lecture_builder`, and `academic_builder`, merge the individual graphs and save them to folder `output`. you should expect to see `output/ntriples.ttl` and `output/turtles.ttl` created.

## During development
- Use `poetry add ...` for installing a new package
- Don't forget to update the this README file when appropriate

## Project structure
- `data` folder contains the datasets used for this project, can be downloaded from `https://opendata.concordia.ca/datasets/`
- `content` folder contains lectures and slides
- `queries` folder contains the queries and their outputs

## SPARQL server setup
first, make sure to generate our ttl/nt files by running python main.py.

On Mac:
- Install Apache Jena Fuseki (`brew install fuseki` if you have homebrew).
- Run `fuseki-server --version` to make sure it's installed.
- To start the server, run `fuseki-server`.
- Open your web browser and go to `http://localhost:3030/`.
- Upload one of the ttl/nt files generated by your script.
- Use the Fuseki interface to write and execute your SPARQL queries.

On Windows (requires Java 17):
- Download apache-jena-fuseki-5.0.0-rc1.zip from (https://jena.apache.org/download/).
- Extract the downloaded ZIP file to a desired location on your system.
- Open Command Prompt and navigate to the extracted folder.
- Run `fuseki-server.bat --version` to make sure it's installed.
- To start the server, run `fuseki-server.bat`.
- Open your web browser and go to `http://localhost:3030/`.
- Upload one of the ttl/nt files generated by your script.
- Use the Fuseki interface to write and execute your SPARQL queries.