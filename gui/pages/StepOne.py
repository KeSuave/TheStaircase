from gui.pages.StepBase import StepBasePage

class StepOnePage(StepBasePage):
  def __init__(self, parent, controller, **kwargs):
    self.name = "stepone"

    self.rules = ["mineMinerals",
                  "noGas",
                  "minimapAttack",
                  "noBabysitting",
                  "noCommandCard",
                  "unitsPerProduction",
                  "productionPerBase"]
    
    self.general_suggestions = ["haveFun",
                                "focus",
                                "screenMovement",
                                "screenPositions",
                                "hotkeys",
                                "threeBasesNoGas",
                                "aggressive",
                                "economy"]

    self.next_step = "steptwo"

    super().__init__(parent, controller, **kwargs)

  def set_race(self):
    race = self.controller.get_player_race()

    if race == "terran":
      self.units = ["scv", "marine"]
      self.race_suggestions = ["ccToOrbital", "ccEnergy"]
    elif race == "protoss":
      self.units = ["probe", "zealot"]
      self.race_suggestions = ["nexusEnergy"]
    elif race == "zerg":
      self.units = ["drone", "zergling", "queen", "overlord"]
      self.race_suggestions = ["queenEnergy"]
      
    super().set_race()