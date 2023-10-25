
RED = (255,0,0)
WHITE = (255,255,255)

SCALE = 1.5
WEAPON_SCALE = 0.2
SLASH_SPEED = 5

BG = (0,0,0)

TILE_SIZE = 34*SCALE
FIRST_LEVEL_MAP = [
'                                            ',
'                                            ',
'                                           ',
'                                           ',
'00                                        ',
'01            P                           ',
'010          00                           ',
'0111110      011110     S                  ',
'                  1111111                 ',
'   S                                    S    ',
'11111111111             S               1111111111 ',
'22222222222           00000                   01111111111110',
'22322232322111                       S      111111111',
'01111111111111000000000000000000000000000000000'

]

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = len(FIRST_LEVEL_MAP) * TILE_SIZE