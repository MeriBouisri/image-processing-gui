import logging
from .event_broker import EventBroker

class EventPublisher:

    logger = logging.getLogger(__name__)

    def __init__(self, event_broker: EventBroker):
        self.event_broker = event_broker

    def publish(self, event, *args, **kwargs):
        self.event_broker.dispatch(event, *args, **kwargs)