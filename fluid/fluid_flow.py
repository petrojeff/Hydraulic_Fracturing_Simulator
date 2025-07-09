def get_injection_rate(t, base_rate, cfg):
    """
    Returns the injection rate at time t.
    Injection stops after the configured duration.
    
    Parameters:
    - t: current time [s]
    - base_rate: injection rate in m³/s
    - cfg: configuration dictionary from YAML
    
    Returns:
    - injection_rate: float (m³/s)
    """
    duration = cfg["injection"]["duration"]
    return base_rate if t <= duration else 0.0
