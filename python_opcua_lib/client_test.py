import time
from opcua import Client
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from threading import Thread


def read_value(client, node_id, data):
    # Get the node
    node = client.get_node(node_id)

    while True:
        # Read the value of the node
        value = node.get_value()
        data.append(value)
        print(f"Read value: {value}")  # Print the value for debugging
        time.sleep(1)  # Read the value every second


def animate(i, data):
    plt.cla()  # Clear the current axes
    plt.plot(data)  # Plot the data
    plt.title("Real-time Plot of MyVariable")
    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.pause(0.1)  # Pause for a short time to update the plot


def main():
    # Replace with the URL of your OPC UA server
    server_url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
    node_id = "ns=2;i=2"  # Node ID of the variable to read
    # Create a client instance
    client = Client(server_url)
    client.connect()
    
    # Deque to store the latest data points for real-time plotting
    data = deque(maxlen=100)  # Keep the last 100 data points
    try:
        # Start a background thread to read the OPC UA variable
        reader_thread = Thread(target=read_value, args=(client, node_id, data))
        reader_thread.daemon = (
            True  # Ensure the thread will close when the main program exits
        )
        reader_thread.start()

        # Set up the real-time plot
        fig = plt.figure()
        ani = animation.FuncAnimation(
            fig, animate, fargs=(data,), interval=1000, cache_frame_data=False
        )  # Update the plot every second

        print("Starting the plot display...")
        plt.show()  # This will keep the plot window open

        print("Plot display ended.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Disconnect from the server
        client.disconnect()
        print(f"Disconnected from {server_url}")


if __name__ == "__main__":
    main()
