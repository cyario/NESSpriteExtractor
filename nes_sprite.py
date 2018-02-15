import binascii
import sys
from PIL import Image

NES_HEADER_SIZE = 0x0010;
RPG_ROM_SIZE = 0x4000;
CHR_ROM_SIZE = 0x2000;
CANVAS_WIDTH = 800;

DEFAULT_PALETTE = [
    (0xff, 0xff, 0xff),
    (0x75, 0x75, 0x75),
    (0xbc, 0xbc, 0xbc),
    (0x00, 0x00, 0x00),
]

romPath = sys.argv[1]

with open(romPath, 'rb') as f:
	hexdata = binascii.hexlify(f.read())
	romHexList = map(''.join, zip(hexdata[::2], hexdata[1::2]))

rpgRomPage = int(romHexList[4], 16)
chrRomPage = int(romHexList[5], 16)
chrRomSart = NES_HEADER_SIZE + rpgRomPage * RPG_ROM_SIZE;
spritesPerRow = CANVAS_WIDTH / 8;
spritesNum = CHR_ROM_SIZE * chrRomPage / 16;
rowNum = ~~(spritesNum / spritesPerRow) + 1;

height = rowNum * 8;
width = CANVAS_WIDTH


def buildSprite(spriteNum):
	sprite = [[0 for i in range(8)] for j in range(8)]
 	for i in range(16):
		for j in range(8):
			if int(romHexList[chrRomSart + spriteNum * 16 + i], 16) & (0x80 >> j):
				sprite[i % 8][j] += 0x01 << (i / 8)
	return sprite

def renderSprite(canvas, sprite, spriteNum):
	for i in range(8):
		for j in range(8):
			x = (j + (spriteNum % spritesPerRow) * 8)
			y = (i + ~~(spriteNum / spritesPerRow) * 8)
			canvas.putpixel((x,y), DEFAULT_PALETTE[sprite[i][j]])	

canvas = Image.new('RGB', (width, height))
for i in range(spritesNum):
	sprite = buildSprite(i)
	renderSprite(canvas, sprite, i);

canvas.show()
canvas.save('sprite.png')
