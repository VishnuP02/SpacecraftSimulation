import json
from spacecraft import Spacecraft
from visualization import plot_fuel_consumption, plot_trajectory, animate_trajectories
import matplotlib.pyplot as plt
import os


# Validate and Load JSON File
def load_json_file(filename):
    """
    Load and validate a JSON file.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Error: '{filename}' does not exist.")

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"Error: '{filename}' contains invalid JSON.")

    return data


# Validate Spacecraft Configurations
def validate_spacecraft_config(config):
    """
    Validate a single spacecraft configuration.
    """
    required_keys = ["name", "mass", "fuel", "thrust", "angle"]
    for key in required_keys:
        if key not in config:
            raise KeyError(f"Error: Missing key '{key}' in spacecraft configuration.")
        if key == "name":  # 'name' should be a string
            if not isinstance(config[key], str) or not config[key].strip():
                raise ValueError(f"Error: 'name' must be a non-empty string.")
        else:  # For numeric keys
            if not isinstance(config[key], (int, float)) or config[key] <= 0:
                raise ValueError(f"Error: '{key}' must be a positive number.")


# Add a new spacecraft dynamically
def add_spacecraft():
    """
    Prompt the user to add a new spacecraft.
    """
    print("\nAdd a New Spacecraft:")
    name = input("Enter spacecraft name: ").strip()
    mass = float(input("Enter spacecraft mass (kg): "))
    fuel = float(input("Enter initial fuel (kg): "))
    thrust = float(input("Enter thrust (N): "))
    angle = float(input("Enter launch angle (degrees): "))

    return {
        "name": name,
        "mass": mass,
        "fuel": fuel,
        "thrust": thrust,
        "angle": angle
    }


# Main Simulation
try:
    # Load spacecraft configurations from file
    spacecraft_configs = load_json_file("spacecrafts.json")
    for config in spacecraft_configs:
        validate_spacecraft_config(config)

    # Allow user to add new spacecraft
    add_more = input("\nWould you like to add a new spacecraft? (yes/no): ").strip().lower()
    while add_more == "yes":
        new_spacecraft = add_spacecraft()
        validate_spacecraft_config(new_spacecraft)
        spacecraft_configs.append(new_spacecraft)
        add_more = input("Would you like to add another spacecraft? (yes/no): ").strip().lower()

except (FileNotFoundError, ValueError, KeyError) as e:
    print(e)
    exit(1)

simulation_time = 20  # seconds
time_step = 0.1  # seconds per update
fuel_consumption_rate = 0.5  # kg of fuel per second of thrust

# Initialize spacecraft
spacecraft_objects = [
    Spacecraft(
        name=config["name"],
        mass=config["mass"],
        fuel=config["fuel"]
    )
    for config in spacecraft_configs
]

# Simulate each spacecraft
trajectories = {}
fuel_data = {}
landing_results = {}

print("\nStarting Multi-Spacecraft Simulation...\n")

for spacecraft, config in zip(spacecraft_objects, spacecraft_configs):
    print(f"Simulating {spacecraft.name}...\n")
    positions = []
    fuel_levels = []
    landed = False

    for t in range(int(simulation_time / time_step)):
        current_time = t * time_step
        if current_time == 2:  # Apply thrust at 2 seconds
            spacecraft.apply_thrust(
                thrust=config["thrust"],
                angle=config["angle"],
                duration=2,
                fuel_consumption_rate=fuel_consumption_rate
            )
        spacecraft.update_position(time_step)
        status = spacecraft.status()
        positions.append((status["x"], status["y"]))
        fuel_levels.append(status["fuel"])

        # Check for landing
        if status["y"] == 0 and not landed:
            landing_result = spacecraft.check_landing()
            landing_results[spacecraft.name] = landing_result
            print(f"{spacecraft.name} has landed: {landing_result}")
            landed = True

        print(
            f"Time: {current_time:.1f}s | "
            f"Position: ({status['x']:.2f}, {status['y']:.2f}) m | "
            f"Velocity: ({status['vx']:.2f}, {status['vy']:.2f}) m/s | "
            f"Fuel: {status['fuel']:.2f} kg"
        )

    trajectories[spacecraft.name] = positions
    fuel_data[spacecraft.name] = fuel_levels
    print(f"Simulation for {spacecraft.name} Complete!\n")

# Print landing results
print("\nLanding Results:")
for name, result in landing_results.items():
    print(f"{name}: {result}")

# Plot static trajectories
plt.figure(figsize=(8, 6))
for name, trajectory in trajectories.items():
    x_vals, y_vals = zip(*trajectory)
    plt.plot(x_vals, y_vals, label=f"{name} Trajectory")
plt.title("Multi-Spacecraft Trajectory Simulation")
plt.xlabel("Horizontal Position (m)")
plt.ylabel("Vertical Position (m)")
plt.legend()
plt.grid()
plt.show()

# Animate trajectories
animate_trajectories(trajectories, simulation_time, time_step)

# Plot fuel consumption
plt.figure(figsize=(8, 6))
time_steps = [i * time_step for i in range(int(simulation_time / time_step))]
for name, fuel_levels in fuel_data.items():
    plt.plot(time_steps, fuel_levels, label=f"{name} Fuel")
plt.title("Fuel Consumption of Multi-Spacecraft")
plt.xlabel("Time (s)")
plt.ylabel("Fuel (kg)")
plt.legend()
plt.grid()
plt.show()