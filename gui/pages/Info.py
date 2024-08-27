from tkinter import filedialog
import customtkinter as ctk
import i18n

from gui.pages.PageBase import PageBase
from globals import NORMAL_FONT, PROTOSS_IMAGE, SPECIAL_FONT, TERRAN_IMAGE, ZERG_IMAGE
from gui.widgets.Button import ButtonWidget
from gui.widgets.Label import FadedLabelWidget, NormalLabelWidget
from gui.widgets.Title import TitleWidget


class InfoPage(PageBase):
  def __init__(self, parent, controller, **kwargs):
    super().__init__(parent, controller, **kwargs)

    self.name = "info"

    self.grid_rowconfigure(1, weight=2)
    self.grid_rowconfigure(2, weight=1)
    self.grid_rowconfigure(3, weight=1)

    self._selected_race = None

    self._add_player_name()
    self._add_player_race()
    self._add_replay_directory()

    self._continue_button = ButtonWidget(self, i18n.t("global.continue"), self._on_continue)

    self._continue_button.grid(row=3, column=0, padx=20, pady=20)

  def update_language(self):
    self._player_name_label.configure(text=i18n.t("info.playerName"))
    self._player_name_description.configure(text=i18n.t("info.playerNameDescription"))
    self._player_race_label.configure(text=i18n.t("info.race"))
    self._replay_directory_label.configure(text=i18n.t("info.replays"))
    self._replay_directory_button.configure(text=i18n.t("info.replaysBrowse"))
    self._replay_directory_description.configure(text=i18n.t("info.replaysDescription"))
    self._continue_button.configure("global.continue")

  def _add_player_name(self):
    player_name = ctk.CTkFrame(self, fg_color="gray20")

    player_name.grid_columnconfigure(0, weight=1)
    player_name.grid_rowconfigure(0, weight=1)
    player_name.grid_rowconfigure(1, weight=1)
    player_name.grid_rowconfigure(2, weight=1)

    self._player_name_label = TitleWidget(player_name, i18n.t("info.playerName"))
    self._player_name_input = ctk.CTkEntry(player_name, width=200, placeholder_text="Suave", font=NORMAL_FONT)
    self._player_name_description = FadedLabelWidget(player_name, i18n.t("info.playerNameDescription"))

    self._player_name_input.grid(row=1, column=0)
    self._player_name_description.grid(row=2, column=0, pady=(0,20))

    player_name.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

  def _add_player_race(self):
    player_race = ctk.CTkFrame(self)

    player_race.grid_columnconfigure(0, weight=1)
    player_race.grid_rowconfigure(0, weight=1)
    player_race.grid_rowconfigure(1, weight=2)

    self._player_race_label = TitleWidget(player_race, i18n.t("info.race"))

    self._add_player_race_container(player_race)

    player_race.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

  def _add_replay_directory(self):
    replay_directory = ctk.CTkFrame(self, fg_color="gray20")

    replay_directory.grid_columnconfigure(0, weight=10)
    replay_directory.grid_columnconfigure(1, weight=1)
    replay_directory.grid_rowconfigure(0, weight=1)
    replay_directory.grid_rowconfigure(1, weight=1)
    replay_directory.grid_rowconfigure(2, weight=1)

    self._replay_directory_label = TitleWidget(replay_directory, i18n.t("info.replays"))
    self._replay_directory_input = ctk.CTkEntry(replay_directory, font=NORMAL_FONT, placeholder_text="C:\\Users\\Username\\Documents\\StarCraft II\\Accounts\\#AccountID\\#ID\\Replays\\Multiplayer")
    self._replay_directory_button = ctk.CTkButton(replay_directory, text=i18n.t("info.replaysBrowse"), font=NORMAL_FONT, command=self._browse_replay_directory)
    self._replay_directory_description = FadedLabelWidget(replay_directory, i18n.t("info.replaysDescription"), wraplength=1200)

    self._replay_directory_input.grid(row=1, column=0, padx=(20, 5), sticky="ew")
    self._replay_directory_button.grid(row=1, column=1, padx=(5, 20), sticky="ew")
    self._replay_directory_description.grid(row=2, column=0, columnspan=2, pady=(0, 20))

    replay_directory.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
  
  def _add_player_race_container(self, container):
    player_race_container = ctk.CTkFrame(container, fg_color="transparent")

    player_race_container.grid_columnconfigure(0, weight=1)
    player_race_container.grid_columnconfigure(1, weight=1)
    player_race_container.grid_columnconfigure(2, weight=1)
    player_race_container.grid_rowconfigure(0, weight=1)

    terran_image = ctk.CTkImage(TERRAN_IMAGE, size=(273, 390))
    protoss_image = ctk.CTkImage(PROTOSS_IMAGE, size=(273, 390))
    zerg_image = ctk.CTkImage(ZERG_IMAGE, size=(273, 390))

    label_kwargs = {
      "compound": "center",
      "font": SPECIAL_FONT,
      "fg_color": "gray64",
      "padx": 2,
      "pady": 2,
      "cursor": "hand2"
    }

    self.terran_label = ctk.CTkLabel(player_race_container, text="Terran", image=terran_image, **label_kwargs)
    self.protoss_label = ctk.CTkLabel(player_race_container, text="Protoss", image=protoss_image, **label_kwargs)
    self.zerg_label = ctk.CTkLabel(player_race_container, text="Zerg", image=zerg_image, **label_kwargs)

    self.terran_label.grid(row=0, column=0, padx=20, pady=20)
    self.protoss_label.grid(row=0, column=1, padx=20, pady=20)
    self.zerg_label.grid(row=0, column=2, padx=20, pady=20)

    self.terran_label.bind("<Enter>", self._hover_terran)
    self.protoss_label.bind("<Enter>", self._hover_protoss)
    self.zerg_label.bind("<Enter>", self.hover_zerg)

    self.terran_label.bind("<Leave>", self._leave_terran)
    self.protoss_label.bind("<Leave>", self._leave_protoss)
    self.zerg_label.bind("<Leave>", self._leave_zerg)

    self.terran_label.bind("<Button-1>", self._select_terran)
    self.protoss_label.bind("<Button-1>", self._select_protoss)
    self.zerg_label.bind("<Button-1>", self._select_zerg)

    player_race_container.grid(row=1, column=0, stick="nsew")

  def _hover_terran(self, _):
    self._hover_race(self.terran_label)

  def _hover_protoss(self, _):
    self._hover_race(self.protoss_label)

  def hover_zerg(_self, _):
    _self._hover_race(_self.zerg_label)

  def _leave_terran(self, _):
    self._leave_race(self.terran_label)

  def _leave_protoss(self, _):
    self._leave_race(self.protoss_label)

  def _leave_zerg(self, _):
    self._leave_race(self.zerg_label)

  def _select_terran(self, _):
    self._select_race(self.terran_label)

  def _select_protoss(self, _):
    self._select_race(self.protoss_label)

  def _select_zerg(self, _):
    self._select_race(self.zerg_label)

  def _select_race(self, widget):
    if self._selected_race is not None:
      self._selected_race.configure(fg_color="gray64", text_color="gray64")

    self._selected_race = widget

  def _hover_race(self, widget):
    if self._selected_race is not widget:
      widget.configure(fg_color="gray94", text_color="gray94")

  def _leave_race(self, widget):
    if self._selected_race is not widget:
      widget.configure(fg_color="gray64", text_color="gray64")

  def _browse_replay_directory(self):
    dir = filedialog.askdirectory()

    if dir:
      self.replay_directory_path = dir
      
      self._replay_directory_input.delete(0)
      self._replay_directory_input.insert(0, dir)

  def _on_continue(self):
    player_name = self._player_name_input.get()
    player_race = "None"
    replay_directory = self._replay_directory_input.get()

    if not player_name:
      self._player_name_input.focus()

      return
    
    if self._selected_race is self.terran_label:
      player_race = "terran"
    elif self._selected_race is self.protoss_label:
      player_race = "protoss"
    elif self._selected_race is self.zerg_label:
      player_race = "zerg"
    else:
      return

    if not replay_directory:
      self._replay_directory_input.focus()

      return

    self.controller.set_info(player_name, player_race, replay_directory)
    self.controller.show_frame("stepone", True)
