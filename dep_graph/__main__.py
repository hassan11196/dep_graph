from .graph_resolver import resolve_dep_graph, visualize_dep_graph


if __name__ == '__main__':
    deps_path = '/tmp/deps.json'
    resolved_graph = resolve_dep_graph(deps_path)
    visualize_dep_graph(resolved_graph)
