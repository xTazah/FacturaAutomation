import tkinter as tk

class ButtonFactory:
    @staticmethod
    def create_button(parent, onClickHandler, text=None, icon=None, padx=5, pady=5, column=0, row=0):
        # Create the button with either text or icon, based on the arguments passed
        if icon:
            button = tk.Button(parent, image=icon, command=onClickHandler, borderwidth=1, highlightthickness=0)
        elif text:
            button = tk.Button(parent, text=text, command=onClickHandler, borderwidth=1, highlightthickness=0)
        else:
            raise ValueError
        
        button.grid(row=row, column=column,padx=padx, pady=pady)

        return button