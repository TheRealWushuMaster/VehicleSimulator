"""
This module implements message delivery system for components
to exchange resources while simulating.
"""

from dataclasses import dataclass, field
from uuid import uuid4
from components.port import Port
from helpers.functions import assert_type, assert_type_and_range


@dataclass
class Message():
    """
    Base class for all simulation messages.
    """
    sender_id: str
    from_port: Port
    message_id: str=field(init=False)

    def __post_init__(self):
        assert_type(self.sender_id,
                    expected_type=str)
        assert_type(self.from_port,
                    expected_type=Port)
        self.message_id = f"Message-{uuid4()}"


@dataclass
class RequestMessage(Message):
    """
    Messages requesting a resource (power or fuel).
    These messages are broadcasted and may be responded
    by one or more components.
    """
    amount: float

    def __init__(self,
                 sender_id: str,
                 from_port: Port,
                 amount: float) -> None:
        super().__init__(sender_id=sender_id,
                         from_port=from_port)
        assert_type_and_range(amount,
                              more_than=0.0)
        self.amount = amount
        self.resource = from_port.exchange


@dataclass
class DeliveryMessage(RequestMessage):
    """
    Messages delivering a resource (power or fuel).
    These messages are sent by a specific component and
    directed to another specific component.
    """
    request_message_id: str
    receiver_id: str

    def __init__(self,
                 sender_id: str,
                 from_port: Port,
                 amount: float,
                 request_message_id: str,
                 receiver_id: str) -> None:
        super().__init__(sender_id=sender_id,
                         from_port=from_port,
                         amount=amount)
        assert_type(request_message_id, receiver_id,
                    expected_type=str)
        self.request_message_id = request_message_id
        self.receiver_id = receiver_id
