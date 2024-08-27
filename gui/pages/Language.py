import customtkinter as ctk

from gui.pages.PageBase import PageBase
from globals import APP_HEIGHT, APP_WIDTH
from gui.widgets.Button import ButtonWidget


class LanguagePage(PageBase):
  def __init__(self, parent, controller, **kwargs):
    super().__init__(parent, controller, **kwargs)

    self.name = "language"

    container = ctk.CTkFrame(self, width=APP_WIDTH, height=APP_HEIGHT)

    container.grid(row=0, column=0, sticky="nsew")

    english_button = ButtonWidget(container, "English", self._set_language_to_english)
    spanish_button = ButtonWidget(container, "Español", self._set_language_to_spanish)

    english_button.place(relx=0.45, rely=0.5, anchor="e")
    spanish_button.place(relx=0.55, rely=0.5, anchor="w")

  def update_language(self):
    pass

  def _set_language_to_english(self):
    self.controller.set_language("enUS")
    self.controller.show_frame("intro", True)

  def _set_language_to_spanish(self):
    self.controller.set_language("esUS")
    self.controller.show_frame("intro", True)
