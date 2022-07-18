from ui.definitions.context import UIContext
from ui.screens.initial_screen import generate_initial_screen

if __name__ == "__main__":
    context = UIContext()
    context.set_ui_content(generate_initial_screen)
    context.launch()