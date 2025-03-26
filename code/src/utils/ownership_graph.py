from collections import defaultdict, deque

class OwnershipGraph:
    def __init__(self):
        self.graph = defaultdict(set)

    def add_relationship(self, owner, owned):
        self.graph[owner].add(owned)

    def trace_influence(self, source_entity, target_entity, max_depth=3):
        visited = set()
        queue = deque([(source_entity, 0)])
        while queue:
            current, depth = queue.popleft()
            if current == target_entity and depth > 0:
                return True
            if depth >= max_depth:
                continue
            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        return False

    def get_all_influenced(self, source_entity, max_depth=3):
        influenced = set()
        queue = deque([(source_entity, 0)])
        while queue:
            current, depth = queue.popleft()
            if depth >= max_depth:
                continue
            for neighbor in self.graph.get(current, []):
                if neighbor not in influenced:
                    influenced.add(neighbor)
                    queue.append((neighbor, depth + 1))
        return influenced
