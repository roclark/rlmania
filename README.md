# RLMania
RLMania is a reinforcement learning framework for Trackmania (2020).

## Screen Capture
The screen capture tool grabs images from an active window with 'Trackmania' in
the title, though can be extended to any window by specifying a different name.
Prior to executing a script to capture images, the application needs to be
running on the computer. The screen capture tool will find the appropriate
window, set it to the foreground, identify the pixel coordinates for the window,
and capture images as `numpy` arrays. These arrays can be layered for a
reinforcement learning environment to serve as the observation space and
identify motion of the agent.

The capture tool can be used similarly to the following sample script:

```python
from screen_capture import ScreenCapture
from windows_handler import WindowsHandler

handler = WindowsHandler('trackmania').handler
screen_cap = ScreenCapture(handler)

while True:
    np_array = screen_cap.capture_screen()
    ...
```
