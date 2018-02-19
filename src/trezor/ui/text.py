from micropython import const
from trezor import ui
from trezor.ui import display

DISPLAY_WIDTH = const(240)
TEXT_HEADER_HEIGHT = const(48)
TEXT_LINE_HEIGHT = const(26)
TEXT_MARGIN_LEFT = const(14)

class Text(ui.Widget):

    def __init__(self, header_text, header_icon, *content, icon_color=ui.ORANGE_ICON, break_lines=False):
        self.header_text = header_text
        self.header_icon = header_icon
        self.icon_color = icon_color
        self.content = content
        self.breakl = break_lines

    def render(self):
        offset_x = TEXT_MARGIN_LEFT
        offset_y = TEXT_LINE_HEIGHT + TEXT_HEADER_HEIGHT
        style = ui.NORMAL
        fg = ui.FG
        bg = ui.BG
        ui.header(self.header_text, self.header_icon, ui.TITLE_GREY, ui.BG, self.icon_color)

        # line breaking by words
        def _line_render(w):
            words = w
            temp = words[0]
            offset_y = TEXT_LINE_HEIGHT + TEXT_HEADER_HEIGHT

            for i in range(1, len(words)):
                temp += ' ' + words[i]
                width = display.text_width(temp, style)
                if offset_x + width > DISPLAY_WIDTH:
                    temp = temp[:-len(words[i])]
                    ui.display.text(offset_x, offset_y, temp, style, fg, bg)
                    offset_y += TEXT_LINE_HEIGHT
                    temp = words[i]
                elif i == len(words) - 1:
                    ui.display.text(offset_x, offset_y, temp, style, fg, bg)


        for item in self.content:
            if isinstance(item, str):
                if self.breakl:
                    words = item.split(" ")
                    _line_render(words)
                else:
                    ui.display.text(offset_x, offset_y, item, style, fg, bg)
                    offset_y += TEXT_LINE_HEIGHT
            elif item == ui.MONO or item == ui.NORMAL or item == ui.BOLD:
                style = item
            else:
                fg = item

