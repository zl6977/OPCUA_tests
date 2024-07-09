from opcua import Client, ua

# Replace with the URL of your OPC UA server
server_url = "opc.tcp://localhost:4840"
server_url = "opc.tcp://milo.digitalpetri.com:62541/milo"
server_url = "opc.tcp://BGO-1043.ad.norceresearch.no:53530/OPCUA/SimulationServer"


def read_value(client, node_id):
    """
    Reads the value of the specified node.

    Parameters:
        node_id (str): The node ID of the data to be read.
    """
    node = client.get_node(node_id)
    value = node.get_value()
    print(f"Value of node {node_id}: {value}")


def browse_child_node(client, object_node_id):
    """
    Browses and prints the children of the specified node.

    Parameters:
        node (Node): The node to be browsed.
    """
    node = client.get_node(object_node_id)
    print("Parent " + list_node_attributes(node))
    children = node.get_children()
    for child in children:
        print("Children " + list_node_attributes(child))


def list_node_attributes(node):
    ret_str = f"Node: {node}"
    ret_str += "\n\t"
    ret_str += f"Browse Name: {node.get_browse_name()}"
    ret_str += "\n\t"
    ret_str += f"Node ID: {node.nodeid}"
    ret_str += "\n\t"
    ret_str += f"Node get_node_class: {ua.NodeClass(node.get_node_class()).name}"
    ret_str += "\n\t"
    ret_str += f"Node get_parent: {node.get_parent()}"
    # ret_str += "\n\t"
    # ret_str += f"Node get_value: {child.get_value()}"
    # ret_str += "\n\t"
    # ret_str += f"Node get_data_type: {child.get_data_type()}"
    # ret_str += "\n\t"
    # ret_str += f"Node get_data_value: {child.get_data_value()}"
    ret_str += "\n\t"
    ret_str += f"Node get_description: {node.get_description()}"
    ret_str += "\n\t"
    ret_str += f"Node get_display_name: {node.get_display_name()}"
    ret_str += "\n\t"
    ret_str += f"Node get_methods: {node.get_methods()}"
    return ret_str


def call_method(client, object_node_id, method_node_id, input_args):
    """
    Calls a method on the specified node with given input arguments.

    Parameters:
        object_node_id (str): The node ID of the parent object that has the method.
        method_node_id (str): The node ID of the method to be called.
        x_value (float): The input argument for the method.
    """
    object_node = client.get_node(object_node_id)
    method_node = client.get_node(method_node_id)
    # input_args = [ua.Variant(25, ua.VariantType.Double), ua.Variant(26, ua.VariantType.Double)]
    result = object_node.call_method(method_node, *input_args)
    print(f"Result of method call: {result}")

def call_method2(client, method_node_id, input_args):
    """
    Calls a method on the specified node with given input arguments.

    Parameters:
        method_node_id (str): The node ID of the method to be called.
        x_value (float): The input argument for the method.
    """
    method_node = client.get_node(method_node_id)
    # input_args = [ua.Variant(25, ua.VariantType.Double), ua.Variant(26, ua.VariantType.Double)]
    result = method_node.call_method(method_node, *input_args)
    print(f"Result of method call: {result}")

def main():
    """
    Main function that manages the connection to the OPC UA server and executes
    the read and method call operations.
    """
    try:
        # Connect to the server
        # Create a client instance
        client = Client(server_url)
        client.connect()
        print(f"Connected to {server_url}")

        # Example usage
        read_value(client, "i=2256")
        browse_child_node(client, "ns=6;s=MyDevice")
        input_args = [ua.Variant("sin", ua.VariantType.String), ua.Variant(60, ua.VariantType.Double)]
        call_method(client, "ns=6;s=MyDevice", "ns=6;s=MyMethod", input_args)
        # call_method2(client, "ns=6;s=MyMethod", input_args)

    except Exception as e:
        # Handle any exceptions that occur
        print(f"An error occurred: {e}")

    finally:
        # Ensure the client disconnects from the server
        client.disconnect()
        print(f"Disconnected from {server_url}")


if __name__ == "__main__":
    main()
