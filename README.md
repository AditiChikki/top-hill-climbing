# Traveling Salesman Problem Solver using Hill Climbing Algorithm

This project implements an interactive Traveling Salesman Problem (TSP) solver using the Hill Climbing heuristic algorithm with a graphical user interface (GUI). It allows users to input cities, select a starting city, and visualize both the optimal route and pairwise distances between cities.

Features:-

- Solves TSP using a greedy hill climbing approach (Nearest Neighbor heuristic)
- Calculates distances using geopy (Haversine formula)
- Visualizes the TSP route and distance graph using matplotlib + NetworkX
- Intuitive GUI built using `tkinter`
- Real-time switching between TSP route and full distance graph
- Adjustable GUI layout and fonts based on window size

Algorithm:-

- Hill Climbing (Nearest Neighbor): Iteratively selects the nearest unvisited city from the current city and builds a route.
- Distance Calculation: Uses `geopy`'s `geodesic()` function to compute real-world distances between cities.
- Graph Visualization: Utilizes NetworkX for plotting city nodes and route edges with distance labels.

GUI Interface:-

- Built using `tkinter`
- Input cities and confirm route interactively
- Graphs rendered directly within the GUI

Requirements:-

Install required libraries with:

```bash
pip install -r requirements.txt
