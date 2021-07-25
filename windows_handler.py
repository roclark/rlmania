import win32gui
from errors import IdenticalWindowsError, WindowNotFound
from typing import Any


class WindowsHandler:
    """
    Extract a handler for a specific active window.

    Parameters
    ----------
    screen_name : str
        A ``string`` of the title to match from the list of enumerated windows.
    """
    def __init__(self, screen_name: str) -> Any:
        self._windows = self._enumerate_screens()
        _hwdl = self._extract_window(self._windows, screen_name)
        self._set_windows_foreground(_hwdl)
        self.handler = _hwdl

    def _enumerate_callback(self, hwdl: Any, windows: list) -> list:
        """
        Enumerate all running windows.

        Create a list of tuples representing the window handle plus the text
        corresponding to the window.

        Parameters
        ----------
        hwdl : Any
            A handler pointing to a single active window.
        windows : list
            A ``list`` of ``tuples`` where each item represents the handler to
            the window and the corresponding text for the window.

        Returns
        -------
        list
            Returns a ``list`` of ``tuples`` where each item represents the
            handler to a window and the corresponding text for the window.
        """
        windows.append((hwdl, win32gui.GetWindowText(hwdl)))

    def _enumerate_screens(self) -> list:
        """
        Enumerate all active screens.

        Get a list of all active screens running on the PC including the window
        handler and the corresponding text.

        Returns
        -------
        list
            Returns a ``list`` of ``tuples`` where each item represents the
            handler to a window and the corresponding text for the window.
        """
        windows = []

        win32gui.GetDesktopWindow()
        win32gui.EnumWindows(self._enumerate_callback, windows)
        return windows


    def _extract_window(self, windows: list, screen_name: str) -> Any:
        """
        Retrieve the handle for a specific window.

        Iterate through a list of enumerated active windows on the system and
        attempt to find a match for a specific window with a given title. If
        multiple windows exist with the same name, throw an error that the specific
        window can't be identified. If no matching windows can be found, throw an
        error that it can't be found.

        Parameters
        ----------
        windows : list
            A ``list`` of ``tuples`` where each item represents the handler to a
            window and the corresponding text for the window.
        screen_name : str
            A ``string`` of the title to match from the list of enumerated windows.

        Returns
        -------
        Any
            Returns a handler to the requested window if found.

        Raises
        ------
        WindowNotFound
            Raises a ``WindowNotFound`` error if no windows match the requested
            title.
        IdenticalWindowsError
            Raises an ``IdenticalWindowsError`` when there are multiple running
            windows with the same name and a unique instance cannot be found.
        """
        window = [(hwdl, title) for hwdl, title in windows
                if screen_name.lower() in title.lower()]
        if not len(window):
            raise WindowNotFound(f'Screen "{screen_name}" not found. Ensure a '
                                 f'window with name "{screen_name}" is '
                                 'running.')
        elif len(window) > 1:
            # Multiple windows have the screen name included in at least part
            # of the title. Check for an exact copy of the name excluding case.
            window = [(hwdl, title) for hwdl, title in window
                    if screen_name.lower() == title.lower()]
            if len(window) != 1:
                raise IdenticalWindowsError('Multiple windows contain the '
                                            f'name {screen_name}. Unable to '
                                            'identify unique window.')
        # The first and only element is the requested window at this point.
        hwdl, _ = window[0]
        return hwdl

    def _set_windows_foreground(self, hwdl: Any) -> None:
        """
        Set the requested window to the foreground.

        In order to capture screenshots, the window needs to be placed in the
        foreground as the screen grabber captures the specified dimensions for
        the top-most windows.

        hwdl : Any
            A handler to the requested window.
        """
        win32gui.SetForegroundWindow(hwdl)
