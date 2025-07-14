import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_trajectory(results, obstacles=True):
    """
    Visualize the Drive, Trace, Drag, and Track.

    Parameters:    
    -----------
        results : A dictionary containing the following:
        - Drive (ndarray): An array of shape (2, data_number) storing the (x, y) coordinates of the Drive point at each time step.
        - Trace (ndarray): An array of shape (2, data_number) storing the (x, y) coordinates of the Trace point at each time step.
        - Drag (ndarray): An array of shape (drag_number, 2, data_number) storing the (x, y) coordinates of each Drag point at each time step.
        - Track (ndarray): An array of shape (track_number, 2, data_number) storing the (x, y) coordinates of each Track point at each time step.
        - Wing Center (ndarray): An array of shape (2, data_number) storing the position (x, y) of the wing center at each time step.
        - Tail Center (ndarray): An array of shape (2, data_number) storing the position (x, y) of the tail center at each time step.
        - Min Values (ndarray): An array of shape (2,) storing the minimum (x, y) values encountered during the calculations for plotting.
        - Max Values (ndarray): An array of shape (2,) storing the maximum (x, y) values encountered during the calculations for plotting.
    """
    Drive = results["Drive"]
    Trace = results["Trace"]
    Drag = results["Drag"]
    Track = results["Track"]
    wing_cen = results["Wing Center"]
    tail_cen = results["Tail Center"]

    olive_color = (128 / 255, 128 / 255, 0 / 255)

    plt.figure(figsize=(12, 8))

    # Plot Drive trajectory
    plt.plot(Drive[0], Drive[1], label='Drive', color='black', linewidth=2)

    # Plot Trace trajectory
    plt.plot(Trace[0], Trace[1], label='Trace', color='blue', linewidth=2)

    # Plot Drag trajectories
    for i in range(0, Drag.shape[0]):  
        plt.plot(Drag[i, 0], Drag[i, 1], label=f'Drag {i+1}', linestyle='--')

    # Plot Track trajectories
    for j in range(0, Track.shape[0]):  
        plt.plot(Track[j, 0], Track[j, 1], label=f'Track {j+1}', linestyle=':')


    # Calculate start, middle, and end indices
    indices = [0, Drive.shape[1] // 2, Drive.shape[1] - 1]

    # Add intermittent lines every `step` points
    for i in indices: 
        # Track point 1 and wing center
        plt.plot([Track[0, 0, i], wing_cen[0, i]], [Track[0, 1, i], wing_cen[1, i]], 
                 linestyle='-', color=olive_color , linewidth=3)

        # Track point 2 and wing center
        plt.plot([Track[1, 0, i], wing_cen[0, i]], [Track[1, 1, i], wing_cen[1, i]], 
                 linestyle='-', color=olive_color , linewidth=3)

        # Track point 3 and tail center
        plt.plot([Track[2, 0, i], tail_cen[0, i]], [Track[2, 1, i], tail_cen[1, i]], 
                 linestyle='-', color=olive_color , linewidth=3)

        # Track point 4 and tail center
        plt.plot([Track[3, 0, i], tail_cen[0, i]], [Track[3, 1, i], tail_cen[1, i]], 
                 linestyle='-', color=olive_color , linewidth=3)

        # Track point 5 and tail center
        plt.plot([Track[4, 0, i], tail_cen[0, i]], [Track[4, 1, i], tail_cen[1, i]], 
                 linestyle='-', color=olive_color , linewidth=3)

        # Nose gear point
        plt.plot(Drive[0,i], Drive[1,i], marker='o', markersize=8, color='red')

        # Drag 1 point
        plt.plot(Drag[0,0,i], Drag[0,1,i], marker='o', markersize=8, color='blue')

        # Drag 2 point
        plt.plot(Drag[1,0,i], Drag[1,1,i], marker='o', markersize=8, color='blue')

    # Add two rectangular obstacles with X marks
    # Define positions and sizes for obstacles
    if obstacles:
        obstacle_1_pos = (25, -4.1)  # (x, y) position
        obstacle_1_size = (40, 45)   # (width, height)
        
        obstacle_2_pos = (-65, -4.1)
        obstacle_2_size = (40, 45)

        # Draw obstacles as rectangles
        obstacle_1 = patches.Rectangle(obstacle_1_pos, *obstacle_1_size, linewidth=3, edgecolor='black', facecolor='none')
        obstacle_2 = patches.Rectangle(obstacle_2_pos, *obstacle_2_size, linewidth=3, edgecolor='black', facecolor='none')
        plt.gca().add_patch(obstacle_1)
        plt.gca().add_patch(obstacle_2)

        # Draw X marks in the center of each obstacle
        for obstacle_pos, obstacle_size in zip([obstacle_1_pos, obstacle_2_pos], [obstacle_1_size, obstacle_2_size]):
            x_center = obstacle_pos[0] + obstacle_size[0] / 2
            y_center = obstacle_pos[1] + obstacle_size[1] / 2
            x_delta = obstacle_size[0] / 4
            y_delta = obstacle_size[1] / 4

            # Draw "X" by plotting two crossing lines
            plt.plot([x_center - x_delta, x_center + x_delta], [y_center - y_delta, y_center + y_delta], color='black', linewidth=3)
            plt.plot([x_center - x_delta, x_center + x_delta], [y_center + y_delta, y_center - y_delta], color='black', linewidth=3)

    # Set legend
    plt.legend()

    # Set axis labels and title
    plt.xlabel('X in [m]')
    plt.ylabel('Y in [m]')
    plt.title('Path Visualization')

    # Set grid
    plt.grid(True)

    # Show the plot
    plt.axis('equal')  # Make the aspect ratio equal
    plt.show()



