import matplotlib.pyplot as plt

def make_plot(x_data, y_data):
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plotting the data
    ax.plot(x_data, y_data, label='y = 2x', marker='o', linestyle='-', color='b', linewidth=2)

    # Adding labels and title
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Simple Line Graph')

    # Adding a grid
    ax.grid(True)

    # Adding a legend
    ax.legend()

    # Show plot
    plt.show()

if __name__ == "__main__":
    # Data for plotting
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    make_plot(x, y)