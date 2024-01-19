import arcade

TEXT_HEIGHT = 20
TEXT_WIDTH = 300

class TextPanel:
    def __init__(self, screen_width, screen_height):
        self.texts = []
        self.screen_width = screen_width
        self.screen_height = screen_height

    def set_text(self, idx, text):
        if len(self.texts) < idx+1:
            self.texts += [""] * (idx+1 - len(self.texts))

        self.texts[idx] = text

    def draw(self):
        px = self.screen_width - (TEXT_WIDTH/2)
        py = self.screen_height - (TEXT_HEIGHT/2)
        arcade.draw_rectangle_filled(px,py,TEXT_WIDTH+20, 40*TEXT_HEIGHT, (50, 50, 50, 150))

        for idx in range( len(self.texts)):
            x = self.screen_width - TEXT_WIDTH
            y = self.screen_height - (idx * TEXT_HEIGHT) - TEXT_HEIGHT
            arcade.draw_text(self.texts[idx], x, y, arcade.color.WHITE, bold=False, font_size=12)
