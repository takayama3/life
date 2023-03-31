import pygame


class Area:
    def __init__(self, window, x, y, width, height,
                 text='',
                 background_color=(189, 189, 189),
                 border_color=(70, 70, 70),
                 border=2,
                 border_radius=0,
                 font_color=(10, 10, 10),
                 font_family='arial',
                 font_size=16
                 ):

        self.window = window
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        self.background_color = background_color
        self.border_color = border_color
        self.border = border
        self.border_radius = border_radius
        self.font_color = font_color
        self.font_family = font_family
        self.font_size = font_size

    def draw_border(self):
        pygame.draw.rect(self.window, self.border_color, self.rect, self.border, border_radius=self.border_radius)

    def draw_text(self):
        font = pygame.font.SysFont(self.font_family, self.font_size)
        s = 0
        for text in self.text.split('\n'):
            text_surface = font.render(text, True, self.font_color)
            size = text_surface.get_rect().size
            s += size[1]

        i = 0
        for text in self.text.split('\n'):
            text_surface = font.render(text, True, self.font_color)
            size = text_surface.get_rect().size
            coords = [self.rect.x, self.rect.y]
            coords[0] += (self.rect.width - size[0]) // 2
            coords[1] += (self.rect.height - s) // 2 + i
            self.window.blit(text_surface, coords)
            i += size[1]

    def draw(self):
        pygame.draw.rect(self.window, self.background_color, self.rect, border_radius=self.border_radius)
        self.draw_border()
        self.draw_text()

    def collidepoint(self, x, y):
        if self.rect.x <= x <= self.rect.x + self.rect.width:
            if self.rect.y <= y <= self.rect.y + self.rect.height:
                return True
        return False
