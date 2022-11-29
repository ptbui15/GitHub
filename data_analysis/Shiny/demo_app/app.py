from shiny import App, render, ui

# Import modules for plot rendering
import numpy as np
import matplotlib.pyplot as plt

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider("n", "N", 0, 100, 20),
        ),
        ui.panel_main(
            ui.output_plot("plot"),
        ),
    ),
)


def server(input, output, session):
    @output
    @render.plot(alt="A histogram")
    def plot():
        np.random.seed(19680801)
        x = 100 + 15 * np.random.randn(437)
        plt.hist(x, input.n(), density=True)


app = App(app_ui, server, debug=True)

# Execute
# python3 -m shiny run --port 8000 --reload "/Users/phongbui/Documents/GitHub/data_analysis/Shiny/demo_app/app.py"
