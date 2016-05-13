import hug


@hug.cli()
@hug.get(examples='name=Adam')
@hug.local()
def hello(name: hug.types.text):
    """Hello world"""
    return {'message': 'hello {0}'.format(name)}


if __name__ == '__main__':
    hello.interface.cli()
