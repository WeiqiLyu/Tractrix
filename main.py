import pandas as pd

from pushback_path_generation import calculate_positions
from path_visualisation import plot_trajectory
from reference_path_generation import generate_path, save_path_to_csv

# -------------------------------------------------------------------------------------------------------------------------------------------------------
# USER INPUT --------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------


# Set the length and direction of the reference path
segments = [                     # A list of segments that define the reference path.
    # Each tuple specifies the type of segment and its parameters.
    ('line', 90, 100),         # A line segment with a length of 90 meters, extending at an angle of 90 degrees (north direction).
                                  # Format: ('line', length, angle)
                                  # length [m]: The length of the line segment.
                                  # angle [degrees]: The direction of the line segment in degrees, measured counterclockwise from the east (0 degrees).
]

#segments = [                     # A list of segments that define the reference path.
#    # Each tuple specifies the type of segment and its parameters.
#    ('line', 42.11, 90),         # A line segment with a length of 42.11 meters, extending at an angle of 90 degrees (north direction).
#                                  # Format: ('line', length, angle)
#                                  # length [m]: The length of the line segment.
#                                  # angle [degrees]: The direction of the line segment in degrees, measured counterclockwise from the east (0 degrees).
#
#    ('arc', 42.11, -90, False),  # An arc segment with a radius of 42.11 meters, covering a central angle of -90 degrees (indicating a clockwise turn).
#                                  # Format: ('arc', radius, central_angle, is_left)
#                                  # radius [m]: The radius of the arc segment.
#                                  # central_angle [degrees]: The angle subtended by the arc at the center, negative values indicate clockwise motion.
#                                  # is_left [Boolean]: Indicates whether the arc turns to the left (True) or to the right (False).
#
#    ('line', 42.11, 0),          # Another line segment with a length of 42.11 meters, extending at an angle of 0 degrees (east direction).
#                                  # Format: ('line', length, angle)
#                                  # This line continues in the same direction as the previous segments.
#]

#segments = [                      
#    ('line', 42.11, 180),         # A line segment with a length of 42.11 meters, extending at an angle of 180 degrees (west direction).
#    ('arc', 42.11, 90, True),     # An arc segment with a radius of 42.11 meters, covering a central angle of 90 degrees (indicating a counterclockwise turn)
#    ('line', 42.11, -90),         # Another line segment with a length of 42.11 meters, extending at an angle of -90 degrees (south direction).
#]


# Set the initial position of airplane     
nose_gear_angle = 10                          # Float, the angle of the nose gear of the aircraft, measured counterclockwise in degrees from the nord.
track_number = 5                              # Int, the number of track points of the aircraft, defualt is 5.
drag_number = 2                               # Int, the number of drag points of the aircraft, defualt is 2.
trace_init_data = [0, 17.17]                  # The initial position of the trace point, typically an array with two elements representing (x, y) coordinates.
track_init_data = [[17.16, 22.48],            # The initial positions of the track points, with shape (track_number, 2) representing (x, y) coordinates for each Track point.
                   [-17.16, 22.48], 
                   [7.18, 38.02], 
                   [-7.18, 38.02], 
                   [0, -4.09]]
drag_init_data = [[2.86, 17.17],              # The initial positions of the drag points, with shape (drag_number, 2) representing (x, y) coordinates for each Drag point.
                  [-2.86, 17.17]]


# -------------------------------------------------------------------------------------------------------------------------------------------------------
# Generation OF REFERENCE PATH --------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------


path_samples = generate_path(segments)

# Save path data to CSV
save_path_to_csv(path_samples, "reference_path_data.csv")


# -------------------------------------------------------------------------------------------------------------------------------------------------------
# GENEATION OF TRACTRIX CURVE ---------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------


# Read the CSV file
drive_sequence = pd.read_csv('reference_path_data.csv')  # A sequence of Drive point data containing the position of the nose gear at each time point.
data_number = len(drive_sequence)                        # The number of data points, representing the number of time-series data points for Drive, Trace, Drag, and Track.

# Call the function to calculate positions
results = calculate_positions(data_number, track_number, drag_number, drive_sequence, trace_init_data, drag_init_data, track_init_data, nose_gear_angle)


# -------------------------------------------------------------------------------------------------------------------------------------------------------
# PLOT RESULTS ------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------


# plot trajectories
plot_trajectory(results, obstacles=True)

# Print results
print("Drive:\n", results["Drive"])
print("Trace:\n", results["Trace"])
print("Drag:\n", results["Drag"])
print("Track:\n", results["Track"])
print("Wing center:\n", results["Wing Center"])
print("Tail center:\n", results["Tail Center"])
print("Min values:\n", results["Min Values"])
print("Max values:\n", results["Max Values"])