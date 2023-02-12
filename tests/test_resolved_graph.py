import os
import json
import unittest
from dep_graph import graph_resolver

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class TestResolvedGraph(unittest.TestCase):
    """
    Tests for dep_graph module
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

        resolved_deps = graph_resolver.resolve_dep_graph(valid_deps_filepath)

        self.assertDictEqual(resolved_deps, valid_resolved_deps)

    def test_circular_dependency_in_graph(self):
        """
        Test to verify dep_graph module throws error on circular dependency list.
        """

        valid_deps_filepath = os.path.join(
            BASE_PATH, './mock_data/circular_deps.json')
        self.assertRaises(graph_resolver.CircularDependencyException, graph_resolver.resolve_dep_graph, valid_deps_filepath)

    def test_missing_deps_in_graph(self):
        """
        Test to verify dep_graph module throws error on missing deps.
        """

        valid_deps_filepath = os.path.join(
            BASE_PATH, './mock_data/missing_deps.json')
        self.assertRaises(graph_resolver.MissingDependencyException, graph_resolver.resolve_dep_graph, valid_deps_filepath)