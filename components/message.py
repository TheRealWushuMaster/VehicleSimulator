"""
This module implements message delivery system for components
to exchange resources while simulating.
"""

from dataclasses import dataclass, field
from uuid import uuid4
from components.port import Port
from components.fuel_type import Fuel
from helpers.functions import assert_type, assert_type_and_range
from helpers.types import PowerType


@dataclass
class RequestMessage():
    """
    Messages requesting a resource (power or fuel).
    These messages are broadcasted and may be responded
    by one or more components.
    """
    sender_id: str
    from_port: Port
    requested: float
    message_id: str=field(init=False)
    delivered: float=field(init=False)
    resource: PowerType|Fuel=field(init=False)

    def __post_init__(self) -> None:
        assert_type(self.sender_id,
                    expected_type=str)
        assert_type(self.from_port,
                    expected_type=Port)
        self.message_id = f"Message-{uuid4()}"
        self.delivered = 0.0
        self.resource = self.from_port.exchange

    @property
    def fulfilled(self) -> bool:
        """
        Returns if the request has been fulfilled by a component.
        """
        return self.requested == self.delivered


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
            # Need to upgrade the state of the message sender
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
