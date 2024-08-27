from PIL import Image

APP_WIDTH = 1280
APP_HEIGHT = 720

SPECIAL_FONT = ("Starcraft Normal", 32)
NORMAL_FONT = ("ShareTech", 20)

UPPER_FRAME_COLOR = "gray20"

BG_IMAGE = Image.open("assets/images/bg.jpg")
BG_IMAGE_RATIO = BG_IMAGE.width / BG_IMAGE.height

TERRAN_IMAGE = Image.open("assets/images/terran.jpg")
PROTOSS_IMAGE = Image.open("assets/images/protoss.jpg")
ZERG_IMAGE = Image.open("assets/images/zerg.jpg")

ARROW = "→ "

MIN_MATCHES_TO_PROGRESS = 5
MIN_SQ_TO_PASS = 100

DEFAULT_CONFIG = {
  "page": "",
  "language": "enUS",
  "player_name": "",
  "race": "",
  "replays": "",
  "stepone_terran_sqs": [],
  "stepone_protoss_sqs": [],
  "stepone_zerg_sqs": [],
  "steptwo_terran_sqs": [],
  "steptwo_protoss_sqs": [],
  "steptwo_zerg_sqs": [],
  "stepthree_terran_sqs": [],
  "stepthree_protoss_sqs": [],
  "stepthree_zerg_sqs": [],
  "stepfour_terran_sqs": [],
  "stepfour_protoss_sqs": [],
  "stepfour_zerg_sqs": [],
  "stepfive_terran_sqs": [],
  "stepfive_protoss_sqs": [],
  "stepfive_zerg_sqs": [],
  "stepsix_terran_sqs": [],
  "stepsix_protoss_sqs": [],
  "stepsix_zerg_sqs": []
}