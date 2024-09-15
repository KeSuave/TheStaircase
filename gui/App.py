import customtkinter as ctk
import json
import os
import i18n

from gui.pages.ChooseUnits import ChooseUnitsPage
from gui.pages.Language import LanguagePage
from gui.pages.Intro import IntroPage
from gui.pages.Info import InfoPage
from gui.pages.Outro import OutroPage
from gui.pages.StepFive import StepFivePage
from gui.pages.StepFour import StepFourPage
from gui.pages.StepOne import StepOnePage
from gui.pages.StepSix import StepSixPage
from gui.pages.StepThree import StepThreePage
from gui.pages.StepTwo import StepTwoPage
from globals import APP_HEIGHT, APP_WIDTH, DEFAULT_CONFIG, MIN_SQ_TO_PASS
from gui.settings import SettingsWindow
from sc2 import SC2

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.FontManager.load_font("assets/fonts/ShareTech.ttf")
ctk.FontManager.load_font("assets/fonts/Starcraft Normal.ttf")

pages = (LanguagePage,
         IntroPage,
         InfoPage,
         StepOnePage,
         StepTwoPage,
         StepThreePage,
         ChooseUnitsPage,
         StepFourPage,
         StepFivePage,
         StepSixPage,
         OutroPage)

i18n.load_path.append("assets/locales")
i18n.set("filename_format", "{locale}.{format}")
i18n.set("fallback", "enUS")

class App(ctk.CTk):
  def __init__(self):
    super().__init__()
    
    self._current_shown_frame = None
    self._choose_units_step = "stepfour"
    self._choose_units_num = 0
    self._settings_window = None
    self._latest_matches_with_passing_sq = 0

    x = (self.winfo_screenwidth() - APP_WIDTH) // 2
    y = (self.winfo_screenheight() - APP_HEIGHT) // 2

    self.title("TheStaircase")
    self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")
    self.iconbitmap("assets/logo.ico")

    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self._load_config()

    self._sc2 = SC2(self._config["player_name"],
                   self._config["race"],
                   self._config["replays"],
                   self._on_sc2_status_update,
                   self._is_valid_stats,
                   self._on_sc2_valid_stats)

    self._frames = {}

    self._create_frames()

    self.protocol("WM_DELETE_WINDOW", self._on_closing)

  def get_config(self):
    return self._config

  def show_frame(self, page_name, set_to_config=False):
    if self._current_shown_frame != None:
      self._current_shown_frame.grid_forget()

    frame = self._frames[page_name]

    if page_name == "chooseunits":
      frame.reset(self._choose_units_num)
    
    frame.grid(row=0, column=0, sticky="nsew")

    self._current_shown_frame = frame

    if set_to_config:
      self._config["page"] = page_name

      self._save_config()

    self._sc2.deactivate()

    if page_name.startswith("step"):
      self.after(1000, self._sc2.activate)

  def set_language(self, lang):
    i18n.set("locale", lang)

    self._config["language"] = lang

    self._save_config()

    for frame in self._frames.values():
      frame.update_language()

    if self._settings_window != None:
      self._settings_window.update_language()

  def set_info(self, player_name, player_race, replay_directory, language=''):
    if language:
      self.set_language(language)
    
    self._config["player_name"] = player_name
    self._config["race"] = player_race
    self._config["replays"] = replay_directory

    self._save_config()

    for frame in self._frames.values():
      if frame.name.startswith("step") or frame.name == "chooseunits":
        frame.set_race()

  def open_config(self):
    if self._settings_window is None or not self._settings_window.winfo_exists():
      self._settings_window = SettingsWindow(self, self)

    self._settings_window.focus()

  def get_player_name(self):
    return self._config["player_name"]

  def get_current_language(self):
    return self._config["language"]
  
  def get_current_replays_directory(self):
    return self._config["replays"]

  def get_match_status(self):
    return self._sc2.get_status()

  def get_latest_matches_with_passing_sq(self):
    return self._latest_matches_with_passing_sq
  
  def get_player_race(self):
    return self._config["race"]

  def continue_from_choose_units(self):
    self._frames[self._choose_units_step].update_units()

    self.show_frame(self._choose_units_step, True)

  def set_choose_units_config(self, num_of_units, step):
    self._choose_units_num = num_of_units
    self._choose_units_step = step

  def get_chosen_units(self):
    return self._frames["chooseunits"].get_chosen_units()

  def _load_config(self):
      file_config = {}

      if os.path.exists("config.json"):
        with open("config.json", "r") as f:
          file_config = json.load(f)

      combined_config = { **DEFAULT_CONFIG, **file_config }
    
      self._config = combined_config

      if not os.path.exists("config.json"):
        self._save_config()

      i18n.set("locale", self._config["language"])

  def _save_config(self):
    with open("config.json", "w") as f:
      json.dump(self._config, f)
  
  def _create_frames(self):
    for F in pages:
        frame = F(self, self)

        self._frames[frame.name] = frame

        if frame.name.startswith("step") or frame.name == "chooseunits":
          frame.set_race()

    if "page" in self._config and self._config["page"] in self._frames:
        self.show_frame(self._config["page"])
    else:
        # language should always be the first page
        self.show_frame("language")
  
  def _is_current_frame_a_step(self):
    return self._current_shown_frame is not None and self._current_shown_frame.name.startswith("step")

  def _on_sc2_status_update(self):
    if self._is_current_frame_a_step():
      self._current_shown_frame.update_progress_status()

  def _on_sc2_valid_stats(self, stats):
    if self._is_current_frame_a_step():
      if stats[0] < MIN_SQ_TO_PASS:
        self._latest_matches_with_passing_sq = 0
      else:
        self._latest_matches_with_passing_sq += 1

      self._config[f"{self._current_shown_frame.name}_{self._config["race"]}_sqs"].append(stats[0])

      self._save_config()
      self._current_shown_frame.update_progress()

  def _is_valid_stats(self, stats):
    if self._is_current_frame_a_step():
      if self._current_shown_frame.is_valid_stats is not None:
        return self._current_shown_frame.is_valid_stats(stats)
    
    return False
  
  def _set_latest_matches_with_passing_sq(self):
    self._latest_matches_with_passing_sq = 0

    if self._is_current_frame_a_step():
      matches = self._config[f"{self._current_shown_frame.name}_{self._config["race"]}_sqs"]

      for sq in reversed(matches):
        if sq >= MIN_SQ_TO_PASS:
          self._latest_matches_with_passing_sq += 1
        else:
          break

  def _on_closing(self):
    self._save_config()
    self._sc2.shutdown()

    self.destroy()
