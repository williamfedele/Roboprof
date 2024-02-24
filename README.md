Roboprof is an intelligent agent that can answer university course- and student-related questions, using a knowledge graph and natural language processing.
For example, Roboprof is able to answer questions such as, “What is course COMP
474 about?”, “Which topics is Jane competent in?” or “Which courses at Concordia
teach deep learning?”


## Initial Setup
- Create conda environment using this command `conda env create -f environment.yml`
- Run `conda activate roboprof`
- Run `python main.py`, you should expect to see output/graph.ttl created


## During development
- Upon adding new dependencies, make sure to run `conda env export > environment.yml` to update our environment file
- Don't forget to update the this README file when appropriate

## Project structure
- data folder contains used for this project, datasets mostly downloaded from https://opendata.concordia.ca/datasets/
