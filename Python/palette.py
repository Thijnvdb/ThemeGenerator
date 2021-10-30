# palette.py
import click
import colorget

@click.command()
@click.argument('image')
def main(**kwargs):
    scheme = colorget.getScheme(kwargs["image"])
    for e in scheme:
        click.echo(e)

if __name__ == "__main__":
    main()