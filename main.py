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
    H_LINES_SPACING = .15
    horizontal_lines = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.create_vertical_lines()
        self.create_horizontal_lines()
        Clock.schedule_interval(self.update, 1/60)

    def create_vertical_lines(self):
        with self.canvas:
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def create_horizontal_lines(self):
        with self.canvas:
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def get_line_x_from_index(self, index):
        center_x = self.perspective_point_x
        spacing_x = self.width * self.V_LINES_SPACING
        x = (center_x - spacing_x/2) - spacing_x * index
        return x

    def update_vertical_lines(self):
        start_index = int(- self.V_NB_LINES / 2)

        for i in range(start_index, start_index+self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        y = index * spacing_y
        return y

    def update_horizontal_lines(self):
        start_index = int(- self.V_NB_LINES / 2)
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


class PianoApp(App):
    pass


PianoApp().run()
