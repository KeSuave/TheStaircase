import customtkinter as ctk

from globals import NORMAL_FONT

class NormalLabelWidget(ctk.CTkLabel):
  def __init__(self, master, label, **kwargs):
    super().__init__(master, text=label, font=NORMAL_FONT, **kwargs)

class FadedLabelWidget(ctk.CTkLabel):
  def __init__(self, master, label, **kwargs):
    super().__init__(master, text=label, font=NORMAL_FONT, text_color="gray64", **kwargs)
