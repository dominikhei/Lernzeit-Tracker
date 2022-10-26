from rich.table import Table
from rich.console import Console
import typer
from database import *
from Fehler import *

app = typer.Typer()

start_text = """
-----------------------------------------------------------------------------------------
 _                                    _  _     _____                     _
| |                                  (_)| |   |_   _|                   | |
| |      ___  _ __  _ __   ____  ___  _ | |_    | |   _ __   __ _   ___ | | __  ___  _ __
| |     / _ \| '__|| '_ \ |_  / / _ \| || __|   | |  | '__| / _` | / __|| |/ / / _ \| '__|
| |____|  __/| |   | | | | / / |  __/| || |_    | |  | |   | (_| || (__ |   < |  __/| |
\_____/ \___||_|   |_| |_|/___| \___||_| \__|   \_/  |_|    \__,_| \___||_|\_\ \___||_|

------------------------------------------------------------------------------------------
"""



@app.command(short_help="Zeigt die gelernte Zeit für jedes Modul.")
def zeige_modul():

    create_table()

    result = zeige()

    print(start_text)

    table = Table(title="Deine Lernzeiten")
    table.add_column("Modul")
    table.add_column("Zeiten")
    table.add_column("% von gesamt")

    for row in result:
        table.add_row(*row)
    console = Console()
    console.print(table)

    print("------------------------------------------------------------------------------------------")



@app.command(short_help="Zeigt die gelernte Zeit für jeden Tag der jetzigen Woche.")
def zeige_wochen():

    create_table()

    result = zeige_woche()

    print(start_text)

    table = Table(title="Deine Lernzeiten diese Woche")
    table.add_column("Tag")
    table.add_column("Zeiten")

    for row in result:
        table.add_row(*row)
    console = Console()
    console.print(table)

    print("------------------------------------------------------------------------------------------")



@app.command(short_help='Man kann Zeiten für ein Modul subtrahieren (Gebe immer einen positiven Wert an). Parameter: "Modulname" Zeit')
def veraendere_zeiten(modul: str, zeit: int):

    create_table()

    mdl = modul
    zeiten = zeit

    try:
        if type(mdl) != 'str' or type(zeit) != 'int':
            raise FalscherDatenTypError
        if zeit < 0:
            raise TimeIsNegativeError
        del_time(mdl, zeiten)
        typer.echo("{0} Minuten von Modul {1} gelöscht".format(zeit, mdl))
    except FalscherDatenTypError:
        print("""Du musst den Namen des Moduls in Anführungszeichen
                 setzten und die Anzahl der Minuten muss eine Zahl sein,
                 versuche es erneut""")
    except TimeIsNegativeError:
        print("Du musst einen positiven Wert eingeben, versuche es erneut.")




@app.command(short_help='Zeigt die gerlernte zeit für jeden bisherigen Monat.')
def zeige_monate():

    print(start_text)

    create_table()

    result = zeige_monat()

    table = Table(title="Deine Lernzeiten pro Monat")
    table.add_column("Monat")
    table.add_column("Zeiten")

    for row in result:
        table.add_row(*row)
    console = Console()
    console.print(table)

    print("------------------------------------------------------------------------------------------")




@app.command(short_help='Fügt eine Zeit für ein Modul hinzu. Parameter: "Modulname" Zeit')
def lernzeit(modul: str, minuten : int):

    module = get_lectures()

    if modul not in module:
        val = input("""Das Modul {0} existiert nicht, wenn du es neu anlegen willst und die {1} Minuten hinzufügen willst, drücke y Wenn nicht drücke n """.format(modul, minuten))
        if val.lower() == 'y':

            create_table()

            zeit = minuten
            mdl = modul

            try:
                if type(mdl) != 'str' or type(zeit) != 'int':
                    raise FalscherDatenTypError
                insert_time(mdl, zeit)
                typer.echo("{0} Minuten zu Modul {1} hinzugefügt".format(zeit, mdl))
            except FalscherDatenTypError:
                print("""Du musst den Namen des Moduls in Anführungszeichen
                         setzten und die Anzahl der Minuten muss eine Zahl sein,
                         versuche es erneut""")



@app.command(short_help='Löscht ein Modul und sämtliche verwendete Zeiten. Parameter: "Modulname"')
def loesche_modul(modulname: str):

    module = get_lectures()

    create_table()

    name = modulname

    try:
        if modulname not in module:
            raise VorlesungExistiertNichtError
        if type(name) != 'str':
            raise FalscherDatenTypError
        loesche_vorlesung(name)
        typer.echo(" Modul {0} gelöscht".format(name))
    except VorlesungExistiertNichtError:
        print(" Modul {0} konnte nicht gelöscht werden, da die Vorlesung nicht existiert. Es existieren nur die folgenden Vorlesungen: ".format(name), module)
    except FalscherDatenTypError:
        print("Du musst den Namen der Vorlesung die du löschen willst in Anführungszeichen setzten, versuche es erneut.")


if __name__ == "__main__":
    app()
