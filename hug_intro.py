import hug

@hug.local()
def hello(name: hug.types.text):
    """Hello world"""
    return {'message': 'hello {0}'.format(name)}
