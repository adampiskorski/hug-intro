# Hug Intro
## Hug basics
Hug is an API framework that focuses on guiding developers to build 
clean, non repetitive (DRY), modern APIs that are easy to maintain and 
fast that should'nt need to be rewritten in another framework or 
language in the future for the sake of performance.

This is done by focusing on leveraging the Pythonic philosophy by 
allowing a single endpoint definition that is minimalistic and self 
explanatory to have automatic type validation, version handling, 
documentation, be exposed as an internal, cli, or http API and all this 
for free while being the among the fastest web frameworks available for 
Python.

It is also a forward looking framework that only supports Python 3.

### Installation
`pip install hug`

### Internal API
You can leverage most of these features in each kind of endpoint. The 
simplest is internally, by importing and executing hug code:
```python
# example.py
import hug


@hug.local()
def add(num_a: hug.types.number, num_b: hug.types.number):
    """Adds two numbers together"""
    return {'message': num_a + num_b}

```

You can then run it with:
`>>> import example`
`>>> example.add(1,2)`
`{'message': 3}`

It gives you free input coercion:
`>>> example.add('1',2)`
`{'message': 3}`

And meaningful user error messages:
`>>> example.add('a',2)`
`{'errors': {'num_a': 'Invalid whole number provided'}}`

Note that you can use `int` instead of `hug.types.number` and that you can
make your own types.

### CLI API
We can do the same with the CLI by simply adding `@hug.cli()` and adding
a interface bind at the bottom of the file:

```python
import hug


@hug.local()
@hug.cli()
def add(num_a: hug.types.number, num_b: hug.types.number):
    """Adds two numbers together"""
    return {'message': num_a + num_b}


if __name__ == '__main__':
    add.interface.cli()
```

Note that hug uses and understands Python 3.5's new type hinting feature.

Then in the console run:
`$ hug -f example.py -c add 1 2`
`{'message': 3}`

You can get a help command for free:
`$ hug -f example.py -c help`
```
example

Available Commands:

	- add


```

### Web API
You can expose the function to an HTTP GET request by simply adding 
`@hug.get()` and you can give an example like so 
`@hug.get(examples='num_a=1&num_b=2')`:
```
import hug


@hug.local()
@hug.cli()
@hug.get(examples='num_a=1&num_b=2')
def add(num_a: hug.types.number, num_b: hug.types.number):
    """Adds two numbers together"""
    return {'message': num_a + num_b}


if __name__ == '__main__':
    add.interface.cli()

```
Note that you don't need:
```
if __name__ == '__main__':
    add.interface.cli()
```
if you don't want a CLI endpoint anymore.

Then start the development server with:
`$ hug -f example.py`
Note that it doesn't support automatic restart yet, though you can use
Gunicorn for that at the moment.

Then navigate to `http://127.0.0.1:8000/` in a browser and you will see
the full documentation now with usage and examples:
```
{
    "404": "The API call you tried to make was not defined. Here's a definition of the API to help you get going :)",
    "documentation": {
        "handlers": {
            "/add": {
                "GET": {
                    "usage": "Adds two numbers together",
                    "examples": [
                        "http://127.0.0.1:8000/add?num_a=1&num_b=2"
                    ],
                    "outputs": {
                        "format": "JSON (Javascript Serialized Object Notation)",
                        "content_type": "application/json"
                    },
                    "inputs": {
                        "num_a": {
                            "type": "A Whole number"
                        },
                        "num_b": {
                            "type": "A Whole number"
                        }
                    }
                }
            }
        }
    }
}
```

So if you go to `http://127.0.0.1:8000/add?num_a=1&num_b=2` you get your
response:
`{"message": 3}`
Note that the default URL endpoint is the name of the function, but you
can simply change it by adding your alternate URL in as the first 
parameter: `@hug.get('/add2')`
Note that the default output formatting is JSON

You can also add a POST endpoint with `@hug.post(examples='num_a=1&num_b=2')`. 
It can be explored with 
requests:
`>>> requests.post('http://127.0.0.1:8000/add', data = {'num_a': 5, 'num_b': 2}).content`
`b'{"message": 7}'`

Note that you can handle multiple endpoints and URLs with the same 
function definition like so: 
`@hug.call(['POST', 'GET'], ('url1', 'url2'))`

If you have different versions of you function, you can handle that by 
defining the version number or numbers in the hug method decorator:
`@hug.get(versions=1)`:
```
import hug


@hug.get(examples='num_a=1&num_b=2&num_c=3', versions=2)
def add(num_a: hug.types.number, num_b: hug.types.number, num_c: hug.types.number):
    """Adds three numbers together"""
    return {'message': num_a + num_b + num_c}

@hug.local()
@hug.cli()
@hug.get(examples='num_a=1&num_b=2', versions=1)
def add(num_a: hug.types.number, num_b: hug.types.number):
    """Adds two numbers together"""
    return {'message': num_a + num_b}


if __name__ == '__main__':
    add.interface.cli()

```

This will now prefix all URLS with a version number, like so:
`http://127.0.0.1:8000/v1/add?num_a=1&num_b=2`
`http://127.0.0.1:8000/v2/add?num_a=1&num_b=2&num_c=3`

You can also define a range of version numbers, with range(2,8) for example.
Now when you go to the help page, versioning is now taken into account:
```
{
    "404": "The API call you tried to make was not defined. Here's a definition of the API to help you get going :)",
    "documentation": {
        "version": 2,
        "versions": [
            1,
            2
        ],
        "handlers": {
            "/add": {
                "GET": {
                    "usage": "Adds three numbers together",
                    "examples": [
                        "http://127.0.0.1:8000/v2/add?num_a=1&num_b=2&num_c=3"
                    ],
                    "outputs": {
                        "format": "JSON (Javascript Serialized Object Notation)",
                        "content_type": "application/json"
                    },
                    "inputs": {
                        "num_a": {
                            "type": "A Whole number"
                        },
                        "num_b": {
                            "type": "A Whole number"
                        },
                        "num_c": {
                            "type": "A Whole number"
                        }
                    }
                }
            }
        }
    }
}
```
And the latest version is always chosen (even though the older version was
 defined last).
 
### Testing
Testing an HTTP API endpoint is a simple one liner and doesn't require a web server:
`assert hug.test.get(example, 'v2/add', {'num_a': 1, 'num_b': 1, 'num_c': 1}).data == {'message': 2}`

There are many more features and much more documentation:
* [Github page](https://github.com/timothycrosley/hug)
* [Home page](http://www.hug.rest/)
* [Examples](https://github.com/timothycrosley/hug/tree/develop/examples)
