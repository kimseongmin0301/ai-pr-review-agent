"""Empty on purpose.

pytest prepends the directory containing the root ``conftest.py`` to
``sys.path``, which is what lets ``tests/`` import the ``app`` and
``reviewer`` packages when you simply run ``pytest -q`` from the
repository root. No fixtures belong here yet.
"""
