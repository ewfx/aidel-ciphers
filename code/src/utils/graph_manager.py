from utils.ownership_graph import OwnershipGraph

# Singleton pattern for shared graph
ownership_graph = OwnershipGraph()

def add_entity_relationship(owner, owned):
    ownership_graph.add_relationship(owner, owned)

def check_influence_by(source, target):
    return ownership_graph.trace_influence(source, target)

def influenced_entities_by(source):
    return ownership_graph.get_all_influenced(source)
