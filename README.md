This is the repository for “Discrepancy Between Humans and LVLMs in Directed Graph Annotations of Learning Sequences: A Case Study on the Middle School Mathematics Curriculum” from JSAI2025.

This repository includes the following files and datasets.

## Directories

### `dataset`
Contains the datasets used in the study.

- `simplified_formatted_paper_name/`: Contains annotated datasets.
- `label_studio/`: Includes label studio dataset file for annotation works.

### `visualization_paper`
Contains curriculum graph visualization result images.

### `math_graph`
Contains module files to run the code scripts.

## Code Files

### `cal_edges.py`
Calculates the mean number of edges per node in the graph for each dataset.

### `vis_graph.py`
Visualizes the curriculum graph and saves the result as a PDF file.

### `cal_jaccard_sim.py`
Calculates the Jaccard similarity between pairs of graphs from different datasets.

### `cal_dataset_stat.py`
Counts and prints statistics of the results in the dataset.

### `cal_mean_cross_topic_edges.py`
Calculates the mean number of cross-topic edges in the graph for a given dataset.


### `label_studio.xml`
Label Studio annotation layout file.

