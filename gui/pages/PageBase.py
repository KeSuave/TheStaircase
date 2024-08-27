import customtkinter as ctk

class PageBase(ctk.CTkScrollableFrame):
  def __init__(self, parent, controller, **kwargs):
    super().__init__(parent, **kwargs)
    self.controller = controller

    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
