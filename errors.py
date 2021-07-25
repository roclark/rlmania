class WindowNotFound(Exception):
    """
    Raised when the specified window cannot be found.
    """
    pass


class IdenticalWindowsError(Exception):
    """
    Raised when multiple windows of the same name are found and a unique window
    cannot be identified.
    """
    pass
