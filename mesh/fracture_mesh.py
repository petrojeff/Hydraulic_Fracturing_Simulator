def create_mesh(n_cells=100, length=50.0):
    """
    Creates a 1D spatial mesh starting at x = 0 and ending at x = length.

    Parameters:
    - n_cells: number of spatial grid cells
    - length: total fracture length (m)

    Returns:
    - dx: cell size (m)
    - x: list of cell center coordinates (m)
    """
    dx = length / n_cells
    x = [i * dx for i in range(n_cells)]
    return dx, x
