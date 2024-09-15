import math
import os
import sc2reader
import metrics

from stats.DidCollectVespene import DidCollectVespene
from stats.utils import get_unique_units

sc2reader.engine.register_plugin(DidCollectVespene())

prev_last_replay = ""

def get_last_replay(replays_folder):
  files = os.listdir(replays_folder)

  replays = [file for file in files if file.endswith(".SC2Replay")]

  replays_times = [(os.stat(replays_folder + "/" + replay).st_mtime, replay) for replay in replays]

  replays_times.sort(reverse=True)

  return replays_times[0][1]

def get_stats_from_last_replay(replays_folder, player_name, race):
  replay_file = get_last_replay(replays_folder)

  global prev_last_replay

  if replay_file == prev_last_replay:
    return 0, [], "VESPENE_NO", "ERROR_SAME_REPLAY"

  replay = sc2reader.load_replay(replays_folder + "/" + replay_file)
  sq = 0
  units = []
  gas = "VESPENE_NO"
  error = "ERROR_NONE"

  """ if not replay.is_ladder:
    return sq, units, gas, "ERROR_NOT_LADDER"
  
  if replay.game_type != "1v1":
    return sq, units, gas, "ERROR_NOT_1V1" """

  for player in replay.players:
    if player.name == player_name:
      sq = math.floor(player.metrics.avg_sq())
      units = get_unique_units(player)

      if player.did_collect_vespene:
        gas = "VESPENE_YES"

      if player.play_race.lower() != race:
        error = "ERROR_WRONG_RACE"

      break
  
  return sq, units, gas, error
