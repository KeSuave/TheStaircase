import tkinter as tk
import customtkinter as ctk
import i18n

from globals import NORMAL_FONT
from gui.widgets.Button import ButtonWidget
from gui.widgets.Label import NormalLabelWidget

class SettingsWindow(ctk.CTkToplevel):
  def __init__(self, parent, controller, **kwargs):
    super().__init__(parent, **kwargs)
    
    self.controller = controller

    self.title(i18n.t("modal.settings.title"))
    self.geometry("500x460")
    self.resizable(False, False)
    self.after(250, lambda: self.iconbitmap("assets/logo.ico"))

    self.grid_columnconfigure(0, weight=2)
    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(1, weight=1)
    self.grid_rowconfigure(2, weight=1)
    self.grid_rowconfigure(3, weight=1)
    self.grid_rowconfigure(4, weight=1)
    self.grid_rowconfigure(5, weight=1)
    self.grid_rowconfigure(6, weight=1)
    self.grid_rowconfigure(7, weight=1)
    self.grid_rowconfigure(8, weight=1)
    self.grid_rowconfigure(9, weight=1)

    self._language_label = NormalLabelWidget(self, i18n.t("modal.settings.changeLanguage"))
    self._language_options = ctk.CTkOptionMenu(self, values=["English (US)", "Español (US)"], font=NORMAL_FONT)
    self._player_name = NormalLabelWidget(self, i18n.t("modal.settings.changePlayerName"))
    self._player_name_input = ctk.CTkEntry(self, font=NORMAL_FONT)
    self._replays_label = NormalLabelWidget(self, i18n.t("modal.settings.changeReplaysDirectory"))
    self._replays_input = ctk.CTkEntry(self, font=NORMAL_FONT)
    self._replays_button = ctk.CTkButton(self, text=i18n.t("modal.settings.replaysBrowse"), font=NORMAL_FONT, command=self._on_browse)
    self._race_label = NormalLabelWidget(self, i18n.t("modal.settings.changeRace"))
    self._race_options = ctk.CTkOptionMenu(self, values=["terran", "protoss", "zerg"], font=NORMAL_FONT)
    self._reset_button = ButtonWidget(self, i18n.t("modal.settings.resetProgress"), self._on_reset)
    self._save_button = ButtonWidget(self, i18n.t("modal.settings.saveChanges"), self._on_save)

    self._language_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    self._language_options.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    self._player_name.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    self._player_name_input.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    self._replays_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    self._replays_input.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
    self._replays_button.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")
    self._race_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    self._race_options.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    self._reset_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    self._save_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    if self.controller.get_current_language() == "enUS":
      self._language_options.set("English (US)")
    else:
      self._language_options.set("Español (US)")

    self._player_name_input.insert(0, self.controller.get_player_name())
    self._replays_input.insert(0, self.controller.get_current_replays_directory())

    self._race_options.set(self.controller.get_player_race())

  def update_language(self):
    self.title(i18n.t("modal.settings.title"))

    self._language_label.configure(text=i18n.t("modal.settings.language"))
    self._replays_label.configure(text=i18n.t("modal.settings.replays"))
    self._race_label.configure(text=i18n.t("modal.settings.race"))
    self._reset_button.configure(text=i18n.t("modal.settings.reset"))

  def _on_browse(self):
    dir = tk.filedialog.askdirectory()

    if dir:      
      self._replays_input.delete(0)
      self._replays_input.insert(0, dir)

  def _on_reset(self):
    if tk.messagebox.askyesno(f"{i18n.t("modal.settings.title")} - {i18n.t("modal.settings.reset")}", i18n.t("modal.settings.resetProgressConfirm")):
      self.controller.reset_settings()
  
  def _on_save(self):
    language_option = self._language_options.get()
    language = ""
    player_name = self._player_name_input.get()
    race = self._race_options.get()
    replays = self._replays_input.get()

    if language_option == "English (US)":
      language = "enUS"
    else:
      language = "esUS"

    self.controller.set_info(player_name, race, replays, language)
    self.destroy()
