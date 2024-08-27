from gui.pages.StepBase import StepBasePage


class StepSixPage(StepBasePage):
  def __init__(self, parent, controller, **kwargs):
    self.name = "stepsix"

    self.rules = ["mineMinerals",
                  "mineGas",
                  "noCommandCard",
                  "unitsPerProduction",
                  "productionPerBase"]

    self.general_suggestions = ["haveFun",
                                "experiment",
                                "focus",
                                "screenMovement",
                                "screenPositions",
                                "hotkeys",
                                "threeBases",
                                "aggressive",
                                "economy",
                                "unitActive",
                                "avoidBaseCamera"]

    self.next_step = "outro"
    self.extra_units = 3

    super().__init__(parent, controller, **kwargs)

  def set_race(self):
    race = self.controller.get_player_race()

    self._set_units_by_race()

    if race == "terran":
      self.race_suggestions = ["ccToOrbital", "ccEnergy"]
    elif race == "protoss":
      self.race_suggestions = ["nexusEnergy"]
    elif race == "zerg":
      self.race_suggestions = ["queenEnergy"]

    super().set_race()

  def update_units(self):
    self._set_units_by_race()

    chosen_units = self.controller.get_chosen_units()

    for i in range(len(chosen_units)):
      if i >= self.extra_units:
        break

      self.units.append(chosen_units[i])

    super().update_units()

  def _set_units_by_race(self):
    race = self.controller.get_player_race()

    if race == "terran":
      self.units = ["scv", "marine", "hellion", "hellbat", "medivac"]
    elif race == "protoss":
      self.units = ["probe", "zealot", "observer", "prism"]
    elif race == "zerg":
      self.units = ["drone", "zergling", "queen", "overlord", "overseer"]
