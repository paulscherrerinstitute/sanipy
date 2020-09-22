from concurrent.futures import ThreadPoolExecutor


def parallel(func, targets, names):
    with ThreadPoolExecutor() as executor:
        results = executor.map(func, targets)
#        return list(results)
        return dict(zip(names, results))


def serial(func, targets):
    return [func(t) for t in targets]
#    return {t: func(t) for t in targets}



