from typing import Optional

import typer

from constans import CUR_DIR
from main import main

app = typer.Typer()


@app.command(name="delete")
def delete_all(
        path: str = typer.Argument(CUR_DIR, help="Repertoire dans lequel chercher"),

        # filtered
        extension: str = typer.Option("_all", "--ext", help="extensions à chercher"),
        target: Optional[str] = typer.Option("", "--tar", help="Indices de recherche"),
        only_dir: Optional[bool] = typer.Option(False, "--dir", help="Gérer seulement les repertoires"),

        # search methods
        recursive: Optional[bool] = typer.Option(False, "--rec", help="Recherche recursive"),
        all_data: Optional[bool] = typer.Option(False, "--all", help="Gérer tout type de fichiers")):

    """ Supprimer les données trouvé"""

    main(
        path=path,
        extension=extension,
        target=target,
        only_dir=only_dir,
        recursive=recursive,
        all_data=all_data,
        delete=True,
        ordered=False
    )


@app.command(name="search")
def search(
        path: str = typer.Argument(CUR_DIR, help="Repertoire dans lequel chercher"),

        # filtered
        extension: str = typer.Option("_all", "--ext", help="extensions à chercher"),
        target: Optional[str] = typer.Option("", "--tar", help="Indices de recherche"),
        only_dir: Optional[bool] = typer.Option(False, "--dir", help="Gérer seulement les repertoires"),

        # search methods
        recursive: Optional[bool] = typer.Option(False, "--rec", help="Recherche recursive"),
        all_data: Optional[bool] = typer.Option(False, "--all", help="Gérer tout type de fichiers")):

    """ Rechercher des données """

    main(
        path=path,
        extension=extension,
        target=target,
        only_dir=only_dir,
        recursive=recursive,
        all_data=all_data,
        delete=False,
        ordered=False
    )


@app.command(name="clean")
def ordered(
        path: str = typer.Argument(CUR_DIR, help="Repertoire dans lequel chercher"),

        # filtered
        extension: str = typer.Option("_all", "--ext", help="extensions à chercher"),
        target: Optional[str] = typer.Option("", "--tar", help="Indices de recherche"),
        only_dir: Optional[bool] = typer.Option(False, "--dir", help="Gérer seulement les repertoires"),

        # search methods
        recursive: Optional[bool] = typer.Option(False, "--rec", help="Recherche recursive"),
        all_data: Optional[bool] = typer.Option(False, "--all", help="Gérer tout type de fichiers")):

    """ Mettre de l'ordre dans un repertoire """

    main(
        path=path,
        extension=extension,
        target=target,
        only_dir=only_dir,
        recursive=recursive,
        all_data=all_data,
        delete=False,
        ordered=True
    )



if __name__ == "__main__":
    app()
