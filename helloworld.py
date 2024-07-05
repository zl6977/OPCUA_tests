from opcua import Client, ua

# Replace with the URL of your OPC UA server
server_url = "opc.tcp://localhost:4840"
server_url = "opc.tcp://milo.digitalpetri.com:62541/milo"

# Create a client instance
client = Client(server_url)


def read_value(node_id="ns=2;i=2"):
    try:
        # Connect to the server
        client.connect()
        print(f"Connected to {server_url}")

        # Replace with the node id of the data you want to read
        node_id = "ns=2;i=2"
        node = client.get_node(node_id)

        # Read the value of the node
        value = node.get_value()
        print(f"Value of node {node_id}: {value}")

    finally:
        # Disconnect from the server
        client.disconnect()
        print(f"Disconnected from {server_url}")


def browse_node(node):
    """Helper function to browse and print the children of a node"""
    print(f"Browsing children of node: {node}")
    children = node.get_children()
    for child in children:
        print(
            f"Child: {child} | Browse Name: {child.get_browse_name()} | Node ID: {child.nodeid}"
        )


def call_method(x_value):
    # Create a client instance
    client = Client(server_url)

    try:
        # Connect to the server
        client.connect()
        print(f"Connected to {server_url}")

        # Replace with the node id of the parent object that has the method
        object_node_id = "ns=2;s=Methods"
        object_node = client.get_node(object_node_id)

        browse_node(object_node)

        # The method node ID
        method_node_id = "ns=2;s=Methods/sqrt(x)"
        method_node = client.get_node(method_node_id)

        # Define the input arguments for the method (in this case, a single float)
        input_args = [ua.Variant(x_value, ua.VariantType.Double)]

        # Call the method directly on the method node
        result = object_node.call_method(method_node, *input_args)
        print(f"Result of method call: {result}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Disconnect from the server
        client.disconnect()
        print(f"Disconnected from {server_url}")


# Example usage
read_value()
call_method(25)
