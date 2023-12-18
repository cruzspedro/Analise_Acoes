import flet as ft
import time

GOLL4: list = [(1, 9.06),
               (2, 8.35),
               (3, 10.17),
               (4, 8.93),
               (5, 9.60),
               (6, 8.31),
               (7, 7.34),
               (8, 7.65),
               (9, 5.53),
               (10, 6.66),
               (11, 6.65),
               (12, 7.44)]
PETR4: list = [(1, 27.93),
               (2, 34.15),
               (3, 33.22),
               (4, 29.79),
               (5, 29.80),
               (6, 26.65),
               (7, 24.5),
               (8, 26.06),
               (9, 25.23),
               (10, 23.4),
               (11, 23.7),
               (12, 24.6)]
BVSP: list = [(1, 98542.0),
              (2, 103165.0),
              (3, 109523.0),
              (4, 110037.0),
              (5, 116037.0),
              (6, 112486.0),
              (7, 110031.0),
              (8, 113532.0),
              (9, 104932.0),
              (10, 101882.0),
              (11, 104432.0),
              (12, 107724.3)]
BZF: list = [(1, 114.8),
             (2, 110.0),
             (3, 96.4),
             (4, 87.9),
             (5, 94.8),
             (6, 85.4),
             (7, 85.9),
             (8, 83.8),
             (9, 79.7),
             (10, 79.5),
             (11, 75.3)]

class TimeChart(ft.UserControl):
    def __init__(self):
        self.data_points: list = []
        self.points: list = PETR4

        self.chart: ft.Control = ft.LineChart(
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.WHITE),
            expand=True,
            min_y=int(min(self.points, key=lambda y: y[1])[1]),
            max_y=int(max(self.points, key=lambda y: y[1])[1]),
            min_x=int(min(self.points, key=lambda x: x[0])[0]),
            max_x=int(max(self.points, key=lambda x: x[0])[0]) + 1,
            left_axis=ft.ChartAxis(labels_size=50),
            bottom_axis=ft.ChartAxis(labels_size=60, labels_interval=1, ),
        )

        self.line_chart: ft.Control = ft.LineChartData(
            color=ft.colors.GREEN_200,
            stroke_width=2,
            curved=True,
            stroke_cap_round=True,
            below_line_gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.with_opacity(0.25, ft.colors.GREEN_200), "transparent"],

            )
        )
        super().__init__()

    def get_buttons(self, btn, data):
        return ft.ElevatedButton(
            btn,
            color="white",
            width=100,
            height=40,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=6)},
            ),
            bgcolor='teal600',
            data=data,
            on_click=lambda e: self.toggle_data(e),
        )

    def toggle_data(self, e):
        self.switch_list(e)
        self.chart.data_series = [self.line_chart]
        self.get_data_points()

    def switch_list(self, e):
        if e.control.data == 'gol':
            self.points = GOLL4

        if e.control.data == 'pet':
            self.points = PETR4

        if e.control.data == 'bvsp':
            self.points = BVSP

        if e.control.data == 'bzf':
            self.points = BZF

        self.data_points = []
        self.chart.data_series = []
        self.line_chart.data_points = self.data_points

        self.chart.min_y = int(min(self.points, key=lambda y: y[1])[1])
        self.chart.max_y = int(max(self.points, key=lambda y: y[1])[1])
        self.chart.min_x = int(min(self.points, key=lambda x: x[0])[0])
        self.chart.max_x = int(max(self.points, key=lambda x: x[0])[0])+1

        self.chart.update()
        time.sleep(0.5)

    def create_data_points(self, x, y):
        return ft.LineChartDataPoint(
            x,
            y,
            selected_below_line=ft.ChartPointLine(
                width=0.5, color="white", dash_pattern=[2, 4]
            ),
            selected_point=ft.ChartCirclePoint(stroke_width=1),
        )

    def get_data_points(self):
        for x, y in self.points:
            self.data_points.append(self.create_data_points(x, y))
            self.chart.update()
            time.sleep(0.05)

    def build(self):
        self.line_chart.data_points = self.data_points
        self.chart.data_series = [self.line_chart]

        return ft.Column(
            horizontal_alignment='center',
            controls=[
                ft.Text(
                    "valores das ações no período indicado",
                    size=16,
                    weight='bold',
                ),
                self.chart,
            ]
        )


def main(page: ft.page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = "center"
    chart = TimeChart()
    page.add(
        ft.Column(
            expand=True,
            alignment='center',
            horizontal_alignment='center',
            controls=[
                ft.Container(
                    expand=1,
                    bgcolor=ft.colors.with_opacity(0.025, ft.colors.WHITE10),
                    border_radius=6,
                    content=ft.Row(
                        alignment='center',
                        controls=[
                            chart.get_buttons("GOLL4", 'gol'),
                            chart.get_buttons("PETR4", 'pet'),
                            chart.get_buttons("BVSP", 'bvsp'),
                            chart.get_buttons("BZF", 'bzf'),
                        ],
                    )
                ),
                ft.Container(
                    expand=4,
                    bgcolor=ft.colors.with_opacity(0.025, ft.colors.WHITE10),
                    border_radius=6,
                    content=chart,
                )
            ]
        )
    )

    page.update()
    chart.get_data_points()


if __name__ == "__main__":
    ft.flet.app(target=main)
