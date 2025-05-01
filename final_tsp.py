import tkinter as tk
from tkinter import messagebox, font
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TSPSolver:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Traveling Salesman Problem Solver")
        self.root.geometry("800x600")
        self.root.configure(bg="#ffe0bd")  # Set the background color of the root window

        # Load background image
        self.bg_image = tk.PhotoImage(file="peakpx.png")  # Change "background.png" to your image file

        # Create a label for the background image
        self.background_label = tk.Label(self.root, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1) 

        self.page = 0
        self.cities = []
        self.starting_city = None
        self.distances = {}  # Store calculated distances between cities

        self.label_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=10)

        self.label = tk.Label(self.root, text="Enter the city name:", font=self.label_font, bg="#ffe0bd")  # Skin color
        self.label.pack()

        self.city_entry = tk.Entry(self.root, font=self.label_font, bg="#ffe0bd")  # Skin color
        self.city_entry.pack()

        self.add_city_button = tk.Button(self.root, text="Add City", command=self.add_city, font=self.button_font, bg="#ffe0bd")  # Skin color
        self.add_city_button.pack()

        self.done_button = tk.Button(self.root, text="Done", command=self.next_page, font=self.button_font, bg="#ffe0bd")  # Skin color
        self.done_button.pack()

        self.graph_frame = tk.Frame(self.root, bg="#ffe0bd")  # Skin color
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        self.graph_frame.pack_propagate(False)

        self.fig, self.ax = plt.subplots(figsize=(4, 3))  # smaller size (4x3)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.loading_label = tk.Label(self.root, text="Wait champ! We are fetching the best route for you", font=self.label_font, bg="#ffe0bd")  # Skin color
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, font=self.button_font, bg="#ffe0bd")  # Skin color
        self.toggle_button = tk.Button(self.root, text="Show TSP", command=self.toggle_graph, font=self.button_font, bg="#ffe0bd")  # Skin color

        self.start_city_var = tk.StringVar()
        self.start_city_var.set("")  # Initialize with an empty string

        self.start_city_menu = tk.OptionMenu(self.root, self.start_city_var, "")
        self.start_city_menu.pack()
        self.start_city_menu.config(font=self.label_font, width=20, bg="#ffe0bd")  # Set width to make it bigger and background color to skin color

        self.root.bind("<Configure>", self.adjust_fonts)
        self.root.mainloop()

    def adjust_fonts(self, event):
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        label_font_size = max(int(window_width / 70), 10)
        button_font_size = max(int(window_width / 90), 8)
        self.label_font.configure(size=label_font_size)
        self.button_font.configure(size=button_font_size)

    def add_city(self):
        city = self.city_entry.get().strip()
        if city:
            self.cities.append(city)
            self.city_entry.delete(0, tk.END)

    def next_page(self):
        if self.page == 0:
            if len(self.cities) < 2:
                messagebox.showwarning("Warning", "Please enter at least two cities.")
                return
            self.page += 1
            self.start_page()

    def start_page(self):
        self.label.config(text="Select the starting city:")
        self.city_entry.pack_forget()
        self.add_city_button.pack_forget()
        self.done_button.pack_forget()

        # Update the OptionMenu with the cities list
        self.start_city_menu['menu'].delete(0, 'end')
        for city in self.cities:
            self.start_city_menu['menu'].add_command(label=city, command=tk._setit(self.start_city_var, city))

        self.start_city_var.set(self.cities[0])

        self.confirm_button = tk.Button(self.root, text="Confirm", command=self.confirm_start_city, font=self.button_font, bg="#ffe0bd")  # Skin color
        self.confirm_button.pack()

    def confirm_start_city(self):
        self.loading_label.pack()  # Show loading message
        self.root.update()  # Update the window to display the loading message

        self.starting_city = self.start_city_var.get()
        self.solve_tsp()
        self.render_graph()

        self.loading_label.pack_forget()  # Hide loading message
        self.root.update()  # Update the window to hide the loading message

    def solve_tsp(self):
        G = nx.DiGraph()  # Create a directed graph
        for city in self.cities:
            G.add_node(city)
        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                if i != j:
                    city1 = self.cities[i]
                    city2 = self.cities[j]
                    if (city1, city2) not in self.distances:  # Calculate distance only if not calculated before
                        distance = self.get_distance(city1, city2)
                        self.distances[(city1, city2)] = distance
                    else:
                        distance = self.distances[(city1, city2)]
                    G.add_edge(city1, city2, weight=distance)
        self.route = self.approx_tsp(G, self.starting_city)

    def approx_tsp(self, G, start_city):
        route = [start_city]
        current_city = start_city
        unvisited_cities = set(G.nodes()) - {start_city}

        while unvisited_cities:
            nearest_city = min(unvisited_cities, key=lambda city: G[current_city][city]['weight'])
            route.append(nearest_city)
            unvisited_cities.remove(nearest_city)
            current_city = nearest_city

        return route

    def get_distance(self, city1, city2):
        geolocator = Nominatim(user_agent="city_distance_calculator")
        location1 = geolocator.geocode(city1)
        location2 = geolocator.geocode(city2)

        if location1 is None or location2 is None:
            return float('inf')

        coords1 = (location1.latitude, location1.longitude)
        coords2 = (location2.latitude, location2.longitude)
        distance = geodesic(coords1, coords2).kilometers
        return distance

    def render_tsp_graph(self):
        G = nx.DiGraph()  # Create a directed graph
        for city in self.cities:
            G.add_node(city)
        for i in range(len(self.route) - 1):
            G.add_edge(self.route[i], self.route[i + 1], weight=self.distances[(self.route[i], self.route[i+1])])
        G.add_edge(self.route[-1], self.route[0], weight=self.distances[(self.route[-1], self.route[0])])

        pos = nx.spring_layout(G)

        self.ax.clear()
        self.ax.set_facecolor('none')  # Set transparent background
        nx.draw(G, pos, with_labels=True, node_color='g', font_weight='bold', node_size=2000, ax=self.ax)
        nx.draw_networkx_nodes(G, pos, nodelist=[self.route[0]], node_color='b', node_size=2000, node_shape='H', ax=self.ax)

        edge_labels = {(u, v): f"{G[u][v]['weight']:.2f} km" for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax)

        # Corrected function name and explicit arrows parameter
        nx.draw_networkx_edges(G, pos, arrows=True, ax=self.ax)

        self.ax.set_title("Traveling Salesman Problem Solution")
        self.canvas.draw()

    def render_distance_graph(self):
        G = nx.Graph()  # Create an undirected graph
        for city1, city2 in self.distances.keys():
            distance = self.distances[(city1, city2)]
            G.add_edge(city1, city2, weight=distance)

        pos = nx.spring_layout(G)

        self.ax.clear()
        self.ax.set_facecolor('none')  # Set transparent background
        nx.draw(G, pos, with_labels=True, node_color='skyblue', font_weight='bold', node_size=2000, ax=self.ax)

        edge_labels = {(u, v): f"{G[u][v]['weight']:.2f} km" for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax)

        self.ax.set_title('Distances between City Pairs')
        self.canvas.draw()

    def render_graph(self):
        self.ax.clear()
        if self.toggle_button['text'] == "Show TSP":
            self.solve_tsp()
            self.render_tsp_graph()
            self.toggle_button.config(text="Show Distances")
        else:
            self.render_distance_graph()
            self.toggle_button.config(text="Show TSP")

        self.toggle_button.pack()  # Placing Show TSP button above the Quit button
        self.quit_button.pack()

    def toggle_graph(self):
        self.render_graph()

if __name__ == "__main__":
    TSPSolver()
