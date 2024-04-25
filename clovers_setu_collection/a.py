import re

r"来(.*)[张份](.+)$"

print(re.match(r"来(.*)[张份]([rR]18)?(.+)$", "来10张r18色图").groups())
