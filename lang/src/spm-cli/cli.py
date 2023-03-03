import click
from init import init
from deploy import deploy
from install import install

@click.group()
def cli():
  pass

cli.add_command(init)
cli.add_command(install)
cli.add_command(deploy)

if __name__ == '__main__':
  cli()