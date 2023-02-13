# dep_graph

Simple python package to generate dependency graph from given json file.

## Run module

    python -m dep_graph

  By default it reads from `/tmp/deps.json`

## Run module with given path to package dependencie  

    python -m dep_graph  --path ./some_fir/deps.json

## Create dummy dependency json dummy file

    python dep_graph/helper/create_dummy_file.py --path ./tests test_file.json

 By default it outputs to `/tmp/deps.json`
  
## Run Tests

    python -m unittest discover tests/

## install pre-commit hooks

    pre-commit install
