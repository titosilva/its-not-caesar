from ui.definitions.context import UIContext
from ui.screens.initial_screen import InitialScreen

if __name__ == "__main__":
    context = UIContext()
    InitialScreen(context)
    context.launch()