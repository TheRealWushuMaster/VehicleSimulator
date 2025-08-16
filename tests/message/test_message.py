"""
This module contains test routines for the Message class.
"""

from components.fuel_type import Fuel, Gasoline
from components.message import RequestMessage, DeliveryMessage, MessageStack
from components.port import PortInput, PortOutput
from helpers.types import PowerType

def create_request(exchange: PowerType|Fuel,
                   requested: float) -> RequestMessage:
    input_port = PortInput(exchange=exchange)
    request_message = RequestMessage(sender_id="test_id",
                                     from_port=input_port,
                                     requested=requested)
    print(request_message)
    assert isinstance(request_message, RequestMessage)
    return request_message

def create_delivery(exchange: PowerType|Fuel,
                    delivery: float) -> DeliveryMessage:
    output_port = PortOutput(exchange=exchange)
    delivery_message = DeliveryMessage(sender_id="test_id",
                                       from_port=output_port,
                                       delivery=delivery)
    print(delivery_message)
    assert isinstance(delivery_message, DeliveryMessage)
    return delivery_message

def add_request_to_stack(message: RequestMessage) -> MessageStack:
    message_stack = test_create_stack()
    message_stack.add_request(request=message)
    assert message_stack.count > 0
    return message_stack

def add_delivery_to_request(message_stack: MessageStack,
                            delivery_message: DeliveryMessage) -> None:
    request_message = message_stack.pending_request
    assert request_message is not None
    request_message.add_delivery(delivery=delivery_message)
    assert 0.0 <= request_message.delivered <= request_message.requested
    assert request_message.delivered
    assert isinstance(request_message, RequestMessage)

#=================================================================

def test_create_gasoline_request() -> RequestMessage:
    request_message = create_request(exchange=Gasoline(),
                                     requested=100.0)
    return request_message

def test_create_gasoline_delivery() -> DeliveryMessage:
    delivery_message = create_delivery(exchange=Gasoline(),
                                       delivery=100.0)
    return delivery_message

def test_create_ac_electric_request() -> RequestMessage:
    request_message = create_request(exchange=PowerType.ELECTRIC_AC,
                                     requested=80.0)
    return request_message

def test_create_dc_electric_request() -> RequestMessage:
    request_message = create_request(exchange=PowerType.ELECTRIC_DC,
                                     requested=80.0)
    return request_message

def test_create_ac_electric_delivery() -> DeliveryMessage:
    delivery_message = create_delivery(exchange=PowerType.ELECTRIC_AC,
                                       delivery=80.0)
    return delivery_message

def test_create_dc_electric_delivery() -> DeliveryMessage:
    delivery_message = create_delivery(exchange=PowerType.ELECTRIC_DC,
                                       delivery=80.0)
    return delivery_message

def test_create_mechanical_request() -> RequestMessage:
    request_message = create_request(exchange=PowerType.MECHANICAL,
                                     requested=50.0)
    return request_message

def test_create_mechanical_delivery() -> DeliveryMessage:
    delivery_message = create_delivery(exchange=PowerType.MECHANICAL,
                                       delivery=50.0)
    return delivery_message

def test_create_stack() -> MessageStack:
    message_stack = MessageStack()
    assert isinstance(message_stack, MessageStack)
    return message_stack

def test_add_gasoline_request_to_stack() -> MessageStack:
    request_message = test_create_gasoline_request()
    message_stack = add_request_to_stack(message=request_message)
    return message_stack

def test_add_gasoline_delivery_to_request() -> None:
    message_stack = test_add_gasoline_request_to_stack()
    delivery_message = test_create_gasoline_delivery()
    add_delivery_to_request(message_stack=message_stack,
                            delivery_message=delivery_message)

def test_add_ac_electric_request_to_stack() -> MessageStack:
    request_message = test_create_ac_electric_request()
    message_stack = add_request_to_stack(message=request_message)
    return message_stack

def test_add_dc_electric_request_to_stack() -> MessageStack:
    request_message = test_create_dc_electric_request()
    message_stack = add_request_to_stack(message=request_message)
    return message_stack

def test_add_ac_electric_delivery_to_request() -> None:
    message_stack = test_add_ac_electric_request_to_stack()
    delivery_message = test_create_ac_electric_delivery()
    add_delivery_to_request(message_stack=message_stack,
                            delivery_message=delivery_message)

def test_add_dc_electric_delivery_to_request() -> None:
    message_stack = test_add_dc_electric_request_to_stack()
    delivery_message = test_create_dc_electric_delivery()
    add_delivery_to_request(message_stack=message_stack,
                            delivery_message=delivery_message)

def test_add_mechanical_request_to_stack() -> MessageStack:
    request_message = test_create_mechanical_request()
    message_stack = add_request_to_stack(message=request_message)
    return message_stack

def test_add_mechanical_delivery_to_request() -> None:
    message_stack = test_add_mechanical_request_to_stack()
    delivery_message = test_create_mechanical_delivery()
    add_delivery_to_request(message_stack=message_stack,
                            delivery_message=delivery_message)
