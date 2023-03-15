import click
from .init import init
from .deploy import deploy
from .install import install
from .version import version
from .pack import pack

@click.group()
def cli():
  pass

cli.add_command(init)
cli.add_command(install)
cli.add_command(deploy)
cli.add_command(version)
cli.add_command(pack)

if __name__ == '__main__':
  cli()