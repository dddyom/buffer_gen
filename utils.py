from matplotlib.colors import LinearSegmentedColormap, Normalize

norm = Normalize(-1, 1)
CMAP = LinearSegmentedColormap.from_list("", [[norm(-1.0), "0"], [norm(1.0), "yellow"]])  # black
