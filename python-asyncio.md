title: Scaling with async IO
author:
  name: Omar Khan
  url: http://omarkhan.me/
controls: false
style: style.css

--

# Scaling with async IO
## gevent and tulip

--

### @\_\_omar\_\_

- Lead backend developer at [Pocket PlayLab](http://pocketplaylab.com/)
- Python developer for the last 6 years
- Made heavy use of gevent in my last job at [Arachnys](https://www.arachnys.com/)
- Never used tulip for real stuff (nobody has - yet)

--

# What is async IO?

--

### Blocking IO

```python
import requests

urls = ['http://python.org/',
        'http://www.pocketplaylab.com/',
        'http://github.com/']

for url in urls:
    print('Downloading: ' + url)
    requests.get(url)
    print('Done: ' + url)
```

--

### Blocking IO

```python
import requests

urls = ['http://python.org/',
        'http://www.pocketplaylab.com/',
        'http://github.com/']

for url in urls:
    print('Downloading: ' + url)
    requests.get(url)
    print('Done: ' + url)
```

```
Downloading: http://python.org/
Done: http://python.org/
Downloading: http://www.pocketplaylab.com/
Done: http://www.pocketplaylab.com/
Downloading: http://github.com/
Done: http://github.com/
```

--

### Blocking IO

```
Downloading: http://python.org/
Done: http://python.org/
Downloading: http://www.pocketplaylab.com/
Done: http://www.pocketplaylab.com/
Downloading: http://github.com/
Done: http://github.com/
```

- Fetches pages one at a time
- Waits until one page has finished downloading before fetching the next one
- *Blocking* IO - blocks until the operation finishes

--

# Problems with blocking IO

--

### Problems with blocking IO

- The program is not doing anything while we wait for IO
- Slow
- Solution: parallelize

--

### Non-blocking IO

- Threads
- Processes
- Event loop

--

# Threads

--

### Threads

```python
from concurrent.futures import ThreadPoolExecutor
import requests

urls = ['http://python.org/',
        'http://www.pocketplaylab.com/',
        'http://github.com/']

def download(url):
    print('Downloading: ' + url)
    requests.get(url)
    print('Done: ' + url)

with ThreadPoolExecutor(max_workers=10) as thread_pool:
    for url in urls:
        thread_pool.submit(download, url)
```

--

### Threads

```python
from concurrent.futures import ThreadPoolExecutor
import requests

urls = ['http://python.org/',
        'http://www.pocketplaylab.com/',
        'http://github.com/']

def download(url):
    print('Downloading: ' + url)
    requests.get(url)
    print('Done: ' + url)

with ThreadPoolExecutor(max_workers=10) as thread_pool:
    for url in urls:
        thread_pool.submit(download, url)
```

```
Downloading: http://python.org/
Downloading: http://www.pocketplaylab.com/
Downloading: http://github.com/
Done: http://www.pocketplaylab.com/
Done: http://github.com/
Done: http://python.org/
```

--

### Threads

- Scheduled by the operating system
- Share memory and other resources

--

### Problems with threads

- Number of threads limited by OS
- Shared memory
- Synchronisation: locks etc.
- The GIL (Global Interpreter Lock)

--

# Processes

--

### Processes

```python
from concurrent.futures import ProcessPoolExecutor
import requests

urls = ['http://python.org/',
        'http://www.pocketplaylab.com/',
        'http://github.com/']

def download(url):
    print('Downloading: ' + url)
    requests.get(url)
    print('Done: ' + url)

with ProcessPoolExecutor(max_workers=10) as process_pool:
    for url in urls:
        process_pool.submit(download, url)
```

--

### Processes

- Like threads, but without a shared memory space
- No GIL - good for CPU-bound tasks

--

### Problems with processes

- High per-process overhead
- Message-passing overhead

--

# Evented IO

--

### Evented IO

- Event loop
  - libevent
  - libev
  - libuv
- Callbacks
- Easier to synchronise
  - Callbacks explicitly yield control to the main loop

--

# gevent

--

### gevent

- Fast event loop based on libev
- Lightweight execution units based on greenlet
- Monkey patching utility
- Python 2 only

--

### gevent

```python
# Monkey-patch the standard library
from gevent import monkey; monkey.patch_all()

from gevent.pool import Pool
import requests

urls = ['http://python.org/',
        'http://www.pocketplaylab.com/',
        'http://github.com/']

def download(url):
    print('Downloading: ' + url)
    requests.get(url)
    print('Done: ' + url)

pool = Pool(size=10)
for url in urls:
    pool.apply_async(download, args=[url])
pool.join()
```

--

### gevent

```python
...

for url in urls:
    pool.apply_async(download, args=[url])
pool.join()

# OR

responses = list(pool.imap_unordered(download, urls))
```

```
Downloading: http://python.org/
Downloading: http://www.pocketplaylab.com/
Downloading: http://github.com/
Done: http://www.pocketplaylab.com/
Done: http://github.com/
Done: http://python.org/
```

--

### gevent

- Biggest win: use standard library/3rd party packages
- Django!
- Used by Pinterest, Disqus

--

# Scaling web backends

--

### Scaling web backends

- Things that async IO can speed up
  - Database access
  - Request handling
- No need to wait around for data

--

### gunicorn

Just run `gunicorn -k gevent <app>`

```python
# coding=utf-8

import time

def hello(environ, start_response):

    # Do some work...
    time.sleep(1)

    # Send the response
    response = u'สวัสดีครับ\n'.encode('utf-8')
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', len(response)),
    ]
    start_response(status, headers)
    return response
```

--

### gunicorn

Sync:

```
gunicorn server:hello
```

```
$ ab -c 10 -n 10 http://localhost:8000/

Percentage of the requests served within a certain time (ms)
  50%   6010
  66%   7011
  75%   8012
  80%   9013
  90%  10015
  95%  10015
  98%  10015
  99%  10015
 100%  10015 (longest request)
```

--

### gunicorn

Async:

```
gunicorn -k gevent server:hello
```

```
$ ab -c 10 -n 10 http://localhost:8000/

Percentage of the requests served within a certain time (ms)
  50%   1005
  66%   1005
  75%   1005
  80%   1005
  90%   1006
  95%   1006
  98%   1006
  99%   1006
 100%   1006 (longest request)
```

--

### Better performance than threading

From a [mixpanel benchmark](http://code.mixpanel.com/2010/10/29/gevent-the-good-the-bad-the-ugly/) (2010):

![Graph](http://code.mixpanel.com/wp-content/uploads/2010/10/performance2.png)

--

### celery

Just run `celery worker -P gevent`

--

# Tulip

--

### Tulip

- Introduced by Guido in PEP 3156 (Dec 2012)
- Brings async IO into the standard library (replacing asyncore)
- Python 3 only (>=3.4)

--

### Tulip components

- Pluggable event loop
- Coroutines, futures, tasks
- Transports and protocols

--

### Example

```python
import asyncio
import aiohttp

@asyncio.coroutine
def download(url):
    print('Downloading: ' + url)
    yield from aiohttp.request('GET', url)
    print('Done: ' + url)

@asyncio.coroutine
def download_parallel(urls):
    tasks = [asyncio.Task(download(url)) for url in urls]
    yield from asyncio.gather(*tasks)

urls = ['http://python.org/',
        'http://www.pocketplaylab.com/',
        'http://github.com/']

loop = asyncio.get_event_loop()
loop.run_until_complete(download_parallel(urls))
```

--

### Web server example

```python
import asyncio
import aiohttp.server


class HelloServer(aiohttp.server.ServerHttpProtocol):

    @asyncio.coroutine
    def handle_request(self, message, payload):

        # Do some work...
        yield from asyncio.sleep(1)

        # Send the response
        response = aiohttp.Response(self.writer, 200,
                                    http_version=message.version)
        body = u'สวัสดีครับ\n'.encode('utf-8')
        response.add_header('Content-Type', 'text/plain')
        response.add_header('Content-Length', str(len(body)))
        response.send_headers()
        response.write(body)
        yield from response.write_eof()
```

--

### Web server example (cont)

```python
...

loop = asyncio.get_event_loop()
create_server = loop.create_server(HelloServer, '0.0.0.0', '8000')
server = loop.run_until_complete(create_server)
print('Serving on', server.sockets[0].getsockname())
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
```

--

# That's all for now
## Questions?
