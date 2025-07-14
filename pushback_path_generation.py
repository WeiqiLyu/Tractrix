import numpy as np

def calculate_positions(data_number, track_number, drag_number, drive_sequence, trace_init_data, drag_init_data, track_init_data, nose_gear_angle):
    """
    Calculate the positions of various key points (Drive, Trace, Drag, Track) during aircraft motion.

    Parameters:
    ----------
    data_number : int
        The number of data points, representing the number of time-series data points for Drive, Trace, Drag, and Track.
    track_number : int
        The number of Track positions, defualt is 5.
    drag_number : int
        The number of Drag positions, default is 2.
    drive_sequence : DataFrame
        A sequence of Drive point data, typically a Pandas DataFrame containing the position of the Drive at each time point.
    trace_init_data : array_like
        The initial position of the Trace point, typically an array with two elements representing (x, y) coordinates.
    drag_init_data : array_like
        An array containing the initial positions of the Drag points, with shape (drag_number, 2) representing (x, y) coordinates for each Drag point.
    track_init_data : array_like
        An array containing the initial positions of the Track points, with shape (track_number, 2) representing (x, y) coordinates for each Track point.
    nose_gear_angle : float
        The angle of the nose gear of the aircraft, measured in degrees.

    Returns:
    -------
    dict
        A dictionary containing the following:
        - Drive (ndarray): An array of shape (2, data_number) storing the (x, y) coordinates of the Drive point at each time step.
        - Trace (ndarray): An array of shape (2, data_number) storing the (x, y) coordinates of the Trace point at each time step.
        - Drag (ndarray): An array of shape (drag_number, 2, data_number) storing the (x, y) coordinates of each Drag point at each time step.
        - Track (ndarray): An array of shape (track_number, 2, data_number) storing the (x, y) coordinates of each Track point at each time step.
        - Wing Center (ndarray): An array of shape (2, data_number) storing the position (x, y) of the wing center at each time step.
        - Tail Center (ndarray): An array of shape (2, data_number) storing the position (x, y) of the tail center at each time step.
        - Min Values (ndarray): An array of shape (2,) storing the minimum (x, y) values encountered during the calculations for plotting.
        - Max Values (ndarray): An array of shape (2,) storing the maximum (x, y) values encountered during the calculations for plotting.
    """
        
    # Convert nose gear angle to radians
    NGA_RAD = np.deg2rad(nose_gear_angle)

    # Initialize arrays for points
    Drive = np.zeros((2, data_number))
    Trace = np.zeros((2, data_number))
    Drag = np.zeros((drag_number, 2, data_number))
    Track = np.zeros((track_number, 2, data_number))
    wing_cen = np.zeros((2, data_number))
    tail_cen = np.zeros((2, data_number))
    Length_DD1 = np.zeros((drag_number,))
    Length_T = np.zeros((track_number,))
    Drag_pos = np.zeros((drag_number, 2))
    Track_pos = np.zeros((track_number, 2))
    min_vals = np.full(2, np.inf)
    max_vals = np.full(2, -np.inf)

    # Load initial values for Drive, Trace, Drag, Track
    Drive[:, 0] = drive_sequence.iloc[0].to_numpy()
    Trace[:, 0] = trace_init_data
    for i in range(drag_number):
        Drag[i, :, 0] = drag_init_data[i]
    for j in range(track_number):
        Track[j, :, 0] = track_init_data[j]

    # Apply rotation matrix if NGA_RAD != 0
    if NGA_RAD != 0:

        # Define rotation matrix for NGA_RAD
        rotation_matrix = np.array([
            [np.cos(NGA_RAD), -np.sin(NGA_RAD)],
            [np.sin(NGA_RAD), np.cos(NGA_RAD)]
        ])

        Trace[:, 0] = rotation_matrix @ (Trace[:, 0] - Drive[:, 0]) + Drive[:, 0]
        for i in range(drag_number):
            Drag[i, :, 0] = rotation_matrix @ (Drag[i, :, 0] - Drive[:, 0]) + Drive[:, 0]
        for j in range(track_number):
            Track[j, :, 0] = rotation_matrix @ (Track[j, :, 0] - Drive[:, 0]) + Drive[:, 0]


    # Calculate wing center as midpoint between Drive and Trace
    wing_cen[:, 0] = (Drive[:, 0] + Trace[:, 0]) / 2

    # Calculate tail center as 1.5 times the sum of Drive and Trace
    tail_cen[:, 0] = 1.5 * (Drive[:, 0] + Trace[:, 0])

    # Calculate initial orientation (theta) and distance between Drive and Trace
    dx = Trace[0, 0] - Drive[0, 0]
    dy = Trace[1, 0] - Drive[1, 0] 
    theta = np.atan2(dy, dx)
    Length_DTCE = np.sqrt(dx**2 + dy**2)


    # Calculate drag positions relative to initial Drive point
    # (Longitudinal and vertical distance of the drag points relative to the aircraft fuselage)
    for i in range(drag_number):
        dx_drag = Drag[i, 0, 0] - Drive[0, 0]
        dy_drag = Drag[i, 1, 0] - Drive[1, 0]
        Length_DD1[i] = np.sqrt(dx_drag ** 2 + dy_drag ** 2)

        phi_D1 = np.atan2(dy_drag, dx_drag)
        Drag_pos[i, 0] = Length_DD1[i] * np.cos(phi_D1 - theta)
        Drag_pos[i, 1] = Length_DD1[i] * np.sin(phi_D1 - theta)

    # Calculate track positions relative to initial Drive point
    # (Longitudinal and vertical distance of the track points relative to the aircraft fuselage)
    for j in range(track_number):
        dx_track = Track[j, 0, 0] - Drive[0, 0]
        dy_track = Track[j, 1, 0] - Drive[1, 0]
        Length_T[j] = np.sqrt(dx_track ** 2 + dy_track ** 2)

        phi = np.atan2(dy_track, dx_track)
        Track_pos[j, 0] = Length_T[j] * np.cos(phi - theta)
        Track_pos[j, 1] = Length_T[j] * np.sin(phi - theta)

    # Compute new positions for each data point
    for i in range(1, data_number):
        Drive[:, i] = drive_sequence.iloc[i].to_numpy()

        ################################ further improvement necessary?  ###############################
        # Calculate new theta based on drive and previous trace points
        dx_new = Trace[0, i - 1] - Drive[0, i]
        dy_new = Trace[1, i - 1] - Drive[1, i] 
        theta_new = np.atan2(dy_new, dx_new) 

        # TODO assumption: only rotation around the main landing gear???
        Trace[0, i] = Drive[0, i] + Length_DTCE * np.cos(theta_new)
        Trace[1, i] = Drive[1, i] + Length_DTCE * np.sin(theta_new)
        
        # Define rotation matrix for theta_new
        rotation_matrix_theta = np.array([
            [np.cos(theta_new), -np.sin(theta_new)],
            [np.sin(theta_new), np.cos(theta_new)]
        ])

        for k in range(drag_number):
            Drag[k, :, i] = rotation_matrix_theta @ Drag_pos[k, :] + Drive[:, i]

        #for k in range(drag_number):
        #    Drag[k, 0, i] = Drag_pos[k, 0] * np.cos(theta_new) - Drag_pos[k, 1] * np.sin(theta_new) + Drive[0, i]
        #    Drag[k, 1, i] = Drag_pos[k, 0] * np.sin(theta_new) + Drag_pos[k, 1] * np.cos(theta_new) + Drive[1, i]

        for j in range(track_number):
            Track[j, :, i] = rotation_matrix_theta @ Track_pos[j, :] + Drive[:, i]

        #for j in range(track_number):
        #    Track[j, 0, i] = Track_pos[j, 0] * np.cos(theta_new) - Track_pos[j, 1] * np.sin(theta_new) + Drive[0, i]
        #    Track[j, 1, i] = Track_pos[j, 0] * np.sin(theta_new) + Track_pos[j, 1] * np.cos(theta_new) + Drive[1, i]

        # Calculate wing center position
        wing_cen[:, i] = Drive[:, i] + 0.5 * Length_DTCE * np.array([np.cos(theta_new), np.sin(theta_new)])
        
        # Calculate tail center position
        tail_cen[:, i] = Drive[:, i] + 1.5 * Length_DTCE * np.array([np.cos(theta_new), np.sin(theta_new)])

        # Update min/max values for plotting
        for j in range(2):
            min_vals[j] = min(min_vals[j], Drive[j, i], Trace[j, i], wing_cen[j, i], tail_cen[j, i])
            max_vals[j] = max(max_vals[j], Drive[j, i], Trace[j, i], wing_cen[j, i], tail_cen[j, i])

    return {
        "Drive": Drive,
        "Trace": Trace,
        "Drag": Drag,
        "Track": Track,
        "Wing Center": wing_cen,
        "Tail Center": tail_cen,
        "Min Values": min_vals,
        "Max Values": max_vals
    }





