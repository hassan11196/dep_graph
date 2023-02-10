import os
import json


def find_deps(package, package_deps, resolved_deps):
    if package_deps[package] == {}:
        resolved_deps[package] = {}
        return []

    if resolved_deps.get(package) is None:
        resolved_deps[package] = {p: find_deps(
            p, package_deps, resolved_deps) for p in package_deps[package]}
    return resolved_deps[package]


def resolve_dep_graph(deps_path):
    if os.path.exists(deps_path):
        with open(deps_path, encoding='UTF-8') as deps_file:
            packages_deps = json.load(deps_file)
            graph = {}
            for package in packages_deps.keys():
                graph[package] = find_deps(package, packages_deps, graph)
    return graph


def print_package(package, depth, resolved_graph):
    print(f"{depth * '  '}- {package}")
    # print(resolved_graph)
    if resolved_graph == {}:
        return

    for package in sorted(resolved_graph.keys()):
        print_package(package, depth + 1, resolved_graph[package])


def visualize_dep_graph(resolved_graph):
    for package in sorted(resolved_graph.keys()):
        print_package(package, 0, resolved_graph[package])


if __name__ == '__main__':
    deps_path = '/tmp/deps.json'
    resolved_graph = resolve_dep_graph(deps_path)
    visualize_dep_graph(resolved_graph)
