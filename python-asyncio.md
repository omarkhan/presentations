title: Scaling with async IO
author:
  name: Omar Khan
  url: http://omarkhan.me/

--

# Scaling with async IO
## gevent and tulip

--

### @\_\_omar\_\_

- Python developer for the last 8 years
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

### gunicorn

--

### celery

--

# Tulip

--
