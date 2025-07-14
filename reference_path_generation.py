
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def generate_path(segments, num_samples=100):
    """
    Generate a path consisting of multiple segments based on input parameters.

    Parameters:
    ----------
    segments (list of tuples): Each tuple specifies the type of segment and its parameters.
                               Format: ('line', length, angle) for lines and 
                                      ('arc', radius, curve_angle, direction_angle, is_left) for arcs.
    num_samples (int): Number of sample points per segment.

    Returns:
    -------
    all_samples (np.ndarray): Sample coordinates for the entire path.
    """
    path_points = []  # List to store coordinates for each segment
    current_position = np.array([0, 0])  # Starting point of the path
    current_angle = 0  # Initial angle in radians (0 degrees, pointing to the right)

    # Generate segments based on user input
    for i, segment in enumerate(segments):
        if segment[0] == 'line':
            length = segment[1]
            angle = segment[2]  # Use specified angle
            
            # Convert angle from degrees to radians
            angle_rad = np.radians(angle)
            direction = np.array([np.cos(angle_rad), np.sin(angle_rad)])  # Calculate direction vector

            end_position = current_position + length * direction  # Calculate end position based on direction
            samples = np.linspace(current_position, end_position, num_samples + 1)  # Extra point for avoiding overlap

            # Exclude the first point in all segments except the first
            if i > 0:
                samples = samples[1:]  # Skip first point

            path_points.append(samples)
            current_position = end_position  # Update current position
            
            # Update the current angle for the next segment
            current_angle = angle_rad

        elif segment[0] == 'arc':
            radius = segment[1]
            curve_angle = segment[2]  # The angle of curvature in degrees
            is_left = segment[3]  # Boolean for left (True) or right (False) curve
            sign = 1 if is_left else -1

            # Convert angles from degrees to radians
            start_angle_rad = current_angle  # The current angle
            end_angle_rad = start_angle_rad + np.radians(curve_angle)  # End angle

            # Determine the arc center based on the direction
            arc_center = current_position + radius * np.array([
                np.cos(start_angle_rad + sign * np.pi / 2), 
                np.sin(start_angle_rad + sign * np.pi / 2)
            ])
            
            # Generate the arc points
            theta = np.linspace(start_angle_rad, end_angle_rad, num_samples + 1)  # Extra point for avoiding overlap
            arc_samples = arc_center + radius * np.array([
                np.cos(theta - sign * np.pi / 2), 
                np.sin(theta - sign * np.pi / 2)
            ]).T
            
            # Exclude the first point in all segments except the first
            if i > 0:
                arc_samples = arc_samples[1:]  # Skip first point
            
            path_points.append(arc_samples)
            current_position = arc_samples[-1]  # Update current position to the end of arc
            current_angle = end_angle_rad  # Update the angle for the next segment

    # Combine all sample points
    all_samples = np.vstack(path_points)

    # Round all coordinates to 4 decimal places for precision
    all_samples = np.round(all_samples, 4)

    # Plot the trajectory
    plt.plot(all_samples[:, 0], all_samples[:, 1], marker='o')
    plt.title("Trajectory of the Path")
    plt.xlabel("X in m")
    plt.ylabel("Y in m")
    plt.axis('equal')
    plt.grid()
    plt.show()

    return all_samples

def save_path_to_csv(path_data, filename="reference_path_data.csv"):
    """
    Save path data to a CSV file.

    Parameters:
    ----------
    path_data (np.ndarray): Sample coordinates of the path.
    filename (str): Name of the output CSV file.
    """
    # Create a DataFrame
    df = pd.DataFrame(path_data, columns=["X", "Y"])
    
    # Save as CSV file
    df.to_csv(filename, index=False)
    print(f"Path data saved to {filename}")



if __name__ == "__main__":
    # Example usage
    segments = [
        ('line', 40, 180),        # First segment: length 40 meters extending at an angle of 180 degrees (west direction).
        ('arc', 40, 90, True),    # Second segment: arc with radius 40 meters, covering a central angle of 90 degrees (indicating a counterclockwise turn), turning to left.
        ('line', 40, -90),        # Third segment: length 40 meters at -90 degrees (south direction)
        ('arc', 40, -90, False),  # Fourth segment: arc with radius 40 meters, covering a central angle of -90 degrees (indicating a clockwise turn), turning to right.
        ('line', 40, 180),        # Fifth segment: length 100 meters at 180 degrees (west direction)
        ('arc', 40, 90, False),   # Sixth segment: arc with radius 40 meters, covering a central angle of 90 degrees (indicating a counterclockwise turn), turning to right.
        ('line', 40, 90),         # Seventh segment: length 40 meters at 90 degrees (north direction)
        ('arc', 40, -90, True),   # Eighth segment: arc with radius 40 meters, covering a central angle of -90 degrees (indicating a clockwise turn), turning to left.
        ('line', 40, 180)         # Ninth segment: length 100 meters at 180 degrees (west direction)
    ]

    path_samples = generate_path(segments)

    # Save path data to CSV
    # save_path_to_csv(path_samples, "reference_path_data.csv")
