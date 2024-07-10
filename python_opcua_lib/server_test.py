from opcua import Server
from opcua import ua
import time
import math
from threading import Thread


def setup_server(end_point="opc.tcp://127.0.0.1:4840/freeopcua/server/"):
    # Create a server instance
    server = Server()

    # Set the endpoint URL
    server.set_endpoint(end_point)

    # Set server name
    server.set_server_name("Python OPC UA Server")

    # Set the URI for the namespace
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # Get Objects node (default node for adding objects)
    objects = server.get_objects_node()

    # Add a new object to the server
    my_obj = objects.add_object(idx, "MyObject")

    # Add variables to the object
    my_var = my_obj.add_variable(idx, "MyVariable", 6.7)
    my_var.set_writable()  # Set MyVariable to be writable

    # Add a method to the object
    def sqrt_method(parent, variant):
        value = variant.Value  # Extract the actual value from the ua.Variant
        return [ua.Variant(value**0.5, ua.VariantType.Double)]

    my_obj.add_method(
        idx, "SqrtMethod", sqrt_method, [ua.VariantType.Double], [ua.VariantType.Double]
    )

    return server, my_var


def update_variable(var):
    t = 0
    while True:
        # Calculate the new value as sin(t)
        value = math.sin(0.5 * t)
        # Update the variable's value
        var.set_value(ua.Variant(value, ua.VariantType.Float))
        # Increment t for the next calculation
        t += 1
        # Sleep for 1 second before the next update
        time.sleep(1)


def main():
    # Setup server and get the variable to update
    end_point = "opc.tcp://0.0.0.0:4840/freeopcua/server/"
    server, my_var = setup_server(end_point)

    # Start the server
    server.start()
    print("Server started at " + end_point)

    # Start the background thread to update the variable
    updater_thread = Thread(target=update_variable, args=(my_var,))
    updater_thread.daemon = (
        True  # Ensure the thread will close when the main program exits
    )
    updater_thread.start()

    try:
        # Keep the main thread running to keep the server alive
        while True:
            pass
            # time.sleep(1)
    except KeyboardInterrupt:
        # Stop the server on interrupt
        server.stop()
        print("Server stopped")


if __name__ == "__main__":
    main()
