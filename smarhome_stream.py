import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd

class SmartGridSimulation:
    def __init__(self, fixed_demand, fixed_renewable_data, storage_capacity, time_step):
        self.total_time_steps = len(fixed_demand)
        self.time_steps = np.arange(1, self.total_time_steps + 1)
        self.demand = fixed_demand
        self.renewable_data = fixed_renewable_data
        self.renewable_generation = np.zeros(self.total_time_steps)
        self.energy_storage = np.zeros(self.total_time_steps)
        self.storage_capacity = storage_capacity
        self.time_step = time_step

    def simulate(self):
        for step in range(self.total_time_steps):
            self.renewable_generation[step] = self.renewable_data[step % len(self.renewable_data)]

            excess_energy = max(0, self.renewable_generation[step] - self.demand[step])
            stored_energy = min(excess_energy, self.storage_capacity)
            stored_energy_after_losses = stored_energy * 0.95
            self.energy_storage[step] = stored_energy_after_losses

            self.demand[step] += self.energy_storage[step]

def main():
    st.title("Smart Grid Simulator")

    storage_capacity = st.text_input("Storage Capacity (kWh):", "50")
    time_step = st.text_input("Time Step (hours):", "1")

    # Additional features
    renewable_upload = st.file_uploader("Upload Renewable Energy Data (CSV)", type=["csv"])
    if renewable_upload is not None:
        renewable_data = np.genfromtxt(renewable_upload, delimiter=',')
        st.success("Renewable_energy data uploaded successfully!")

    if st.button("Simulate"):
        try:
            storage_capacity = float(storage_capacity)
            time_step = float(time_step)

            if 'renewable_data' in locals():
                smart_grid = SmartGridSimulation(
                    np.array([100, 90, 80, 70, 60, 50, 40, 30, 20, 15, 70, 123, 145, 108, 60, 15, 4, 100, 130, 98]),
                    renewable_data,
                    storage_capacity,
                    time_step
                )
            else:
                smart_grid = SmartGridSimulation(
                    np.array([100, 90, 80, 70, 60, 50, 40, 30, 20, 15, 70, 123, 145, 108, 60, 15, 4, 100, 130, 98]),
                    np.array([10, 30, 40, 50, 70, 90, 100, 110, 105, 100, 90, 70, 60, 45, 50, 50, 60, 65, 60, 75, 85]),
                    storage_capacity,
                    time_step
                )

            smart_grid.simulate()

            # Plot results
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(smart_grid.time_steps, smart_grid.demand, label='Demand', marker='o')
            ax.plot(smart_grid.time_steps, smart_grid.renewable_generation, label='Solar Energy', marker='o')
            ax.plot(smart_grid.time_steps, smart_grid.energy_storage, label='Energy Storage', marker='o')
            ax.set_title('Smart Home Simulation')
            ax.set_xlabel('Time Steps')
            ax.set_ylabel('Power(KW)')
            ax.legend()
            ax.grid(True)

            # Display the plot in Streamlit
            plot = st.pyplot(fig)

            # Add click functionality to display coordinates
            

            # plot.figure.canvas.mpl_connect("button_press_event", handle_click)

            # Display additional information
            st.text(f"Total Demand: {np.sum(smart_grid.demand):.2f} kWh")
            st.text(f"Total Renewable Generation: {np.sum(smart_grid.renewable_generation):.2f} kWh")
            st.text(f"Total Energy Storage: {np.sum(smart_grid.energy_storage):.2f} kWh")

            # Export Results
            
        except ValueError:
            st.error("Invalid input. Please enter numeric values.")

if __name__ == "__main__":
    main()