import streamlit as st
from streamlit_d3graph import d3graph, vec2adjmat


def create_graph():
    # Source node names
    source = [
        "Penny",
        "Penny",
        "Amy",
        "Bernadette",
        "Bernadette",
        "Sheldon",
        "Sheldon",
        "Sheldon",
        "Rajesh",
    ]
    # Target node names
    target = [
        "Leonard",
        "Amy",
        "Bernadette",
        "Rajesh",
        "Howard",
        "Howard",
        "Leonard",
        "Amy",
        "Penny",
    ]
    # Edge Weights
    weight = [5, 3, 2, 2, 5, 2, 3, 5, 2]

    # Convert the vector into a adjacency matrix
    adjmat = vec2adjmat(source, target, weight=weight)

    # Initialize
    d3 = d3graph()
    d3.graph(adjmat)
    return d3


# Initialize
# d3 = d3graph()
# # Load karate example
# adjmat, df = d3.import_example("karate")

# label = df["label"].values
# node_size = df["degree"].values

# d3.graph(adjmat)
# d3.set_node_properties(color=df["label"].values)
# d3.show()

# d3.set_node_properties(label=label, color=label, cmap="Set1")
# d3.show()


d = create_graph()
d.show()
