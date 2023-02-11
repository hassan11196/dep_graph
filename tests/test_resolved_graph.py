import os
import json
import unittest
from dep_graph import graph_resolver

class TestResolvedGraph(unittest.TestCase):
    def setUp(self):
        self.base_deps_filepath = "base_deps.json"
        self.original_resolved_graph = {'pkg3': {}, 'pkg2': {
            'pkg3': {}}, 'pkg1': {'pkg2': {'pkg3': {}}, 'pkg3': {}}}
        base_deps = {
            "pkg1": ["pkg2", "pkg3"],
            "pkg2": ["pkg3"],
            "pkg3": []
        }
        with open(self.base_deps_filepath, "w", encoding='UTF-8') as deps_file:
            json.dump(base_deps, deps_file)

    def tearDown(self):
        if os.path.exists(self.base_deps_filepath):
            os.remove(self.base_deps_filepath)

    def test_resolved_graph(self):
        resolved_graph = graph_resolver.resolve_dep_graph(
            self.base_deps_filepath)
        assert resolved_graph == self.original_resolved_graph
