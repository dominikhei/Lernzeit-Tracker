
class Error(Exception):
    """Basis Klasse für weitere Exceptions"""
    pass


class TimeIsNegativeError(Error):
    """Aufgeworfen wenn der Wert für eine Reduktion Negativ ist"""
    pass

class VorlesungExistiertNichtError(Error):
    """Ausgeworfen wenn der Benutzer ein Modul löschen will, welches nicht existiert"""
    pass

class FalscherDatenTypError(Error):
    """Aufgeworfen, wenn ein Benutzer einen falschen Datentyp eingibt"""
    pass
