def update_proppant_concentration(width, pressure, cfg, i=0):
    """
    Determines local proppant concentration based on fracture width.

    Parameters:
    - width: fracture width at a given location [m]
    - pressure: local pressure (unused for now, placeholder for future logic)
    - cfg: full configuration dictionary
    - i: index (for logging/debugging if needed)

    Returns:
    - concentration: local proppant volume fraction
    """
    d_p = cfg["proppant"]["diameter"]
    c_max = cfg["proppant"]["concentration"]

    if width < 1.5 * d_p:
        return 0.0  # Fully bridged
    elif width < 1.8 * d_p:
        return 0.5 * c_max  # Partial bridging
    else:
        return c_max  # Full concentration possible
