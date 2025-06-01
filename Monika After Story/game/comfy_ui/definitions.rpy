################################################################################
#
# Copyright (c) 2020–2021 Dominus Iniquitatis <zerosaiko@gmail.com>
#
# See LICENSE file for the licensing information
#
################################################################################
define comfy_ui.common.font_regular     = "comfy_ui/fonts/Nunito-SemiBold.ttf"
define comfy_ui.common.font_italic      = "comfy_ui/fonts/Nunito-SemiBoldItalic.ttf"
define comfy_ui.common.font_bold        = "comfy_ui/fonts/Nunito-Bold.ttf"
define comfy_ui.common.font_bold_italic = "comfy_ui/fonts/Nunito-BoldItalic.ttf"
define comfy_ui.common.font             = FontGroup().add(
    comfy_ui.common.font_regular                 , 0x0020, 0x00ff).add( # Main
    "mod_assets/font/SourceHanSansK-Regular.otf" , 0xac00, 0xd7a3).add( # Korean
    "mod_assets/font/SourceHanSansSC-Regular.otf", 0x4e00, 0x9faf).add( # Simplified chinese
    "mod_assets/font/mplus-2p-regular.ttf"       , 0x3000, 0x4dff).add( # Japanese and others
    "gui/font/Aller_Rg.ttf"                      , 0x0000, 0xffff)      # Fallback
define comfy_ui.common.font_kerning     = 0.0
define comfy_ui.common.font_size        = 20

define comfy_ui.menu_font         = "gui/font/RifficFree-Bold.ttf"
define comfy_ui.menu_font_kerning = 0.0

define comfy_ui.menu_title.font_size      = 38
define comfy_ui.menu_title.light.color    = "#ffffff"
define comfy_ui.menu_title.light.outlines = [(6, "#8d764c", 0, 0), (3, "#8d764c", 2, 2)]
define comfy_ui.menu_title.dark.color     = "#faeddb"
define comfy_ui.menu_title.dark.outlines  = [(6, "#5e4d2f", 0, 0), (3, "#5e4d2f", 2, 2)]

define comfy_ui.menu_label.font_size      = 24
define comfy_ui.menu_label.light.color    = "#ffffff"
define comfy_ui.menu_label.light.outlines = [(3, "#8d764c", 0, 0), (1, "#8d764c", 1, 1)]
define comfy_ui.menu_label.dark.color     = "#faeddb"
define comfy_ui.menu_label.dark.outlines  = [(3, "#5e4d2f", 0, 0), (1, "#5e4d2f", 1, 1)]

define comfy_ui.menu_text.font_size      = 16
define comfy_ui.menu_text.light.color    = "#373737"
define comfy_ui.menu_text.light.outlines = []
define comfy_ui.menu_text.dark.color     = "#e2b44c"
define comfy_ui.menu_text.dark.outlines  = []

define comfy_ui.menu_button_text.font_size                  = 24
define comfy_ui.menu_button_text.light.color                = "#ffffff"
define comfy_ui.menu_button_text.light.idle_outlines        = [(4, "#8d764c", 0, 0), (2, "#8d764c", 2, 2)]
define comfy_ui.menu_button_text.light.hover_outlines       = [(4, "#f2ba00", 0, 0), (2, "#f2ba00", 2, 2)]
define comfy_ui.menu_button_text.light.insensitive_outlines = [(4, "#ffd487", 0, 0), (2, "#ffd487", 2, 2)]
define comfy_ui.menu_button_text.dark.color                 = "#faeddb"
define comfy_ui.menu_button_text.dark.idle_outlines         = [(4, "#5e4d2f", 0, 0), (2, "#5e4d2f", 2, 2)]
define comfy_ui.menu_button_text.dark.hover_outlines        = [(4, "#9e8760", 0, 0), (2, "#9e8760", 2, 2)]
define comfy_ui.menu_button_text.dark.insensitive_outlines  = [(4, "#9c8a6f", 0, 0), (2, "#9c8a6f", 2, 2)]

define comfy_ui.music_menu_button_text.font                       = "mod_assets/font/mplus-2p-regular.ttf"
define comfy_ui.music_menu_button_text.font_kerning               = 0.0
define comfy_ui.music_menu_button_text.font_size                  = 24
define comfy_ui.music_menu_button_text.light.color                = "#ffffff"
define comfy_ui.music_menu_button_text.light.idle_outlines        = [(3, "#8d764c", 0, 0), (1, "#8d764c", 1, 1)]
define comfy_ui.music_menu_button_text.light.hover_outlines       = [(3, "#f2ba00", 0, 0), (1, "#f2ba00", 1, 1)]
define comfy_ui.music_menu_button_text.light.insensitive_outlines = [(3, "#ffd487", 0, 0), (1, "#ffd487", 1, 1)]
define comfy_ui.music_menu_button_text.dark.color                 = "#faeddb"
define comfy_ui.music_menu_button_text.dark.idle_outlines         = [(3, "#5e4d2f", 0, 0), (1, "#5e4d2f", 1, 1)]
define comfy_ui.music_menu_button_text.dark.hover_outlines        = [(3, "#9e8760", 0, 0), (1, "#9e8760", 1, 1)]
define comfy_ui.music_menu_button_text.dark.insensitive_outlines  = [(3, "#9c8a6f", 0, 0), (1, "#9c8a6f", 1, 1)]

