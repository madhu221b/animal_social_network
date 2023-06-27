import os
import pickle
import networkx as nx
import pickle
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSlider, QSpacerItem, QSizePolicy, QGridLayout
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize

from src.static import PageState, GRAPH_VERSION_FOLDER, GRAPH_DATA
from src.graph import Graph
from src.gui.social_graph.graph import GraphCanvas
from ..custom_buttons import BlueArrowButton

matplotlib.use("Qt5Agg")


class GraphEvolution(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.evolution_id = self.evolutions.index(PageState.version)  # Current evolution index

        # Background utilities
        self.graph_gui = GraphCanvas(parent)
        self.graph_gui.highligh_node_width = 2.
        self.graph_gui.normal_node_width = 0.2
        self.graph_gui.highligh_edge_width = 2.5
        self.graph_gui.normal_edge_width = 0.5
        self.info_tab = QLabel(text="Placeholder", alignment=Qt.AlignmentFlag.AlignCenter)

        # Precalculate changes over time
        self._calculate_graph_changes()

        # Load current graph information and replacing the placeholder
        self.refresh()

        # Building up graphical interface on generated information
        self.build_layout()

    def _calculate_graph_changes(self):

        graphs = {}
        animal_folder = os.path.join(GRAPH_VERSION_FOLDER, PageState.id)
        for evolution in self.evolutions:
            if evolution == "default":
                current_file = GRAPH_DATA[PageState.category][PageState.id]["path"]
                graph = Graph.from_graphml(current_file)
            else:
                current_file = os.path.join(animal_folder, evolution + ".pkl")
                graph = Graph.from_pkl(current_file)
            graphs[evolution] = graph

        self._avg_degrees = {e: graphs[e].avg_degree for e in self.evolutions}
        self._avg_coeffs = {e: graphs[e].avg_coeff for e in self.evolutions}
        self._n_nodes = {e: graphs[e].n_nodes for e in self.evolutions}

        # Setting up differences between graphs
        self.differences = {"default": graphs['default'].difference_to(None)}
        for prev_evolution, evolution in zip(self.evolutions[:-1], self.evolutions[1:]):
            self.differences[evolution] = graphs[evolution].difference_to(graphs[prev_evolution])

    # ===============================================
    # GUI build up
    # ===============================================

    def build_layout(self):

        # All layouts
        self.main_layout = QVBoxLayout()
        self.hlayout = QHBoxLayout()
        self.content_layout = QGridLayout()  # Changed to QGridLayout
        self.hlayout_below = QHBoxLayout()
        self.content_layout_below = QVBoxLayout()

        # Set styling of info tab
        self.info_tab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_tab.setFont(QFont("", 16))
        self.info_tab.setFixedHeight(40)

        # Upper page: Left arrow + graph + right arrow
        self._create_prev_button()
        self.content_layout.addWidget(self.info_tab, 0, 0, 1, 2)
        self.content_layout.addWidget(self.graph_gui, 1, 0)  # Graph at top-left

        # Create additional plots
        self.top_right_plot = self._create_plot(self._avg_degrees, "Mean degree")
        self.bottom_left_plot = self._create_plot(self._avg_coeffs, "Mean clustering coefficient")
        self.bottom_right_plot = self._create_plot(self._n_nodes, "Number of nodes")

        # Add plots to the layout
        self.content_layout.addWidget(self.top_right_plot, 1, 1)
        self.content_layout.addWidget(self.bottom_left_plot, 2, 0)
        self.content_layout.addWidget(self.bottom_right_plot, 2, 1)

        self.content_layout.setRowStretch(0, 1)  # Info tab
        self.content_layout.setRowStretch(1, 2)  # Graph and top-right plot
        self.content_layout.setRowStretch(2, 2)  # Bottom-left and bottom-right plots
        self.content_layout.setColumnStretch(0, 2)  # Graph and bottom-left plot
        self.content_layout.setColumnStretch(1, 2)  # Top-right and bottom-right plots

        self.hlayout.addLayout(self.content_layout)
        self._create_next_button()

        # Upper and bottom page added together
        self.main_layout.addLayout(self.hlayout)

        # Create a slider
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.n_evolutions - 1)
        self.slider.setValue(self.evolution_id)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)

        # Connect the valueChanged signal to a slot function
        self.slider.valueChanged.connect(self._slider_value_changed)

        # Create a layout for the labels
        labels_layout = QHBoxLayout()

        # Add labels to the layout with stretchable spacers in between
        for i, evolution in enumerate(self.evolutions):
            label = QLabel(str(evolution))
            labels_layout.addWidget(label)
            if i < len(self.evolutions) - 1:  # Don't add a spacer after the last label
                labels_layout.addItem(
                    QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Add the slider and the labels layout to the main layout
        self.main_layout.addWidget(self.slider)
        self.main_layout.addLayout(labels_layout)

        self.setLayout(self.main_layout)

        # Disable buttons if first or last evolution indexed
        self._update_button_states()

    def _create_next_button(self):
        """Create a next button to this window"""
        self.next_button = BlueArrowButton(QIcon("res/icons/right_white.png"), "", self)
        self.next_button.clicked.connect(self._next_button_on_click)
        self.hlayout.addWidget(self.next_button)

    def _create_prev_button(self):
        """Create a next button to this window"""
        self.prev_button = BlueArrowButton(QIcon("res/icons/left_white.png"), "", self)
        self.prev_button.clicked.connect(self._prev_button_on_click)
        self.hlayout.addWidget(self.prev_button)

    def _create_plot(self, y_values, title):
        """Create a line plot with plot with the given y values and title."""
        x_values = list(y_values.keys())
        fig = Figure(dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x_values, list(y_values.values()), marker='o')
        ax.set_title(title)
        ax.set_xlabel("Evolution")
        ax.set_ylabel(title)
        # Add a vertical line at the current evolution
        line = ax.axvline(x=self.evolutions[self.evolution_id], color='r', linestyle='--')
        canvas = FigureCanvasQTAgg(fig)
        # Store the line and axes for later use
        canvas.ax = ax
        canvas.line = line

        # Add margins so xlabel and ylabel fits into the space
        fig.subplots_adjust(left=0.2, right=0.9, bottom=0.2, top=0.8)

        return canvas

    # ===============================================
    # Properties
    # ===============================================

    @property
    def n_evolutions(self):
        """Number of evolutions"""
        return len(self.evolutions)

    @property
    def evolutions(self):
        """List of evolutions"""
        if PageState.version == 'default':
            return ['default']
        animal_folder = os.path.join(GRAPH_VERSION_FOLDER, PageState.id)
        versions = [PageState.version]
        while True:
            current_file = os.path.join(animal_folder, versions[-1] + ".pkl")
            with open(current_file, "rb") as f:
                data = pickle.load(f)
                prev_version = data['prev_version']
            versions.append(prev_version)
            if prev_version == 'default':
                break
        versions.reverse()
        return versions

    @property
    def str_statistics(self):
        return f"Version: {self.evolutions[self.evolution_id]}"

    # ===============================================
    # Refresh on this page
    # ===============================================

    def refresh(self):
        """Refresh the page, the graph, the tabls, the buttons"""
        self._refresh_graph()
        self.info_tab.setText(self.str_statistics)
        self._update_button_states()
        self._update_plots()

    def _refresh_graph(self):
        """Refresh the graph"""
        version = self.evolutions[self.evolution_id]
        animal_folder = os.path.join(GRAPH_VERSION_FOLDER, PageState.id)

        # Load graphs
        if version != 'default' and os.path.exists(animal_folder) and os.listdir(animal_folder):
            file_path = os.path.join(GRAPH_VERSION_FOLDER, PageState.id, version + ".pkl")
            self.graph_gui.graph = Graph.from_pkl(filepath=file_path)
        elif version == 'default':
            self.graph_gui.graph = Graph.from_graphml(PageState.graph_path)
        else:
            raise NameError(f"Version {version} does not exist")

        highlighted_nodes, highlighted_edges = self.differences[version]
        self.graph_gui.graph.select(nodes=highlighted_nodes, edges=highlighted_edges)
        self.graph_gui.graph.fresh_nodes = highlighted_nodes
        self.graph_gui.refresh()

    def _update_button_states(self):
        """Refresh the button states"""
        if hasattr(self, 'prev_button') and hasattr(self, 'next_button'):
            self.prev_button.setEnabled(self.evolution_id != 0)
            self.next_button.setEnabled(self.evolution_id != self.n_evolutions - 1)

    def _update_plots(self):
        """Move the vertical line on each plot to the new x position and redraw the plot."""
        if hasattr(self, 'top_right_plot'):
            for plot in [self.top_right_plot, self.bottom_left_plot, self.bottom_right_plot]:
                # Update the xdata of the line
                plot.line.set_xdata(self.evolutions[self.evolution_id])
                # Redraw the plot
                plot.ax.figure.canvas.draw()

    # ===============================================
    # Buttons trigger actions
    # ===============================================

    def _slider_value_changed(self, value):
        """Slot function to handle slider value changes"""
        self.evolution_id = value
        self.refresh()

    def _prev_button_on_click(self):
        """Jump back to previous evolution"""
        self.evolution_id = max(0, self.evolution_id - 1)
        self.slider.setValue(self.evolution_id)  # Update the slider value
        self.refresh()

    def _next_button_on_click(self):
        """Jump to next evolution"""
        self.evolution_id = min(self.n_evolutions - 1, self.evolution_id + 1)
        self.slider.setValue(self.evolution_id)  # Update the slider value
        self.refresh()