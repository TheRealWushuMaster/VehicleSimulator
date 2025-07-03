"""
This module implements message delivery system for components
to exchange resources while simulating.
"""

from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4
from components.port import Port, PortInput, PortOutput, PortBidirectional
from components.fuel_type import Fuel
from helpers.functions import assert_type, assert_type_and_range
from helpers.types import PowerType


@dataclass
class Message():
    """
    Base class for all message types.
    """
    sender_id: str
    from_port: Port
    message_id: str=field(init=False)
    resource: PowerType|Fuel=field(init=False)

    def __post_init__(self):
        assert_type(self.sender_id,
                    expected_type=str)
        assert_type(self.from_port,
                    expected_type=Port)
        self.message_id = f"Message-{uuid4()}"
        self.resource = self.from_port.exchange


@dataclass
class DeliveryMessage(Message):
    """
    Messages delivering the requested resources.
    Can fulfill a request entirely or partially.
    """
    delivery: float

    def __post_init__(self):
        assert_type_and_range(self.delivery,
                              more_than=0.0)
        assert_type(self.from_port,
                    expected_type=(PortOutput, PortBidirectional))
        super().__post_init__()


@dataclass
class RequestMessage(Message):
    """
    Messages requesting a resource (power or fuel).
    These messages are broadcasted and may be responded
    by one or more components.
    """
    requested: float
    deliveries: list[DeliveryMessage]=field(init=False)

    def __post_init__(self):
        assert_type(self.from_port,
                    expected_type=(PortInput, PortBidirectional))
        assert_type_and_range(self.requested,
                              more_than=0.0)
        super().__post_init__()
        self.deliveries = []

    @property
    def delivered(self) -> float:
        """
        Returns the amount of requested resource already delivered.
        """
        amount_delivered = sum(delivery.delivery for delivery in self.deliveries)
        return min(amount_delivered, self.requested)

    @property
    def fulfilled(self) -> bool:
        """
        Returns if the request has been fulfilled by a component.
        """
        return self.requested == self.delivered

    def add_delivery(self, delivery: DeliveryMessage) -> bool:
        """
        Adds a delivery to the request, if possible.
        Adjusts the delivered amount if it exceeds
        the request.
        """
        if not self.from_port.exchange == delivery.from_port.exchange:
            return False
        if delivery.from_port.direction == PortInput:
            return False
        if self.delivered + delivery.delivery > self.requested:
            delivery.delivery = self.requested - self.delivered
        if delivery.delivery > 0.0:
            self.deliveries.append(delivery)
        else:
            return False
        return True


@dataclass
class MessageStack():
    """
    Stack for requests to be resolved.
    """
    requests: list[RequestMessage]=field(default_factory=list)

    @property
    def count(self) -> int:
        """
        Returns the numer of requests in the stack.
        """
        return len(self.requests)

    @property
    def pending_count(self) -> int:
        """
        Returns the number of pending requests.
        """
        return sum(1 for pending in self.requests if not pending.fulfilled)

    @property
    def fulfilled_count(self) -> int:
        """
        Returns the number of fulfilled requests.
        """
        return sum(1 for pending in self.requests if pending.fulfilled)

    @property
    def pending_request(self) -> Optional[RequestMessage]:
        """
        Returns the last, unfulfilled request in
        the stack, which needs to be resolved first.
        """
        for request in reversed(self.requests):
            if not request.fulfilled:
                return request
        return None

    def add_request(self, request: RequestMessage) -> bool:
        """
        Add a new request to the stack.
        """
        assert_type(request,
                    expected_type=RequestMessage)
        if not request in self.requests:
            self.requests.append(request)
            return True
        return False
