# TODO: Rewrite this shit
from common import generalUtils
from constants import serverPackets
from objects import glob
from common.log import logUtils as log


class banchoConfig:
	"""
	Class that loads settings from bancho_settings db table
	"""

	config = {"banchoMaintenance": False, "freeDirect": True, "menuIcon": ""}

	def __init__(self, loadFromDB = True):
		"""
		Initialize a banchoConfig object

		loadFromDB -- if True, load values from db. If False, don't load values. Optional.
		"""
		if loadFromDB:
			try:
				self.loadSettings()
			except:
				raise


	def loadSettings(self):
		self.config["banchoMaintenance"] = glob.conf.config["bancho"]["maintenance"]
		self.config["freeDirect"] = glob.conf.config["bancho"]["freedirect"]
		mainMenuIconId = glob.conf.config["bancho"]["menuiconfileid"]
		mainMenuIconUrl = glob.conf.config["bancho"]["menuiconurl"]
		if mainMenuIconId is "" or mainMenuIconUrl is "":
			self.config["menuIcon"] = ""
		else:
			imageURL = "https://i.ppy.sh/{}.png".format(mainMenuIconId)
			self.config["menuIcon"] = "{}|{}".format(imageURL, mainMenuIconUrl)


	def setMaintenance(self, maintenance):
		"""
		Turn on/off bancho maintenance mode. Write new value to db too

		maintenance -- if True, turn on maintenance mode. If false, turn it off
		"""
		self.conf.config["bancho"]["maintenance"] = "{}".format(maintenance)

	def reload(self):
		# Reload settings from bancho_settings
		glob.banchoConf.loadSettings()

		# Reload channels too
		glob.channels.loadChannels()

		# And chat filters
		glob.chatFilters.loadFilters()

		# Send new channels and new bottom icon to everyone
		glob.streams.broadcast("main", serverPackets.mainMenuIcon(glob.banchoConf.config["menuIcon"]))
		glob.streams.broadcast("main", serverPackets.channelInfoEnd())
		for key, value in glob.channels.channels.items():
			if value.publicRead and not value.hidden:
				glob.streams.broadcast("main", serverPackets.channelInfo(key))