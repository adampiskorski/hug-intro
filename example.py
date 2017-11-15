import hug


@hug.get(examples='num_a=1&num_b=2', versions=2)
@hug.cli()
@hug.local()
def add(num_a: hug.types.number, num_b: hug.types.number,
        num_c: hug.types.number):
    """Adds three numbers together"""
    return {'message': num_a + num_b + num_c}


@hug.get(examples='num_a=1&num_b=2', versions=1)
@hug.cli()
@hug.local()
def add(num_a: hug.types.number, num_b: hug.types.number):
    """Adds two numbers together"""
    return {'message': num_a + num_b}


if __name__ == '__main__':
    add.interface.cli()
