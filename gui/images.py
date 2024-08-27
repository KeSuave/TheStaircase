import customtkinter as ctk

from PIL import Image

TERRAN_UNITS = ["scv",
                "marine",
                "hellion",
                "hellbat",
                "medivac",
                "marauder",
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

PROTOSS_UNITS = ["probe",
                 "zealot",
                 "observer",
                 "prism",
                 "stalker",
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

ZERG_UNITS = ["drone",
              "zergling",
              "queen",
              "overlord",
              "overseer",
              "roach",
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

UNIT_IMAGES = {}

for unit in TERRAN_UNITS + PROTOSS_UNITS + ZERG_UNITS:
  UNIT_IMAGES[unit] = ctk.CTkImage(Image.open(f"assets/images/{unit}.jpg"), size=(76, 76))

UNIT_IMAGES["nounit"] = ctk.CTkImage(Image.open("assets/images/nounit.png"), size=(76, 76))
