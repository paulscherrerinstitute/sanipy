from concurrent.futures import ThreadPoolExecutor


def parallel(func, *targets, names=None):
    with ThreadPoolExecutor() as executor:
        results = executor.map(func, *targets)
        if names is not None:
            return dict(zip(names, results))
        else:
            return list(results)


def serial(func, *targets, names=None):
    targets = zip(*targets)
    if names is not None:
        return {n: func(*t) for n, t in zip(names, targets)}
    else:
        return [func(*t) for t in targets]



