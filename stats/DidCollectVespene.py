class DidCollectVespene:
  name = "DidCollectVespene"

  def handleInitGame(self, event, replay):
    for player in replay.players:
      player.did_collect_vespene = False

  def handlePlayerStatsEvent(self, event, _replay):
    if event.vespene_current > 0:
      event.player.did_collect_vespene = True
