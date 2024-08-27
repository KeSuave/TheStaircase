from gui.pages.StepBase import StepBasePage


class StepThreePage(StepBasePage):
  def __init__(self, parent, controller, **kwargs):
    self.name = "stepthree"

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

    self.next_step = "chooseunits"
    self.next_step_after_choosing = "stepfour"
    self.next_step_extra_units = 1

    super().__init__(parent, controller, **kwargs)

  def set_race(self):
    race = self.controller.get_player_race()

    if race == "terran":
      self.units = ["scv", "marine", "hellion", "hellbat", "medivac"]
      self.race_suggestions = ["ccToOrbital", "ccEnergy"]
    elif race == "protoss":
      self.units = ["probe", "zealot", "observer", "prism"]
      self.race_suggestions = ["nexusEnergy"]
    elif race == "zerg":
      self.units = ["drone", "zergling", "queen", "overlord", "overseer"]
      self.race_suggestions = ["queenEnergy"]

    super().set_race()
