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
    requested: float
    delivered: float=field(init=False)

    def __init__(self,
                 sender_id: str,
                 from_port: Port,
                 amount: float) -> None:
        super().__init__(sender_id=sender_id,
                         from_port=from_port)
        assert_type_and_range(amount,
                              more_than=0.0)
        self.requested = amount
        self.delivered = 0.0
        self.resource = from_port.exchange

    @property
    def fulfilled(self) -> bool:
        """
        Returns if the request has been fulfilled by a component.
        """
        return self.requested == self.delivered


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


@dataclass
class RequestStack():
    """
    Stack for requests to be resolved.
    """
    requests: list[RequestMessage]=field(init=False)
    count: int=field(init=False)

    def __post_init__(self):
        self.requests = []
        self.count = 0

    @property
    def last_request(self) -> RequestMessage:
        """
        Returns the last request in the stack,
        which needs to be resolved first.
        """
        return self.requests[-1]

    def fulfill_last_request(self) -> bool:
        """
        Checks if the last request has been fulfilled fully.
        """
        last_request = self.last_request
        if last_request.requested == last_request.delivered:
            del self.requests[-1]
            return True
        return False

    def add_request(self, request: RequestMessage):
        """
        Add a new request to the stack.
        """
        assert_type(request,
                    expected_type=RequestMessage)
        if not request in self.requests:
            self.requests.append(request)
            self.count += 1

    def supply_request(self, supply: float):
        """
        Supplies resources to the current (last) request.
        The request is removed if supplied entirely.
        """
        assert_type_and_range(supply,
                              more_than=0.0)
        last_request = self.last_request
        self.last_request.delivered = min(last_request.delivered + supply, last_request.requested)
        self.fulfill_last_request()
