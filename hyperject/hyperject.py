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
        self._instance = None
        self._f = f

    def __call__(self, container):
        if self._instance is not None:
            return self._instance
        self._instance = self._f(container)
        return self._instance


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
    def __init__(self, graph, path=()):
        self._graph = graph
        self._path = path

    @classmethod
    def make(cls, factory_graph, config):
        return Container({'config': config, **factory_graph}, ())

    def __getattr__(self, key):
        new_path = self._path + (key,)
        try:
            obj = recursive_traversal(self._graph, new_path)
        except KeyError:
            raise KeyError(f"Object at path {new_path} not found.")

        if isinstance(obj, Factory):
            return obj(Container(self._graph, ()))
        elif isinstance(obj, dict):
            return Container(self._graph, new_path)
        else:
            return obj

    def dict(self):
        return recursive_traversal(self._graph, self._path)
