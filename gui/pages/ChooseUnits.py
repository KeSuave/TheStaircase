import customtkinter as ctk
import i18n

from globals import APP_HEIGHT, APP_WIDTH, UPPER_FRAME_COLOR
from gui.images import UNIT_IMAGES
from gui.pages.PageBase import PageBase
from gui.widgets.Button import ButtonWidget
from gui.widgets.Title import TitleWidget


class ChooseUnitsPage(PageBase):
  def __init__(self, parent, controller, **kwargs):
    super().__init__(parent, controller, **kwargs)

    self.name = "chooseunits"

    self._terran_units = ["marauder",
                         "reaper",
                         "thor",
                         "cyclone",
                         "tank",
                         "ghost",
                         "viking",
                         "battlecruiser",
                         "liberator",
                         "banshee",
                         "raven",
                         "mine"]
    self._protoss_units = ["stalker",
                          "adept",
                          "sentry",
                          "immortal",
                          "colossus",
                          "disruptor",
                          "dt",
                          "ht",
                          "archon",
                          "void",
                          "oracle",
                          "tempest",
                          "carrier",
                          "phoenix"]
    self._zerg_units = ["roach",
                       "baneling",
                       "ravager",
                       "hydralisk",
                       "lurker",
                       "ultralisk",
                       "mutalisk",
                       "swarm",
                       "brood",
                       "infestor",
                       "viper",
                       "corruptor"]
    self._num_of_units_to_choose = 0
    self._selected_units = []

    container = ctk.CTkFrame(self, width=APP_WIDTH, height=APP_HEIGHT)

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)
    container.grid_rowconfigure(2, weight=1)
    container.grid_rowconfigure(3, weight=1)

    container.grid(row=0, column=0, sticky="nsew")

    self.title = TitleWidget(container, i18n.t("steps.chooseUnits", count=self._num_of_units_to_choose))
    self.unit_container = ctk.CTkFrame(container, fg_color=UPPER_FRAME_COLOR)
    self._continue_button = ButtonWidget(self, i18n.t("global.continue"), self._on_continue, state="disabled")

    self.title.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
    self._continue_button.grid(row=3, column=0, padx=10, pady=20)

    self.unit_container.grid_columnconfigure(0, weight=1)
    self.unit_container.grid_columnconfigure(1, weight=1)
    self.unit_container.grid_columnconfigure(2, weight=1)
    self.unit_container.grid_columnconfigure(3, weight=1)
    self.unit_container.grid_columnconfigure(4, weight=1)
    self.unit_container.grid_columnconfigure(5, weight=1)
    self.unit_container.grid_columnconfigure(6, weight=1)
    self.unit_container.grid_columnconfigure(7, weight=1)
    self.unit_container.grid_rowconfigure(1, weight=1)
    self.unit_container.grid_rowconfigure(2, weight=1)

    self._unit_image_labels = []
    for i in range(14):
      img_label = ctk.CTkLabel(self.unit_container,
                               image=UNIT_IMAGES["nounit"],
                               text=" ",
                               fg_color="transparent",
                               compound="center",
                               padx=2,
                               pady=2,
                               cursor="arrow")

      row = i // 7
      col = i % 7

      padx = 10
      pady = (20, 10)

      if row == 1:
        pady = (10, 20)

      if col == 0:
        padx = (20, 10)
      elif col == 6:
        padx = (10, 20)

      img_label.grid(row=row, column=col, padx=padx, pady=pady)

      img_label.bind("<Button-1>", lambda event, i=i: self._on_unit_click(i))
      img_label.bind("<Enter>", lambda event, i=i: self._on_unit_enter(i))
      img_label.bind("<Leave>", lambda event, i=i: self._on_unit_leave(i))

      self._unit_image_labels.append(img_label)

    self.unit_container.grid(row=1, column=0, padx=10, pady=20, sticky="nsew")

  def update_language(self):
    self.title.configure(text=i18n.t("steps.chooseUnits", count=self._num_of_units_to_choose))

  def set_race(self):
    units = self._get_units_from_current_race()

    for i in range(len(units)):
      label = self._unit_image_labels[i]
      
      label.configure(image=UNIT_IMAGES[units[i]])
      label.configure(cursor="hand2")

    for i in range(len(units), len(self._unit_image_labels)):
      label = self._unit_image_labels[i]

      label.configure(image=UNIT_IMAGES["nounit"])
      label.configure(cursor="arrow")

  def set_num_of_units_to_choose(self, num):
    self._num_of_units_to_choose = num
    self.update_language()

  def get_chosen_units(self):
    names = []
    units = self._get_units_from_current_race()

    for index in self._selected_units:
      names.append(units[index])

    return names

  def reset(self, number_of_units_to_choose):
    for unit in self._selected_units:
      self._unit_image_labels[unit].configure(fg_color="transparent")

    self._selected_units.clear()

    self.set_num_of_units_to_choose(number_of_units_to_choose)

    self._continue_button.configure(state="disabled")

    self.update_language()

  def _is_a_unit(self, index):
    return self._unit_image_labels[index].cget("image") != UNIT_IMAGES["nounit"]

  def _on_unit_click(self, index):
    if not self._is_a_unit(index):
      return

    if index not in self._selected_units:
      self._selected_units.append(index)
      self._unit_image_labels[index].configure(fg_color="gray94")
    else:
      self._selected_units.remove(index)
      self._unit_image_labels[index].configure(fg_color="transparent")

    if len(self._selected_units) == self._num_of_units_to_choose:
      self._continue_button.configure(state="normal")
    else:
      self._continue_button.configure(state="disabled")

  def _on_unit_enter(self, index):
    if not self._is_a_unit(index):
      return

    if index not in self._selected_units:
      self._unit_image_labels[index].configure(fg_color="gray94")

  def _on_unit_leave(self, index):
    if not self._is_a_unit(index):
      return

    if index not in self._selected_units:
      self._unit_image_labels[index].configure(fg_color="transparent")

  def _on_continue(self):
    self.controller.continue_from_choose_units()

  def _get_units_from_current_race(self):
    race = self.controller.get_player_race()
    units = []

    if race == "terran":
      units = self._terran_units
    elif race == "protoss":
      units = self._protoss_units
    elif race == "zerg":
      units = self._zerg_units

    return units
