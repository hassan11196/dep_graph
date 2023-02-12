"""
Create dummy file with unresolved depedency graph.

"""

import json

if __name__ == '__main__':
    dummy_data = {
        "pkg1": ["pkg2", "pkg3"],
        "pkg2": ["pkg3"],
        "pkg3": []
    }
    with open('/tmp/deps.json', 'w', encoding='UTF-8') as deps_file:
        json.dump(dummy_data, deps_file)
