import ctypes
import numpy as np
import time
import win32gui
from mss import mss
from typing import Any
from windows_handler import WindowsHandler


FRAMERATE_FRAMES = 60


class ScreenCapture:
    """
    Capture screenshots of a specific active window.

    Parameters
    ----------
    hwdl : Any
        A handler to a specific window.
    """
    def __init__(self, hwdl: Any) -> None:
        self.grabber = mss()

        self._screen_dpi_modifier()
        self.bounding_box = self._bounding_box(hwdl)

    def _screen_dpi_modifier(self) -> None:
        """
        Account for screens with non-standard DPI counts.

        On systems with high DPI levels, the screen capture tool can be off by
        multiple pixels or more, leaving a large chunk of the expected window
        cut off. Making the capture process DPI aware enables greater
        flexibility for different screen types and resolutions.
        """
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()

    def _bounding_box(self, hwdl: Any) -> tuple:
        """
        Get the bounding box for the window.

        Retrieve the pixel coordinates for the specified window.

        Parameters
        ----------
        hwdl : Any
            A handler to the requested window.

        Returns
        -------
        tuple
            Returns a ``tuple`` of integers of the coordinates for the bounding
            box.
        """
        return win32gui.GetWindowRect(hwdl)

    def capture_screen(self, dtype: np.dtype = np.uint8) -> np.ndarray:
        """
        Grab a single screenshot.

        Take a screenshot of the specified dimensions found for a specific
        window.

        Parameters
        ----------
        np.dtype
            The numpy ``dtype`` to save images to as an array.

        Returns
        -------
        Numpy Array
            Returns a numpy array of the specified dtype representing the
            screenshot.
        """
        return np.array(self.grabber.grab(self.bounding_box), dtype=dtype)

    def framerate(self, dtype: np.dtype = np.uint8) -> float:
        """
        Find the framerate for capturing images.

        Find the total amount of time taken to record 60 images and find the
        overall framerate by dividing the 60 frames captured by the total time
        taken to capture all images.

        Parameters
        ----------
        np.dtype
            The numpy ``dtype`` to save images to as an array.

        Returns
        -------
        float
            Returns a ``float`` of the framerate in frames per second.
        """
        start_time = time.time()

        for _ in range(FRAMERATE_FRAMES):
            self.capture_screen(dtype=dtype)

        stop_time = time.time()

        framerate = FRAMERATE_FRAMES / (stop_time - start_time)
        return framerate
