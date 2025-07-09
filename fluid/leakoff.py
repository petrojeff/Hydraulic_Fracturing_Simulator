import numpy as np

def compute_leakoff(pressure, t, cfg):
    """
    Computes fluid leak-off into the formation using a simplified Carter's model.
    
    Parameters:
    - pressure: array of pressures in each grid cell [psi]
    - t: current simulation time [s]
    - cfg: configuration dictionary
    
    Returns:
    - leakoff: array of leak-off rates per cell [m³/s per cell]
    """
    cl = 1e-6  # Leak-off coefficient [m/s^0.5], tunable
    pref = cfg["formation"]["stress_tensor"]["min_horizontal"]
    alpha = 0.1  # Pressure sensitivity factor (dimensionless)
    
    # Compute leakoff for each cell: Carter-like decay with pressure scaling
    leak = cl * (1 + alpha * (pressure - pref) / pref) / (np.sqrt(t + 1e-6))
    leak[leak < 0] = 0  # Prevent negative leak-off
    # import pdb
    # pdb.set_trace()  # Debugging breakpoint
    leak[:] = 0
    return leak
