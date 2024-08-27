import asyncio
from threading import Event, Thread

import aiohttp

from stats.stats import get_stats_from_last_replay


class SC2:
  def __init__(self,
               player_name,
               race,
               replays_directory,
               on_status_update,
               on_valid_stats,
               is_valid_stats):
    self.player_name = player_name
    self.race = race
    self.replays_directory = replays_directory
    self.on_status_update = on_status_update
    self.on_valid_stats = on_valid_stats
    self.is_valid_stats = is_valid_stats

    self._active = False
    self._interval = 20 #seconds
    self._shutdown_event = Event()
    self._loop = asyncio.get_event_loop()
    self._thread = Thread(target=self._start_loop)

    self._status = "gameNotOpened"
    self._previously_in_match = False
    self._is_valid_stats_callback = None

    self._thread.start()

  def activate(self):
    self._active = True
    
    self._check_game()

  def deactivate(self):
    self._active = False

  def get_status(self):
    return self._status

  def shutdown(self):
    self._shutdown_event.set()
    self._loop.call_soon_threadsafe(self._loop.stop)
    self._thread.join()

  def _start_loop(self):
    asyncio.set_event_loop(self._loop)

    while not self._shutdown_event.is_set():
      self._loop.call_soon(self._loop.stop)
      self._loop.run_forever()

  def _check_game(self):
    if self._active:
      asyncio.run_coroutine_threadsafe(self._check_game_coroutine(), self._loop)

    self._loop.call_later(self._interval, self._check_game)

  async def _fetch_ui(self):
    try:
      async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:6119/ui') as response:
          return await response.json()
    except Exception as e:
      return {}

  async def _check_game_coroutine(self):
    if self._status == "analyzing":
      return

    ui = await self._fetch_ui()

    if "activeScreens" not in ui:
      self._update_status("gameNotOpened")

      return

    if len(ui["activeScreens"]) == 0:
      if self._status == "waitingForMatchEnd":
        return
      
      self._update_status("waitingForMatchEnd")
      self._previously_in_match = True
    else:
      self._update_status("waitingForMatch")

      if self._previously_in_match:
        self._previously_in_match = False

        self._analyze_last_match()

  def _analyze_last_match(self):
    self._update_status("analyzing")

    stats = get_stats_from_last_replay(self.replays_directory, self.player_name, self.race)

    if stats[3] == "ERROR_NONE" and self._is_valid_stats_callback(stats) and self.on_valid_stats is not None:
      self.on_valid_stats(stats)

    self._update_status("finishedAnalyzing")

  def _update_status(self, status):
    self._status = status

    if self._status_callback is not None:
      self.on_status_update()
