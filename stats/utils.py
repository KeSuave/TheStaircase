def get_unique_units(player):
  units = []

  for unit in player.units:
    if not unit.is_army and not unit.is_worker:
      continue

    name = unit.name.lower()

    # the following just to match the image names
    if name == "battlehelliom":
      name = "hellbat"
    elif name == "siegetank":
      name = "tank"
    elif name == "widowmine":
      name = "mine"
    elif name == "warpprism":
      name = "prism"
    elif name == "darktemplar":
      name = "dt"
    elif name == "hightemplar":
      name = "ht"
    elif name == "voidray":
      name = "void"
    elif name == "swarmhost":
      name = "swarm"
    elif name == "broodlord":
      name = "brood"

    if name not in units:
      units.append(name)

  return units
