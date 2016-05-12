import hug

@hug.get(examples='name=Adam')
@hug.local()
def hello(name: hug.types.text):
    """Hello world"""
    return {'message': 'hello {0}'.format(name)}
