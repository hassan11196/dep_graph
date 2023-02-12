import os
import json


class CircularDependencyException(Exception):
    pass

class MissingDependencyException(Exception):
    pass

def circular_depenenency_check(dependency_list):

    states = {}

    def dfs(node):
        if states.get(node, 0) == 0:
            states[node] = 1
            if node not in dependency_list.keys():
                raise MissingDependencyException()
            for deps in dependency_list[node]:
                if dfs(deps) == 1:
                    return True
            states[node] = 2
            return False

        if states.get(node, 0) == 2:
            return False
        if states.get(node, 0) == 1:
            return True
        

        return False
    for package in dependency_list:
        if dfs(package):
            return True
    return False


def find_deps(package, package_deps, resolved_deps):
    if package_deps[package] == {}:
        resolved_deps[package] = {}
        return []

    if resolved_deps.get(package) is None:
        resolved_deps[package] = {p: find_deps(
            p, package_deps, resolved_deps) for p in package_deps[package]}
    return resolved_deps[package]


def resolve_dep_graph(deps_path):
    if not os.path.exists(deps_path):
        raise FileNotFoundError(f"file at {deps_path} does not exists.")

    with open(deps_path, encoding='UTF-8') as deps_file:
        packages_deps = json.load(deps_file)
        graph = {}
        if circular_depenenency_check(packages_deps):
            raise CircularDependencyException("Circular Dependency Found.")
        for package in packages_deps.keys():
            graph[package] = find_deps(package, packages_deps, graph)

    return graph


def print_package(package, depth, resolved_graph):
    print(f"{depth * '  '}- {package}")

    if resolved_graph == {}:
        return

    for package in sorted(resolved_graph.keys()):
        print_package(package, depth + 1, resolved_graph[package])


def visualize_dep_graph(resolved_graph):
    for package in sorted(resolved_graph.keys()):
        print_package(package, 0, resolved_graph[package])
