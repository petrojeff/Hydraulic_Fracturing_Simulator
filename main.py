import yaml
import numpy as np
import pandas as pd
import os
import time  # ⏱ Track timing

from mesh.fracture_mesh import create_mesh
from fluid.fluid_flow import get_injection_rate
from fluid.leakoff import compute_leakoff
from mechanics.fracture_mechanics import compute_width
from proppant.transport import update_proppant_concentration
from output.visualization import plot_width_pressure
from output.movie_maker import create_movie

def load_config():
    with open("config/input.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    total_start = time.time()

    print("🔧 Loading configuration...")
    start = time.time()
    cfg = load_config()
    print(f"✅ Done (⏱️ {time.time() - start:.2f} s)\n")

    print("🧱 Creating mesh...")
    start = time.time()
    n_cells = 100
    dx, x = create_mesh(n_cells=n_cells, length=50.0)
    print(f"✅ Done (⏱️ {time.time() - start:.2f} s)\n")

    print("🚀 Starting simulation loop...")
    start = time.time()

    # Units conversion
    bbl_to_m3 = 0.158987
    rate = cfg["injection"]["rate"] * bbl_to_m3 / 60
    half_rate = 0.5 * rate

    total_time = cfg["simulation"]["total_time"]
    dt = cfg["simulation"]["time_step"]
    n_steps = int(total_time / dt)

    pressure = np.full(n_cells, cfg["formation"]["stress_tensor"]["min_horizontal"], dtype=float)
    width = np.zeros(n_cells)
    proppant = np.zeros(n_cells)

    width_history = []
    pressure_history = []

    for step in range(n_steps):
        t = step * dt
        remaining = total_time - t

        injection_rate = get_injection_rate(t, half_rate, cfg)
        leakoff = compute_leakoff(pressure, t, cfg)

        injection_cell = 0
        pressure[injection_cell] += (injection_rate - leakoff[injection_cell]) * dt / (width[injection_cell] + 1e-6)

        for i in range(n_cells):
            proppant[i] = update_proppant_concentration(width[i], pressure[i], cfg, i=i)

        width = compute_width(pressure, cfg)
        width_history.append(width.copy())
        pressure_history.append(pressure.copy())

    print(f"✅ Simulation loop complete (⏱️ {time.time() - start:.2f} s)\n")

    print("💾 Saving simulation results to CSV...")
    start = time.time()
    os.makedirs("output", exist_ok=True)
    df = pd.DataFrame({
        "x": np.tile(x, len(width_history)),
        "time": np.repeat(np.arange(n_steps) * dt, n_cells),
        "width": np.concatenate(width_history),
        "pressure": np.concatenate(pressure_history)
    })
    df.to_csv("output/simulation_results.csv", index=False)
    print(f"✅ Done (⏱️ {time.time() - start:.2f} s)\n")

    print("📊 Generating final plot...")
    start = time.time()
    plot_width_pressure(width_history, pressure_history, x, dt)
    print(f"✅ Done (⏱️ {time.time() - start:.2f} s)\n")

    print("🎞️ Creating animation...")
    start = time.time()
    create_movie(width_history, dx, dt)
    print(f"✅ Done (⏱️ {time.time() - start:.2f} s)\n")

    print(f"🏁 All done! Total runtime: ⏱️ {time.time() - total_start:.2f} seconds")

if __name__ == "__main__":
    main()
