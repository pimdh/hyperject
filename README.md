# Hyperject
Simple tool for configuration based dependency injection. Designed for hyperparameter setting in machine learning experiments. Does not use global state, but instead combines nested dictionaries of factory functions with a configuration JSON-style object to construct a graph of objects.

This is a work in progress.
## Installation
`pip install git+https://github.com/pimdh/hyperject@master`

## Usage example
```
import random
from hyperject import factory, singleton, Container


@factory
def factory_a(container):
    return f"{container.config.a + 2}{container.config.b.c}"


@factory
def factory_b(container):
    return random.randint(0, 1E10)


@singleton
def factory_c(container):
    return container.random.b


@singleton
def factory_d(container):
    return container.a * 2


def test_container():
    config = {'a': 3, 'b': {'c': 'd'}}
    factory_graph = {
        'a': factory_a,
        'random': {
            'b': factory_b,
            'c': factory_c,
        },
        'd': factory_d,
    }
    container = Container.make(factory_graph, config)
    assert container.a == "5d"
    assert container.random.b != container.random.b
    assert container.random.c == container.random.c
    assert container.d == "5d5d"
```

The `@factory` decorator creates a factory that creates a new object at each call, while the `@singleton` decorator reuses the object.
