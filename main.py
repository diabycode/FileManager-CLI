import sys
import time
from pathlib import Path
from typing import Optional

import typer
import tqdm

from constans import FOLDER_NAME, CUR_DIR


def filters(value):
    print(value)
    return value


def get_folders_name(extensions: list) -> list:
    return list(set([FOLDER_NAME.get(extensions[i], "Autres") for i in range(len(extensions))]))


def Quit(message=""):
    typer.echo(message)
    sys.exit()


def main(
        path: str = typer.Argument(CUR_DIR, help="Repertoire dans lequel chercher"),

        # filtered
        extension: str = typer.Option("_all", "--ext", help="extensions à chercher"),
        target: Optional[str] = typer.Option("", "--tar", help="Indices de recherche"),
        only_dir: Optional[bool] = typer.Option(False, "--dir", help="Gérer seulement les repertoires"),

        # search methods
        recursive: Optional[bool] = typer.Option(False, "--rec", help="Recherche recursive"),
        all_data: Optional[bool] = typer.Option(False, "--all", help="Gérer tout type de fichiers"),

        # actions
        delete: Optional[bool] = typer.Option(False, "--del", help="Supprimer les fichiers trouvé"),
        ordered: Optional[bool] = typer.Option(False, "--ord", help="Ranger les fichier par extensions")
    )\
        -> None:
    """ Gérer les fichiers d'un repertoires """

    # for color in colors:
    #     typer.secho(color, fg=color)

    directorie = Path(path)
    if not directorie.exists():
        typer.echo(f"ERREUR: Repertoire '{directorie}' inexistant.")
        Quit()

    if extension == "_all":
        extension = ""
    else:
        extension = "." + extension if not extension.startswith(".") else extension

    # recuperation des données
    datas = []
    if all_data:
        datas = [data for data in directorie.glob("*")]
        if recursive:
            datas = [data for data in directorie.rglob("*")]
    elif only_dir:
        datas = [data for data in directorie.glob("*") if data.is_dir()]
        if recursive:
            datas = [data for data in directorie.rglob("*") if data.is_dir()]
    else:
        datas = [data for data in directorie.glob(f"*{extension}") if data.is_file()]
        if recursive:
            datas = [data for data in directorie.rglob(f"*{extension}") if data.is_file()]

    # Verif de indice de recherche
    if target:
        datas_with_target = []
        for i in range(len(datas)):
            if target.lower() in str(datas[i].parts[-1].lower()):
                datas_with_target.append(datas[i])
        datas = datas_with_target

    if target:
        typer.secho(f"Indice: '{target}'", fg="bright_white")

    if not datas:
        typer.secho("Aucune donnée !", fg="blue")
        Quit()

    # afficher les fichiers trouvés
    typer.echo(f"__Donnée(s) trouvé(s):")
    folders_counts = 0
    for data in datas:
        color = "cyan"
        if data.is_dir():
            color = "blue"
            folders_counts += 1
        typer.secho("  " + str(data), fg=color)

    typer.secho("dossier: " + str(folders_counts) + "  " + "fichiers: " + str(len(datas)-folders_counts))

    # suppression...
    if delete:
        typer.secho("Voulez-vous supprimer ces fichier ?", fg="red")
        if typer.confirm(""):
            typer.echo("Suppression...")
            for i in range(len(datas)):
                if datas[i].is_file():
                    datas[i].unlink()
                    typer.secho(f"'{datas[i]}' supprimé", fg="green")
                else:
                    try:
                        datas[i].rmdir()
                        typer.secho(f"'{datas[i]}' supprimé", fg="green")
                    except:
                        typer.secho(f"Echec: '{datas[i]}' repertoire non vide !", fg="bright_red")
                time.sleep(.08)
            Quit("Terminé.")
        else:
            Quit("Annuler!")

    # ranger les fichier par extensions
    if ordered:
        extensions = list(set([file.suffix for file in datas]))
        typer.echo("Le(s) fichiers seront rangé (selon le(s) type(s)) dans le(s) repertoire(s) suivant(s):")

        # afficher les dossier qui seront créer
        for folder in get_folders_name(extensions):
            typer.secho("  " + folder, fg="blue")

        if typer.confirm("Voulez-vous poursuivre ?"):
            typer.echo("Déplacements...")
            for i in range(len(datas)):
                folder_name = FOLDER_NAME.get(datas[i].suffix, "Autres")
                destination_path = directorie / folder_name
                destination_path.mkdir(exist_ok=True)
                try:
                    datas[i].rename(destination_path / datas[i].name)
                    typer.secho(f"{datas[i]} rangé.", fg=typer.colors.GREEN)
                except FileExistsError:
                    typer.secho(f"Impossible de déplacer {datas[i]}", fg=typer.colors.BRIGHT_RED)
            Quit("Effectué.")
        Quit("Annuler!")

