init -2 python:
    os_blk = False
    print("⚠️ Developer build! Please do not put this file in the end-user distributive! ⚠️")

init python:
    yaru = {"default" : [("gui/mouse/yaru/yaru_arrow.png", 7, 7)], "hand" : [("gui/mouse/yaru/yaru_hand.png", 12, 6)], "drag" : [("gui/mouse/yaru/yaru_drag.png", 17, 16)]}
    config.mouse = yaru if not renpy.android else None

define config.atl_start_on_show = False
define config.gl2 = True
