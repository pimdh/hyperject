class Factory:
    def __call__(self, container):
        raise NotImplementedError()


class FunctionFactory(Factory):
    def __init__(self, f):
        self._f = f

    def __call__(self, container):
        return self._f(container)


class SingletonFactory(Factory):
    def __init__(self, f):
        self._instances = {}
        self._f = f

    def __call__(self, container):
        stored = self._instances.get(id(container))
        if stored is not None:
            return stored
        self._instances[id(container)] = self._f(container)
        return self._instances[id(container)]


def singleton(f):
    return SingletonFactory(f)


def factory(f):
    return FunctionFactory(f)


def recursive_traversal(graph, path):
    while path:
        key, *path = path
        if key not in graph:
            raise KeyError()
        graph = graph[key]
    return graph


class Container:
    def __init__(self, graph):
        self._graph = graph

    @classmethod
    def make(cls, factory_graph, config):
        return Container({'config': config, **factory_graph})

    def get(self, path):
        try:
            obj = recursive_traversal(self._graph, path)
        except KeyError:
            raise KeyError(f"Object at path {path} not found.")

        if isinstance(obj, Factory):
            return obj(self)
        elif isinstance(obj, dict):
            return TraversedContainer(self, path)
        else:
            return obj

    def __getattr__(self, key):
        return self.get((key,))

    def dict(self, path=()):
        return recursive_traversal(self._graph, path)


class TraversedContainer:
    def __init__(self, container, path):
        self._container = container
        self._path = path

    def __getattr__(self, key):
        return self._container.get(self._path + (key,))

    def dict(self):
        return self._container.dict(self._path)
