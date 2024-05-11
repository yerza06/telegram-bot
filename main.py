from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

print(config['DEFAULT']['CompressionLevel'])

# Hello Master Git