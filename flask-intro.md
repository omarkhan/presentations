title: Introduction to Flask
author:
  name: Omar Khan
  url: http://omarkhan.me/

--

# Introduction to Flask

--

### @\_\_omar\_\_

- Lead backend developer at [Pocket PlayLab](http://pocketplaylab.com/)
- Python developer for the last 6 years
- Used Flask in production, briefly

--

# What is Flask?

--

### What Flask is

- Web microframework
- Routing
- Templating (jinja2)
- Sessions

--

### What Flask is not

- Full-featured
- No ORM
- No auth
- No admin panel
- But extensions exist for all of these and more
- Consider using django if you know you will need these features

--

### Routing

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
```

--

### Templates

```
/application.py
/templates
    /hello.html
```

```python
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```

```xml
<!doctype html>
<title>Hello from Flask</title>
{% if name %}
  <h1>Hello {{ name }}!</h1>
{% else %}
  <h1>Hello World!</h1>
{% endif %}
```

--

### Testing

```python
import unittest
from application import app

class HelloWorldTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello(self):
        response = self.client.get('/hello')
        self.assertEqual(response.data, 'Hello World!')
```

--

# The good

--

![Flask debugger](http://flask.pocoo.org/docs/0.10/_images/debugger.png)

--

# The bad

--

### Request context

"Certain objects in Flask are global objects, but not of the usual kind. These
objects are actually proxies to objects that are local to a specific context."

```python
from flask import request

@app.route('/hello', method='POST')
def hello():
    assert request.path == '/hello'
    assert request.method == 'POST'
```

Seriously?!

--

### Request context

- Request context and sessions implemented as thread-locals
- Not a nice design decision
- Global state
- Makes it harder to write tests and other code that doesn't run in a
  request-response cycle
    - Use a fake request context

--

### tl;dr

- Good for prototyping small webapps
- For anything bigger, use django
