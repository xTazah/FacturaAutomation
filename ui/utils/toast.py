import tkinter as tk

class Toast(tk.Toplevel): 
    def __init__(self, master, width=175, height=50, bg='white', text='Toast Message', auto_close_time=None): #ToDo: toast show size automatically to fit content
        super().__init__(master)
        self.geometry(f"{width}x{height}+{master.winfo_width() - width - 20}+{master.winfo_height() - height - 50}")
        self.overrideredirect(True)  # Remove window decorations (title bar)
        self.configure(bg=bg)

        self.auto_close_time = auto_close_time

        # Create the close button
        close_btn = tk.Button(self, text='X', bg=bg, command=self.hide_animation, relief="flat")
        close_btn.pack(side="right", padx=5)

        # Create the toast message label
        message = tk.Label(self, text=text, bg=bg, fg="black")
        message.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Start the show animation
        self.show_animation()

        # Schedule auto-close if time is set
        if self.auto_close_time is not None:
            self.after(self.auto_close_time, self.hide_animation)

    def show_animation(self):
        # ToDo: implement animationm
        pass

    def hide_animation(self):
        self.destroy()  # Destroy the toast window
