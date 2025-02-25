import matplotlib.pyplot as plt

def plot_metrics(
    total_time: float,
    total_distance: int,
    serviced_count: int,
    throughput: float,
    output_file: str = "results/charts/metrics.png"
) -> None:
    """
    Generates a bar chart for the given performance metrics and saves the result.

    :param total_time: Total simulation time in seconds.
    :param total_distance: Total floors traveled by the lift.
    :param serviced_count: Total number of serviced requests.
    :param throughput: Throughput (requests per second).
    :param output_file: The path to save the chart image.
    """
    # Prepare metrics for the bar chart
    metrics = {
        "Total Time (s)": total_time,
        "Total Distance (floors)": total_distance,
        "Serviced Requests": serviced_count,
        "Throughput (req/s)": throughput
    }
    
    names = list(metrics.keys())
    values = list(metrics.values())

    # Create a figure and bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(names, values, color="skyblue")
    plt.title("Simulation Performance Metrics")
    plt.ylabel("Value")
    
    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()