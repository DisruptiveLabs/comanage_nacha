import os
import functools

fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')


def _load_fixture(name):
    with open(os.path.join(fixture_path, name), 'r') as f:
        return f.read()


def with_fixture(name):
    def decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            fixture = _load_fixture(name)
            args = list(args)
            args.append(fixture)
            return func(*args, **kwargs)

        return decorated

    return decorator