define comfy_ui.confirm_prompt_text.light.color    = "#373737"
define comfy_ui.confirm_prompt_text.light.outlines = []
define comfy_ui.confirm_prompt_text.dark.color     = "#dcb56b"
define comfy_ui.confirm_prompt_text.dark.outlines  = []

define comfy_ui.dialogue_text.vertical_offset = -3
define comfy_ui.dialogue_text.line_spacing    = -1
define comfy_ui.dialogue_text.color           = "#f7f7f7"
define comfy_ui.dialogue_text.outlines        = [(2, "#191919", 0, 0)]

define comfy_ui.history_name.color    = "#f7f7f7"
define comfy_ui.history_name.outlines = [(2, "#191919", 0, 0)]

define comfy_ui.history_text.color    = "#ffffff"
define comfy_ui.history_text.outlines = [(2, "#191919", 0, 0)]

define comfy_ui.quick_button_text.font_size               = 14
define comfy_ui.quick_button_text.light.idle_color        = "#393021"
define comfy_ui.quick_button_text.light.hover_color       = "#ffd27b"
define comfy_ui.quick_button_text.light.selected_color    = "#ffffff"
define comfy_ui.quick_button_text.light.insensitive_color = "#837765"
define comfy_ui.quick_button_text.light.outlines          = []
define comfy_ui.quick_button_text.dark.idle_color         = "#deb86e"
define comfy_ui.quick_button_text.dark.hover_color        = "#fcead1"
define comfy_ui.quick_button_text.dark.selected_color     = "#ffefda"
define comfy_ui.quick_button_text.dark.insensitive_color  = "#837765"
define comfy_ui.quick_button_text.dark.outlines           = []

define comfy_ui.button_text.light.idle_color        = "#373737"
define comfy_ui.button_text.light.hover_color       = "#e6b855"
define comfy_ui.button_text.light.selected_color    = "#877558"
define comfy_ui.button_text.light.insensitive_color = "#aaaaaa7f"
define comfy_ui.button_text.light.outlines          = []
define comfy_ui.button_text.dark.idle_color         = "#dcb56b"
define comfy_ui.button_text.dark.hover_color        = "#f7c763"
define comfy_ui.button_text.dark.selected_color     = "#877558"
define comfy_ui.button_text.dark.insensitive_color  = "#7373737f"
define comfy_ui.button_text.dark.outlines           = []

define comfy_ui.option_button_text.font                    = "gui/font/Halogen.ttf"
define comfy_ui.option_button_text.font_kerning            = 0.0
define comfy_ui.option_button_text.font_size               = 24
define comfy_ui.option_button_text.light.idle_color        = "#aaaaaa"
define comfy_ui.option_button_text.light.hover_color       = "#9b845e"
define comfy_ui.option_button_text.light.selected_color    = "#8b754e"
define comfy_ui.option_button_text.light.insensitive_color = "#aaaaaa7f"
define comfy_ui.option_button_text.dark.idle_color         = "#737373"
define comfy_ui.option_button_text.dark.hover_color        = "#ceaa67"
define comfy_ui.option_button_text.dark.selected_color     = "#aa9168"
define comfy_ui.option_button_text.dark.insensitive_color  = "#7373737f"

define comfy_ui.fancy_check_button.light.idle_background_color     = "#00000000"
define comfy_ui.fancy_check_button.light.hover_background_color    = "#f7c96d"
define comfy_ui.fancy_check_button.light.selected_background_color = "#f7c96d"
define comfy_ui.fancy_check_button.dark.idle_background_color      = "#00000000"
define comfy_ui.fancy_check_button.dark.hover_background_color     = "#a69375"
define comfy_ui.fancy_check_button.dark.selected_background_color  = "#a69375"

define comfy_ui.fancy_check_button_text.font                    = "gui/font/Halogen.ttf"
define comfy_ui.fancy_check_button_text.font_kerning            = 0.0
define comfy_ui.fancy_check_button_text.font_size               = 24
define comfy_ui.fancy_check_button_text.light.idle_color        = "#bebebe"
define comfy_ui.fancy_check_button_text.light.hover_color       = "#373737"
define comfy_ui.fancy_check_button_text.light.selected_color    = "#373737"
define comfy_ui.fancy_check_button_text.dark.idle_color         = "#bebebe"
define comfy_ui.fancy_check_button_text.dark.hover_color        = "#d8b882"
define comfy_ui.fancy_check_button_text.dark.selected_color     = "#d8b882"

define comfy_ui.button_height_adjustment = -4

define comfy_ui.scrollable_menu_button_spacing = 6
define comfy_ui.choice_button_spacing          = 12
define comfy_ui.talk_button_spacing            = 16
define comfy_ui.hotkey_button_spacing          = 5

define comfy_ui.input_caret_color = "#8d764c"
