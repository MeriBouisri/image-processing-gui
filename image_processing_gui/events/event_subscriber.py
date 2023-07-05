import logging
from .event_broker import EventBroker

class EventSubscriber:

    logger = logging.getLogger(__name__)

    def __init__(self, event_broker: EventBroker):
        self.event_broker = event_broker

    # ==================== SUBSCRIPTION METHODS ==================== #

    def subscribe(self, event, callback):
        self.event_broker.subscribe(event, callback)

    def subscribe_keyword(self, event_keyword, callback, index=None):
        self.event_broker.subscribe_keyword(event_keyword, callback, index)

    def subscribe_sequence(self, event_sequence, callback):
        self.event_broker.subscribe_sequence(event_sequence, callback)

    def subscribe_regex(self, event_regex, callback):
        self.event_broker.subscribe_regex(event_regex, callback)


    # ==================== UNSUBSCRIPTION METHODS ==================== #

    def unsubscribe(self, event, callback):
        self.event_broker.unsubscribe(event, callback)

    def unsubscribe_keyword(self, event_keyword, callback, index=None):
        self.event_broker.unsubscribe_keyword(event_keyword, callback, index)

    def unsubscribe_sequence(self, event_sequence, callback):
        self.event_broker.unsubscribe_sequence(event_sequence, callback)

    def unsubscribe_regex(self, event_regex, callback):
        self.event_broker.unsubscribe_regex(event_regex, callback)