import customtkinter as ctk

from globals import SPECIAL_FONT

class TitleWidget(ctk.CTkLabel):
  def __init__(self, master, label, **kwargs):
    super().__init__(master, text=label, font=SPECIAL_FONT, **kwargs)

    self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
