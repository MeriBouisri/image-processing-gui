import logging
import re
from .event_constants import separator


class EventBroker:

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.subscriptions = {}

    # ==================== SUBSCRIPTION METHODS ==================== #

    def subscribe(self, event, callback):
        if event not in self.subscriptions:
            self.subscriptions[event] = []

        self.subscriptions[event].append(callback)

    def subscribe_keyword(self, event_keyword, callback, index=None):
        self._filter_events_containing_keyword(self.subscribe, event_keyword, callback, index)

    def subscribe_sequence(self, event_sequence, callback):
        self._filter_events_containing_sequence(self.subscribe, event_sequence, callback)

    def subscribe_regex(self, event_regex, callback):
        self._filter_events_matching_regex(self.subscribe, event_regex, callback)

    # ==================== UNSUBSCRIPTION METHODS ==================== #

    def unsubscribe(self, event, callback):
        if event not in self.subscriptions:
            return
        try:
            self.subscriptions[event].remove(callback)
        except ValueError:
            pass

    def unsubscribe_keyword(self, event_keyword, callback, index=None):
        self._filter_events_containing_keyword(self.unsubscribe, event_keyword, callback, index)

    def unsubscribe_sequence(self, event_sequence, callback):
        self._filter_events_containing_sequence(self.unsubscribe, event_sequence, callback)

    def unsubscribe_regex(self, event_regex, callback):
        self._filter_events_matching_regex(self.unsubscribe, event_regex, callback)


    # ==================== DISPATCH METHOD ==================== #

    def dispatch(self, event, *args, **kwargs):
        if event not in self.subscriptions:
            return

        for callback in self.subscriptions[event]:
            callback(event, *args, **kwargs)

    # ==================== UTILITARY METHODS ==================== #
    
    def _filter_events_containing_keyword(self, broker_function, event_keyword, callback, index=None):
        """
        Match events that contain a keyword at a specific index. This does not account for sequences,
        only for specific keywords delimited by the separator in the event_constants module.
        """
        for event_string in self.subscriptions.keys():
            split_event_string = event_string.split(separator)
            try:
                found_event = False
                if index is None:
                    found_event = event_keyword in split_event_string
                else:
                    found_event = split_event_string[index] == event_keyword

                if found_event:
                    broker_function(event_string, callback)
            except IndexError:
                continue
    
    def _filter_events_containing_sequence(self, broker_function, event_sequence, callback):
        """
        Match events that contain a sequence of keywords. This does not account for sequences,
        only for specific keywords delimited by the separator in the event_constants module.
        """
        event_key_list = self.subscriptions.keys()

        for event_string in self.subscriptions.keys():
            if event_sequence in event_string:
                broker_function(event_string, callback)

    def _filter_events_matching_regex(self, broker_function, regex, callback):
        """
        Match events using a regex pattern.
        """
        event_key_list = self.subscriptions.keys()
        regex = re.compile(regex)
        for event_string in event_key_list:
            if regex.match(event_string):
                broker_function(event_string, callback)