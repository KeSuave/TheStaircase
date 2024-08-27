import customtkinter as ctk
import i18n

from gui.images import UNIT_IMAGES
from gui.pages.PageBase import PageBase
from globals import ARROW, MIN_MATCHES_TO_PROGRESS, MIN_SQ_TO_PASS, SPECIAL_FONT, UPPER_FRAME_COLOR

from gui.widgets.Button import ButtonWidget
from gui.widgets.Label import FadedLabelWidget, NormalLabelWidget
from gui.widgets.Title import TitleWidget

MAX_UNITS = 9

class StepBasePage(PageBase):
  rules = []
  units = []
  general_suggestions = []
  race_suggestions = []

  next_step_extra_units = 0
  extra_units = 0
  allow_mine_vespene = False
  prev_step = None
  next_step = None
  next_step_after_choosing = ""

  _general_suggestion_labels = {}
  _race_suggestion_labels = {}

  def __init__(self, parent, controller, **kwargs):
    super().__init__(parent, controller, **kwargs)

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1) # title
    self.grid_rowconfigure(1, weight=1) # rules and units
    self.grid_rowconfigure(2, weight=1) # matches/progress
    self.grid_rowconfigure(3, weight=1) # motto
    self.grid_rowconfigure(4, weight=1) # suggestions
    self.grid_rowconfigure(5, weight=1) # buttons/nav

    self._create_frames()
    self._create_config()

  def is_valid_stats(self, stats):
    if stats[0] < MIN_SQ_TO_PASS:
      return False
    
    if not self.allow_mine_vespene and stats[2] == "VESPENE_YES":
      return False
    
    for unit in stats[1]:
      if unit not in self.units:
        return False
    
    return True

  def set_race(self):
    self._update_unit_images()

    self._remove_race_suggestions()
    self._add_race_suggestions()
    
    self.update_language()
    self.update_progress()
  
  def update_units(self):
    self._update_unit_images()

  def update_progress(self):
    progress = self.controller.get_valid_step_matches() / MIN_MATCHES_TO_PROGRESS

    if progress > 1:
      progress = 1

    self._progress.set(progress)

    self.update_progress_status()

    if self.next_button is not None and self._get_next_button_state() == "normal":
      self._progress_status.configure(state="normal")

  def update_progress_status(self):
    self._update_progress_description()
    self._update_progress_status()

  def update_language(self):
    self._title.configure(text=i18n.t(f"steps.{self.name}"))

    structure_key = f"steps.{self.controller.get_player_race()}SupplyStructures"
    for rule in self.rules:
      self._rule_labels[rule].configure(text=ARROW+i18n.t(f"steps.rules.{rule}",
                                                          supplyStructures=i18n.t(structure_key)))

    self._progress_title.configure(text=i18n.t(f"steps.progress.title"))

    self.update_progress_status()

    self._motto_title.configure(text=i18n.t(f"steps.motto.title"))
    self._motto_text.configure(text=i18n.t(f"steps.motto.text"))

    self._suggestions_title.configure(text=i18n.t(f"steps.suggestions.title"))

    for suggestion in self.general_suggestions:
      self._general_suggestion_labels[suggestion].configure(text=i18n.t(f"steps.suggestions.{suggestion}"))

    for suggestion in self.race_suggestions:
      self._race_suggestion_labels[suggestion].configure(text=i18n.t(f"steps.suggestions.{suggestion}"))

    if self.prev_step is not None:
      self.prev_button.configure(text=i18n.t(f"steps.prevStep"))

    if self.next_step is not None:
      self.next_button.configure(text=i18n.t(f"steps.nextStep"))

  def _create_frames(self):
    self._create_title()
    self._create_rules()
    self._create_units()
    self._create_progress()
    self._create_motto()
    self._create_suggestions()
    self._create_nav_buttons()

  def _create_title(self):
    self._title = TitleWidget(self, i18n.t(f"steps.{self.name}"))

    self._title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

  def _create_rules(self):
    rules_container = ctk.CTkFrame(self, fg_color=UPPER_FRAME_COLOR)

    rules_container.grid_columnconfigure(0, weight=1)
    rules_container.grid_rowconfigure(0, weight=1)

    for i in range(len(self.rules)):
      rules_container.grid_rowconfigure(i + 1, weight=1)

    self._rules_title = TitleWidget(rules_container, i18n.t("steps.rules.title"))

    structure_key = f"steps.{self.controller.get_player_race()}SupplyStructures"

    self._rule_labels = {}
    for i in range(len(self.rules)):
      rule = self.rules[i]

      rule_label = NormalLabelWidget(rules_container,
                                     ARROW+i18n.t(f"steps.rules.{rule}",
                                             supplyStructures=i18n.t(structure_key)),
                                     wraplength=500,
                                     justify="left")

      self._rule_labels[rule] = rule_label

      ypad = 0

      if i == len(self.rules) - 1:
        ypad = (0, 20)

      rule_label.grid(row=i + 1, column=0, padx=20, pady=ypad, sticky="w")

    rules_container.grid(row=1, column=0, padx=10, pady=20, sticky="nsew")

  def _create_units(self):
    units_container = ctk.CTkFrame(self, fg_color=UPPER_FRAME_COLOR)

    units_container.grid_columnconfigure(0, weight=1)
    units_container.grid_columnconfigure(1, weight=1)
    units_container.grid_columnconfigure(2, weight=1)
    units_container.grid_rowconfigure(0, weight=1) # title
    units_container.grid_rowconfigure(1, weight=1) # units 1-3
    units_container.grid_rowconfigure(2, weight=1) # units 4-6
    units_container.grid_rowconfigure(2, weight=1) # units 7-9
    units_container.grid_rowconfigure(3, weight=1) # change units button
    
    self.units_title = ctk.CTkLabel(units_container, text=i18n.t("steps.units.title"), font=SPECIAL_FONT)

    self.units_title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

    self._unit_image_labels = []
    for i in range(MAX_UNITS):
      img_label = ctk.CTkLabel(units_container, image=UNIT_IMAGES["nounit"], text="")

      img_label.grid(row=i // 3 + 1,
                     column=i % 3,
                     padx=20,
                     pady=20,
                     sticky="nsew")

      self._unit_image_labels.append(img_label)

    units_container.grid(row=1, column=1, padx=10, pady=20, sticky="nsew")

  def _create_progress(self):
    progress_container = ctk.CTkFrame(self, fg_color=UPPER_FRAME_COLOR)

    progress_container.grid_columnconfigure(0, weight=1)
    progress_container.grid_rowconfigure(0, weight=1) # title
    progress_container.grid_rowconfigure(1, weight=1) # progress bar
    progress_container.grid_rowconfigure(2, weight=1) # description
    progress_container.grid_rowconfigure(3, weight=1) # status

    self._progress_title = TitleWidget(progress_container, i18n.t("steps.progress.title"))
    self._progress = ctk.CTkProgressBar(progress_container, orientation="horizontal", mode="determinate")
    self._progress_description = FadedLabelWidget(progress_container,i18n.t("steps.progress.description"))
    self._progress_status = NormalLabelWidget(progress_container,
                                             i18n.t("steps.progress.status.label")+
                                             ": " + i18n.t("steps.progress.status.gameNotOpened"))

    self._progress.set(self.controller.get_valid_step_matches() / MIN_MATCHES_TO_PROGRESS)

    self._progress.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
    self._progress_description.grid(row=2, column=0, padx=20, sticky="ew")
    self._progress_status.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

    progress_container.grid(row=2, column=0, columnspan=4, padx=10, pady=0, sticky="ew")

  def _create_motto(self):
    motto_container = ctk.CTkFrame(self, fg_color=UPPER_FRAME_COLOR)

    motto_container.grid_columnconfigure(0, weight=1)
    motto_container.grid_rowconfigure(0, weight=1)
    motto_container.grid_rowconfigure(1, weight=1)

    self._motto_title = TitleWidget(motto_container, i18n.t("steps.motto.title"))
    self._motto_text = NormalLabelWidget(motto_container, i18n.t("steps.motto.text"))

    self._motto_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

    motto_container.grid(row=3, column=0, columnspan=2, padx=10, pady=20, sticky="nsew")

  def _create_suggestions(self):
    self._suggestions_container = ctk.CTkFrame(self, fg_color=UPPER_FRAME_COLOR)

    self._suggestions_container.grid_columnconfigure(0, weight=1)
    self._suggestions_container.grid_rowconfigure(0, weight=1)

    self._suggestions_title = TitleWidget(self._suggestions_container, i18n.t("steps.suggestions.title"))

    self._general_suggestion_labels = {}
    for i in range(len(self.general_suggestions)):
      suggestion = self.general_suggestions[i]

      self._suggestions_container.grid_rowconfigure(i+1, weight=1)

      suggestion_label = NormalLabelWidget(self._suggestions_container,
                                     ARROW+i18n.t(f"steps.suggestions.{suggestion}"),
                                     wraplength=1100,
                                     justify="left")

      self._general_suggestion_labels[suggestion] = suggestion_label

      suggestion_label.grid(row=i + 1, column=0, padx=20, sticky="w")
    
    self._suggestions_container.grid(row=4, column=0, columnspan=2, padx=10, sticky="nsew")

  def _add_race_suggestions(self):
    general_suggestions = len(self.general_suggestions)

    self._race_suggestion_labels = {}
    for i in range(len(self.race_suggestions)):
      suggestion = self.race_suggestions[i]

      self._suggestions_container.grid_rowconfigure(i+1+general_suggestions, weight=1)

      suggestion_label = NormalLabelWidget(self._suggestions_container,
                                     ARROW+i18n.t(f"steps.suggestions.{suggestion}"),
                                     wraplength=1100,
                                     justify="left")

      self._race_suggestion_labels[suggestion] = suggestion_label

      ypad = 0

      if i == len(self.race_suggestions) - 1:
        ypad = (0, 20)

      suggestion_label.grid(row=i + 1 + general_suggestions, column=0, padx=20, pady=ypad, sticky="w")

  def _update_unit_images(self):
    for i in range(len(self.units)):
      self._unit_image_labels[i].configure(image=UNIT_IMAGES[self.units[i]])

    for i in range(len(self.units), MAX_UNITS):
      self._unit_image_labels[i].configure(image=UNIT_IMAGES["nounit"])

  def _remove_race_suggestions(self):
    for label in self._race_suggestion_labels.values():
      label.grid_forget()
      label.destroy()

  def _create_nav_buttons(self):
    if self.prev_step is not None:
      self.prev_button = ButtonWidget(self, i18n.t("steps.prevStep"), self._on_prev_button, width=380)
    
      self.prev_button.grid(row=5, column=0, padx=10, pady=20, sticky="w")
    if self.next_step is not None:
      self.next_button = ButtonWidget(self,
                                      i18n.t("steps.nextStep"),
                                      self._on_next_button,
                                      width=380,
                                      state=self._get_next_button_state())

      self.next_button.grid(row=5, column=1, padx=10, pady=20, sticky="e")

  def _create_config(self):
    self.config = ctk.CTkButton(self, text="⚙", width=40, height=40, command=self.controller.open_config)

    self.config.place(relx=0.99, rely=0.01, anchor="ne")

  def _update_progress_description(self):
    label = i18n.t(f"steps.progress.description")

    if self._get_next_button_state() == "normal":
      label = i18n.t(f"steps.progress.descriptionAfterCompletion")
    
    self._progress_description.configure(text=label)

  def _update_progress_status(self):
    self._progress_status.configure(text=i18n.t(f"steps.progress.status.{self.controller.get_match_status()}"))

  def _on_prev_button(self):
    self.controller.show_frame(self.prev_step)

  def _on_next_button(self):
    if self.next_step == "chooseunits":
      self.controller.set_choose_units_config(self.next_step_extra_units, self.next_step_after_choosing)

    self.controller.show_frame(self.next_step, self.next_step != "chooseunits")

  def _get_next_button_state(self):
    return "normal" if self.controller.get_valid_step_matches() >= MIN_MATCHES_TO_PROGRESS else "disabled"
