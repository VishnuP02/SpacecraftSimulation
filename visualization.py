import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_trajectory(x_vals, y_vals):
    """
    Static plot for the trajectory of the spacecraft.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, label="Trajectory", marker="o", color="orange")
    plt.title("Spacecraft Trajectory Simulation")
    plt.xlabel("Horizontal Position (m)")
    plt.ylabel("Vertical Position (m)")
    plt.legend()
    plt.grid()
    plt.show()

def plot_fuel_consumption(time_steps, fuel_levels):
    """
    Plot the fuel consumption over time.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(time_steps, fuel_levels, label="Fuel Remaining", color="orange")
    plt.title("Fuel Consumption Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Fuel (kg)")
    plt.legend()
    plt.grid()
    plt.show()

def animate_trajectories(trajectories, simulation_time, time_step):
    """
    Animate the trajectories of multiple spacecraft in real-time.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Set axis limits based on the trajectories
    all_x = [x for trajectory in trajectories.values() for x, _ in trajectory]
    all_y = [y for trajectory in trajectories.values() for _, y in trajectory]
    ax.set_xlim(0, max(all_x) + 10)
    ax.set_ylim(0, max(all_y) + 10)

    # Initialize lines for each spacecraft
    lines = {name: ax.plot([], [], label=name)[0] for name in trajectories.keys()}

    # Title, labels, and legend
    ax.set_title("Real-Time Spacecraft Trajectory Animation")
    ax.set_xlabel("Horizontal Position (m)")
    ax.set_ylabel("Vertical Position (m)")
    ax.legend()
    ax.grid()

    # Update function for animation
    def update(frame):
        current_time = frame * time_step
        for name, line in lines.items():
            x_vals, y_vals = zip(*trajectories[name][:frame + 1])
            line.set_data(x_vals, y_vals)
        return lines.values()

    # Create the animation
    frames = int(simulation_time / time_step)
    ani = FuncAnimation(fig, update, frames=frames, interval=50, blit=True)

    # Show the animation
    plt.show()