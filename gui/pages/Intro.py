import customtkinter as ctk
import i18n

from gui.pages.PageBase import PageBase
from globals import ARROW, UPPER_FRAME_COLOR
from gui.widgets.Button import ButtonWidget
from gui.widgets.Label import NormalLabelWidget
from gui.widgets.Title import TitleWidget

class IntroPage(PageBase):
  def __init__(self, parent, controller, **kwargs):
    super().__init__(parent, controller, **kwargs)

    self.grid_rowconfigure(1, weight=1)
    self.grid_rowconfigure(2, weight=1)
    self.grid_rowconfigure(3, weight=1)
    self.grid_rowconfigure(4, weight=1)
    
    self.name = "intro"
    
    self._title = TitleWidget(self, i18n.t("intro.welcome"))

    self._add_description()
    self._add_rules()
    self.add_suggestions()

    self._continue_button = ButtonWidget(self, i18n.t("global.continue"), self._on_continue)

    self._title.grid(row=0, column=0, padx=20, pady=20)
    self._continue_button.grid(row=4, column=0, padx=20, pady=20)

  def update_language(self):
    self._title.configure(text=i18n.t("intro.welcome"))
    self.description_label.configure(text=i18n.t("intro.description"))
    self.rules_title.configure(text=i18n.t("intro.rules"))
    self.rule_one.configure(text=ARROW+i18n.t("intro.ruleOne"))
    self.rule_two.configure(text=ARROW+i18n.t("intro.ruleTwo"))
    self.rule_three.configure(text=ARROW+i18n.t("intro.ruleThree"))
    self.suggestions_title.configure(text=i18n.t("intro.suggestions"))
    self.suggestion_one.configure(text=ARROW+i18n.t("intro.suggestionOne"))
    self.suggestion_two.configure(text=ARROW+i18n.t("intro.suggestionTwo"))
    self.suggestion_three.configure(text=ARROW+i18n.t("intro.suggestionThree"))
    self._continue_button.configure(text=i18n.t("global.continue"))

  def _add_description(self):
    description = ctk.CTkFrame(self, fg_color="transparent")

    description.grid_columnconfigure(0, weight=1)
    description.grid_rowconfigure(0, weight=1)
    description.grid_rowconfigure(1, weight=1)

    self.description_label = NormalLabelWidget(description, i18n.t("intro.description"), wraplength=1200)
    description_author = NormalLabelWidget(description, "- JaKaTaK", anchor="e", justify="right")

    self.description_label.grid(row=0, column=0, sticky="nsew")
    description_author.grid(row=1, column=0, sticky="nsew")

    description.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

  def _add_rules(self):
    rules = ctk.CTkFrame(self, fg_color=UPPER_FRAME_COLOR)

    rules.grid_columnconfigure(0, weight=1)
    rules.grid_rowconfigure(0, weight=2)
    rules.grid_rowconfigure(1, weight=1)
    rules.grid_rowconfigure(2, weight=1)
    rules.grid_rowconfigure(3, weight=1)

    self.rules_title = TitleWidget(rules, i18n.t("intro.rules"))
    self.rule_one = NormalLabelWidget(rules, ARROW+i18n.t("intro.ruleOne"), justify="left")
    self.rule_two = NormalLabelWidget(rules, ARROW+i18n.t("intro.ruleTwo"), justify="left")
    self.rule_three = NormalLabelWidget(rules, ARROW+i18n.t("intro.ruleThree"), justify="left")

    self.rule_one.grid(row=1, column=0, padx=20, sticky="w")
    self.rule_two.grid(row=2, column=0, padx=20, sticky="w")
    self.rule_three.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="w")

    rules.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

  def add_suggestions(self):
    suggestions = ctk.CTkFrame(self, fg_color=UPPER_FRAME_COLOR)

    suggestions.grid_columnconfigure(0, weight=1)
    suggestions.grid_rowconfigure(0, weight=2)
    suggestions.grid_rowconfigure(1, weight=1)
    suggestions.grid_rowconfigure(2, weight=1)
    suggestions.grid_rowconfigure(3, weight=1)

    self.suggestions_title = TitleWidget(suggestions, i18n.t("intro.suggestions"))
    self.suggestion_one = NormalLabelWidget(suggestions, ARROW+i18n.t("intro.suggestionOne"), anchor="w", justify="left")
    self.suggestion_two = NormalLabelWidget(suggestions, ARROW+i18n.t("intro.suggestionTwo"), anchor="w", justify="left")
    self.suggestion_three = NormalLabelWidget(suggestions, ARROW+i18n.t("intro.suggestionThree"), anchor="w", justify="left")

    self.suggestion_one.grid(row=1, column=0, padx=20, sticky="w")
    self.suggestion_two.grid(row=2, column=0, padx=20, sticky="w")
    self.suggestion_three.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="w")

    suggestions.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

  def _on_continue(self):
    self.controller.show_frame("info", True)
