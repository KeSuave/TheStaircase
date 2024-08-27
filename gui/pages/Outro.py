import customtkinter as ctk
import i18n

from gui.pages.PageBase import PageBase
from globals import ARROW, UPPER_FRAME_COLOR
from gui.widgets.Button import ButtonWidget
from gui.widgets.Label import NormalLabelWidget
from gui.widgets.Title import TitleWidget

class OutroPage(PageBase):
  def __init__(self, parent, controller, **kwargs):
    super().__init__(parent, controller, **kwargs)

    self.grid_rowconfigure(1, weight=1)
    self.grid_rowconfigure(2, weight=1)
    self.grid_rowconfigure(3, weight=1)
    
    self.name = "outro"
    
    self._title = TitleWidget(self, i18n.t("outro.title"))
    self.content_label = NormalLabelWidget(self, i18n.t("outro.content"), wraplength=1200)
    self.thanks_label = NormalLabelWidget(self, i18n.t("outro.thanks"), wraplength=1200)
    self.author_label = NormalLabelWidget(self, "- KeSuave", justify="right")

    self._title.grid(row=0, column=0, padx=20, pady=20)
    self.content_label.grid(row=1, column=0, padx=20, pady=20)
    self.thanks_label.grid(row=2, column=0, padx=20, pady=20)
    self.author_label.grid(row=3, column=0, padx=20, pady=20, sticky="e")

  def update_language(self):
    self._title.configure(text=i18n.t("intro.welcome"))
    self.content_label.configure(text=i18n.t("intro.content"))
    self.thanks_label.configure(text=i18n.t("outro.thanks"))
