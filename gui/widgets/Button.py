import customtkinter as ctk

from globals import SPECIAL_FONT

class ButtonWidget(ctk.CTkButton):
  def __init__(self, master, label, cmd, **kwargs):
    default_kwargs = {
        "text": label,
        "font": SPECIAL_FONT,
        "corner_radius": 0,
        "width": 260,
        "height": 60,
        "command": cmd
    }

    combined_kwargs = {**default_kwargs, **kwargs}

    super().__init__(master, **combined_kwargs)
