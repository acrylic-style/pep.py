from common.log import logUtils as log
from common.redis import generalPubSubHandler
from objects import glob
from constants import serverPackets


class handler(generalPubSubHandler.generalPubSubHandler):
	def __init__(self):
		super().__init__()
		self.structure = {
			"userID": 0,
			"mainMenuIconID": 0
		}

	def handle(self, data):
		data = super().parseData(data)
		if data is None:
			return
		targetTokens = glob.tokens.getTokenFromUserID(data["userID"], ignoreIRC=True, _all=True)
		if targetTokens:
			if glob.banchoConf.config["menuIcon"] == "":
				log.warning("Tried to test an unknown main menu icon")
				return
			for x in targetTokens:
				x.enqueue(
					serverPackets.mainMenuIcon(glob.banchoConf.config["menuIcon"])
				)
