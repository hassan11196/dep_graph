""" Core class of module. provides DependencyResolver to resolved package dependency graphs.

    Raises:
        FileNotFoundError: raised when dependency graph file does not exist at the provided path.
        CircularDependencyException:
            raised when theres a circular dependency present inside the code.
        MissingDependencyException:
            raised when the given dependency graph has missing packages without its dependency list.

"""
import os
import json

from .exceptions import MissingDependencyException, CircularDependencyException


class DependencyResolver(object):
    """DependencyResolver class to resolve package dependency graphs.

    """
    def __init__(self, deps_path):
        self.deps_path = deps_path
        self.unresolved_graph = {}
        self.resolved_graph = {}
        if not os.path.exists(deps_path):
            raise FileNotFoundError(f"file at {deps_path} does not exists.")

    def _resolve_package_dependencies(self, package):
        if self.unresolved_graph[package] == {}:
            self.resolved_graph[package] = {}
            return []

        if self.resolved_graph.get(package) is None:
            self.resolved_graph[package] = {p: self._resolve_package_dependencies(
                p) for p in self.unresolved_graph[package]}

        return self.resolved_graph[package]

    def load_dependency_graph(self):
        """Loads Unresolved dependency graph from path given at object instantiation.
        """
        with open(self.deps_path, encoding='UTF-8') as deps_file:
            self.unresolved_graph = json.load(deps_file)

    def resolve_dependency_graph(self):
        """Resolves the dependency graph and returns a resolved dependency graph.

        Raises:
            CircularDependencyException:
                raised when theres a circular dependency present inside the given dependency graph.

        Returns:
            _type_: dict
        """
        self.load_dependency_graph()
        if self.circular_dependency_check():
            raise CircularDependencyException(
                "Circular Dependency Found in Graph. Exiting")

        for package in self.unresolved_graph.keys():
            self.resolved_graph[package] = self._resolve_package_dependencies(
                package)

        return self.resolved_graph

    def _package_depenencies_contain_cycle(self, package, states):
        if package not in states:
            states[package] = 'resolving'

            if package not in self.unresolved_graph.keys():
                raise MissingDependencyException()

            for deps in self.unresolved_graph[package]:
                if self._package_depenencies_contain_cycle(deps, states):
                    return True
            states[package] = 'resolved'

        if states[package] == 'resolved':
            return False
        if states[package] == 'resolving':
            return True

        return False

    def circular_dependency_check(self):
        """Checks if the given dependency graph has any circular dependencies.

        Returns:
            _type_: bool
        """
        states = {}
        for package in self.unresolved_graph:
            if self._package_depenencies_contain_cycle(package, states):
                return True
        return False
