from seez.tests.mypy import mypy_test


def test_mypy():
    mypy_test("setup.cfg")
