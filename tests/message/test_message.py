"""
This module contains test routines for the Message class.
"""

from components.fuel_type import Gasoline
from components.message import RequestMessage, DeliveryMessage, MessageStack
from components.port import PortInput, PortOutput

def test_create_request() -> None:
    input_port = PortInput(exchange=Gasoline())
    request_message = RequestMessage(sender_id="test_id",
                                     from_port=input_port,
                                     requested=100.0)
    print(request_message)
    assert isinstance(request_message, RequestMessage)

def test_create_delivery() -> None:
    output_port = PortOutput(exchange=Gasoline())
    delivery_message = DeliveryMessage(sender_id="test_id",
                                       from_port=output_port,
                                       delivery=100.0)
    print(delivery_message)
    assert isinstance(delivery_message, DeliveryMessage)

def test_create_stack() -> None:
    message_stack = MessageStack()
    assert isinstance(message_stack, MessageStack)
