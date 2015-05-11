title: pytest - because this ain't java
author:
  name: Omar Khan
  url: http://omarkhan.me/
controls: false
style: style.css

--

# pytest - because this ain't java

--

### @\_\_omar\_\_

- Backend lead at [Playlab Games](http://www.playlab.com/)
- Python developer for the last 6 years
- Mainly django, some web crawling and machine learning too

--

# Testing

--

### Why test?

- Catch regressions
- Clarify your designs
- Improve code quality
- Make life easier for new developers
- You're doing it anyway

--

### Testing pyramid

![Testing pyramid](images/testing-pyramid.png)

from [rubyplus.com](https://rubyplus.com/)

--

# Testing in python

--

### Testing in python

- doctest
- unittest
- nose
- **[pytest](https://pytest.org/)**

--

### doctest

```python
def square(x):
    """
    Squares x.

    >>> square(2)
    4
    >>> square(-2)
    4
    """
    return x * x

if __name__ == '__main__':
    import doctest
    doctest.testmod()
```

from [python-guide.org](http://python-guide.org/)

--

### doctest

Success - no output

Failure:

    **********************************************************************
    File "tests.py", line 5, in __main__.square
    Failed example:
        square(2)
    Expected:
        4
    Got:
        3
    **********************************************************************

--

### doctest

- In the stdlib
- Good for simple unit tests
- Makes great documentation
- Not enough on its own

--

### unittest

```python
import unittest

def square(x):
    return x * x

class MyTest(unittest.TestCase):
    def setUp(self):
        # Do some setup
        pass

    def test_square(self):
        self.assertEqual(square(2), 4)
        self.assertEqual(square(-2), 4)

    def tearDown(self):
        # Tear everything down
        pass

if __name__ == '__main__':
    unittest.main()
```

--

### unittest

Success:

    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK

Failure:

    F
    ======================================================================
    FAIL: test_square (__main__.MyTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests.py", line 12, in test_square
        self.assertEqual(square(2), 4)
    AssertionError: 3 != 4

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    FAILED (failures=1)

--

### unittest

- In the stdlib
- De-facto standard
- Direct port of JUnit
- Powerful but **unpythonic**

--

### pytest

```python
def square(x):
    return x * x

def test_square():
    assert square(2) == 4
    assert square(-2) == 4
```

    $ py.test tests.py

    ================================================ test session starts =================================================
    platform darwin -- Python 2.7.9 -- py-1.4.26 -- pytest-2.7.0
    rootdir: /Users/omar/dev/presentations, inifile:
    collected 1 items

    tests.py .

    ============================================== 1 passed in 0.01 seconds ==============================================

--

### pytest

Failure:

    ================================================ test session starts =================================================
    platform darwin -- Python 2.7.6 -- py-1.4.26 -- pytest-2.7.0
    rootdir: /Users/omar/dev/presentations, inifile:
    collected 1 items

    tests.py F

    ====================================================== FAILURES ======================================================
    ____________________________________________________ test_square _____________________________________________________

        def test_square():
    >       assert square(2) == 4
    E       assert 3 == 4
    E        +  where 3 = square(2)

    tests.py:5: AssertionError
    ============================================== 1 failed in 0.01 seconds ==============================================

--

### pytest

- Has been around forever
- Simple, clean, pythonic

--

### Fixtures

```python
import os
import pytest

def exp(x):
    return x ** int(os.environ['EXPONENT'])

@pytest.fixture
def square():
    os.environ['EXPONENT'] = '2'

def test_exp(square):
    assert exp(2) == 4
    assert exp(-2) == 4
```

--

### Discovery

- Suffix each test file with `_test.py`
- Run `py.test`

--

### Examples

- [flask](https://github.com/mitsuhiko/flask/tree/master/tests)
