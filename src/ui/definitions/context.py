from typing import Callable
from ui.definitions.interactible import InteractionControl
from ui.definitions.renderable import Renderable
from ui.definitions.device import Shell
from pynput.keyboard import Listener
from os import system
from time import sleep

from ui.definitions.screen import Screen

class UIContext:
    def __init__(self) -> None:
        self.__signaling = {
            'stop': False,
        }

        self.__interaction_control = InteractionControl(self.__signaling)
        self.__device = Shell()

    def get_control(self):
        return self.__interaction_control

    def get_device(self):
        return self.__device

    def launch(self):
        try:
            system("stty -echo")

            with Listener(on_press=self.__interaction_control.handle_key) as listener:
                while not self.__signaling['stop']:
                    sleep(1)
                listener.stop()
                listener.join()

            print("Goodbye! 'u'")
        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt as e:
            print("Killed x_x")
        finally:
            system("stty echo")
