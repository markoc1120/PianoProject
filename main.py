import random
from kivy.app import App
from kivy.graphics import Color, Line, Quad
from kivy.properties import NumericProperty, Clock
from kivy.uix.relativelayout import RelativeLayout


class MainWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 6
    V_LINES_SPACING = .2
    vertical_lines = []

    H_NB_LINES = 8
    H_LINES_SPACING = .1
    horizontal_lines = []

    NB_TILES = 16
    tiles = []
    tiles_coordinates = []

    SPEED = .4
    current_offset_y = 0
    current_y_loop = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.create_vertical_lines()
        self.create_horizontal_lines()
        self.create_tiles()
        self.pre_fill_tiles()
        self.create_tiles_coordinates()
        Clock.schedule_interval(self.update, 1/60)

    def create_vertical_lines(self):
        with self.canvas:
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def create_horizontal_lines(self):
        with self.canvas:
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def create_tiles(self):
        with self.canvas:
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())

    def pre_fill_tiles(self):
        for i in range(10):
            self.tiles_coordinates.append((0, i))

    def create_tiles_coordinates(self):
        last_y = 0
        last_x = 0
        # clean the coordinates that are out of the screen
        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_y = last_coordinates[1] + 1
            last_x = last_coordinates[0]

        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(0, 2)

            start_index = -int(self.V_NB_LINES / 2) + 1
            end_index = start_index + self.V_NB_LINES - 2
            if last_x <= start_index:
                r = 1

            if last_x >= end_index:
                r = 2

            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            elif r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))

            self.tiles_coordinates.append((last_x, last_y))
            last_y += 1

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_tiles(self):
        for i in range(0, self.NB_TILES):
            tile_coordinates = self.tiles_coordinates[i]
            tile = self.tiles[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0]+1, tile_coordinates[1]+1)

            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def get_line_x_from_index(self, index):
        center_x = self.perspective_point_x
        spacing_x = self.width * self.V_LINES_SPACING
        offset = index - 0.5
        x = center_x + offset * spacing_x
        return x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        y = index * spacing_y - self.current_offset_y
        return y

    def update_vertical_lines(self):
        start_index = int(- self.V_NB_LINES / 2) + 1

        for i in range(start_index, start_index+self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_horizontal_lines(self):
        start_index = int(- self.V_NB_LINES / 2) + 1
        end_index = start_index + self.V_NB_LINES - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        self.update_vertical_lines()
        self.update_horizontal_lines()
        print(len(self.tiles), len(self.tiles_coordinates))
        self.update_tiles()

        spacing_y = self.H_LINES_SPACING * self.height
        speed_y = self.SPEED * self.height / 100
        self.current_offset_y += speed_y

        while self.current_offset_y > spacing_y:
            self.current_offset_y -= spacing_y
            self.current_y_loop += 1
            self.create_tiles_coordinates()


class PianoApp(App):
    pass


PianoApp().run()
