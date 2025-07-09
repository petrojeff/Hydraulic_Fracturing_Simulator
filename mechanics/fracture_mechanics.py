import numpy as np

def compute_width(pressure, cfg):
    """
    Computes fracture width using net pressure and plain strain modulus.

    Parameters:
    - pressure: array of pressure values [psi]
    - cfg: configuration dictionary

    Returns:
    - width: array of fracture widths [m]
    """
    E = float(cfg["formation"]["youngs_modulus"])       # Force float
    nu = float(cfg["formation"]["poisson_ratio"])       # Force float
    sigma = float(cfg["formation"]["stress_tensor"]["min_horizontal"])  # Force float

    # Convert modulus from psi to Pa if needed (optional, currently consistent in psi)
    E_prime = E / (1 - nu**2)                    # Plane strain modulus [psi]

    net_pressure = pressure - sigma              # Driving force for opening [psi]

    # Height model (simplified as pressure-dependent growth)
    height = 10.0 + 0.01 * net_pressure           # Height grows slightly with pressure [m]

    # Compute width (PKN-like assumption)
    width = (4 * net_pressure * height) / (np.pi * E_prime)
    width[width < 0] = 0  # Clamp negative widths

    return width

