title: Scaling with async IO
author:
  name: Omar Khan
  url: http://omarkhan.me/

--

# Scaling with async IO
## gevent and tulip

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
