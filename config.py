import ConfigParser
import os

def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/all.conf'
    config.read(path)
    return config.get(section, key)

def setConfig(setion, key, value):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/all.conf'
    config.read(path)
    with open(path, "w") as f:
        config.set(section=setion, option=key, value=value)
        config.write(f)
