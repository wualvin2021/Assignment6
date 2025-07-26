import networkx as nx
from collections import deque

# Created directed graph
G = nx.DiGraph()

# User nodes with attributes
G.add_node("user_1", type="user", gender="female", location="US", reading_level=12, num_posts=5)
G.add_node("user_2", type="user", gender="male", location="UK", reading_level=9, num_posts=3)
G.add_node("user_3", type="user", gender="female", location="US", reading_level=14, num_posts=8)

# Post nodes
G.add_node("post_1", type="post", num_comments=2)
G.add_node("post_2", type="post", num_comments=10)
G.add_node("post_3", type="post", num_comments=0)

# edge: (user ➝ post)
G.add_edge("user_1", "post_1")
G.add_edge("user_3", "post_2")

# edge: (post ➝ user)
G.add_edge("post_1", "user_2")
G.add_edge("post_2", "user_1")
G.add_edge("post_2", "user_2")
G.add_edge("post_2", "user_3")
G.add_edge("post_3", "user_1")  # viewed by user_1

# Stackable attributes
def is_interesting(user_data, filters):
    return all(user_data.get(attr) == val or
               (callable(val) and val(user_data.get(attr)))
               for attr, val in filters.items())

# BFS traversal with filtering
def bfs_with_filters(graph, start_node, filters):
    visited = set()
    queue = deque([start_node])
    interesting_users = []

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        node_data = graph.nodes[current]

        if node_data.get("type") == "user" and is_interesting(node_data, filters):
            interesting_users.append(current)

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                queue.append(neighbor)

    return interesting_users

# Analyst-defined filters
filters = {
    "gender": "female",
    "location": "US",
    "reading_level": lambda x: x >= 10,
    "num_posts": lambda x: x >= 5
}

# Run BFS from a user
interesting = bfs_with_filters(G, "user_1", filters)
print("Interesting users found from BFS:", interesting)