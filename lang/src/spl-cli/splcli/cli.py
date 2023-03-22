import click
from .combine import combine
from .init import init

@click.group()
def cli():
  pass

cli.add_command(init)
cli.add_command(combine)

if __name__ == '__main__':
  cli()