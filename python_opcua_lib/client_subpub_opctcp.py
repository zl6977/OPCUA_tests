from opcua import Client
from opcua import ua
import time

class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription.
    """
    def datachange_notification(self, node, val, data):
        print(f"New data change event: Node {node}, Value {val}")

    def event_notification(self, event):
        print("New event", event)

def main():
    end_point = "opc.tcp://localhost:4840/freeopcua/server/"
    client = Client(end_point)
    try:
        client.connect()
        print("Connected to server.")

        # Get the variable node to subscribe to
        uri = "http://examples.freeopcua.github.io"
        idx = client.get_namespace_index(uri)
        myvar = client.get_node(f"ns={idx};i=2")

        # Create a subscription
        handler = SubHandler()
        subscription = client.create_subscription(1000, handler)
        handle = subscription.subscribe_data_change(myvar)

        # Run the subscription for a while
        time.sleep(1000)

        # Unsubscribe and delete the subscription
        subscription.unsubscribe(handle)
        subscription.delete()
        print("Subscription deleted.")

    finally:
        client.disconnect()
        print("Client disconnected.")

if __name__ == "__main__":
    main()
