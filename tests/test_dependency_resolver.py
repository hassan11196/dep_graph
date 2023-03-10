""" Tests for dep_graph module
"""
import os
import json
import unittest
from dep_graph.graph_resolver import DependencyResolver, reconstruct_full_dependency_graph
from dep_graph.exceptions import CircularDependencyException, MissingDependencyException

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class TestResolvedGraph(unittest.TestCase):
    """
    Tests for dep_graph module, to verify if the module generates a valid resolved dependency graph.
    """

    def test_resolved_graph_of_valid_deps_file(self):
        """
        Test to verify the dep_graph module generates a valid resolved depenendency graph for a
        given valid depenedency list.
        """
        valid_deps_filepath = os.path.join(
            BASE_PATH, './mock_data/valid_deps.json')
        valid_resolved_deps_filepath = os.path.join(
            BASE_PATH, './mock_data/resolved_valid_deps.json')
        with open(valid_resolved_deps_filepath, encoding='UTF-8') as resolved_file:
            valid_resolved_deps = json.load(resolved_file)

        dependency_resolver = DependencyResolver(valid_deps_filepath)
        resolved_deps = dependency_resolver.resolve_dependency_graph()

        self.assertDictEqual(resolved_deps, valid_resolved_deps)

    def test_circular_dependency_in_graph(self):
        """
        Test to verify dep_graph module throws error on circular dependency list.
        """

        valid_deps_filepath = os.path.join(
            BASE_PATH, './mock_data/circular_deps.json')

        dependency_resolver = DependencyResolver(valid_deps_filepath)
        self.assertRaises(CircularDependencyException,
                          dependency_resolver.resolve_dependency_graph)

    def test_missing_deps_in_graph(self):
        """
        Test to verify dep_graph module throws error on missing deps.
        """

        valid_deps_filepath = os.path.join(
            BASE_PATH, './mock_data/missing_deps.json')

        dependency_resolver = DependencyResolver(valid_deps_filepath)
        self.assertRaises(MissingDependencyException,
                          dependency_resolver.resolve_dependency_graph)

    def test_reconstruct_full_dependency_graph(self):
        """ Test to verify the function in dep_graph module generates
            a valid resolved depenendency graph for a given package depenedency json.
        """
        valid_deps_filepath = os.path.join(
            BASE_PATH, './mock_data/valid_deps.json')
        valid_resolved_deps_filepath = os.path.join(
            BASE_PATH, './mock_data/resolved_valid_deps.json')
        with open(valid_resolved_deps_filepath, encoding='UTF-8') as resolved_file:
            valid_resolved_deps = json.load(resolved_file)

        resolved_deps = reconstruct_full_dependency_graph(valid_deps_filepath)

        self.assertDictEqual(resolved_deps, valid_resolved_deps)
