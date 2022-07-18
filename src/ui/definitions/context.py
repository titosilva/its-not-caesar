from typing import Callable
from ui.definitions.renderable import InteractionControl, Renderable
from ui.definitions.screen import ShellScreen
from pynput.keyboard import Listener
from os import system
from time import sleep

class UIContext:
    def __init__(self) -> None:
        self.__signaling = {
            'stop': False,
        }

        self.__interaction_control = InteractionControl(self.__signaling)
        self.__screen = ShellScreen()

    def get_control(self):
        return self.__interaction_control

    def get_screen(self):
        return self.__screen

    def set_ui_content(self, content):
        self.__content = content

    def launch(self):
        try:
            system("stty -echo")

            with Listener(on_press=self.__interaction_control.handle_key) as listener:
                while not self.__signaling['stop']:
                    if callable(self.__content):
                        self.__screen.draw(self.__content(self.__screen))
                    else:
                        self.__screen.draw(self.__content)
                    sleep(0.2)

                listener.stop()
                listener.join()

            print("Goodbye! 'u'")
        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt as e:
            print("Killed x_x")
        finally:
            system("stty echo")
            