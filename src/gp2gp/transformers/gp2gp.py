from typing import Iterator

from gp2gp.models.gp2gp import Transfer
from gp2gp.models.spine import Conversation, Message


def summarise_conversation(conversation: Conversation) -> Transfer:
    parser = SpineConversationParser(iter(conversation.messages))
    sla = parser.parse()
    return Transfer(conversation.id, sla)


EHR_REQUEST_STARTED = "urn:nhs:names:services:gp2gp/RCMR_IN010000UK05"
EHR_REQUEST_COMPLETED = "urn:nhs:names:services:gp2gp/RCMR_IN030000UK06"
APP_ACKNOWLEDGEMENT = "urn:nhs:names:services:gp2gp/MCCI_IN010000UK13"


"""
class SpineConversationParser:
    def __init__(self, messages: Iterator[Message]):
        self.messages = list(messages)
        self.req_complete_message = None
        self.final_ack = None

    def parse(self):
        # if self.messages[0].interaction_id != EHR_REQUEST_STARTED:
        for message in self.messages:
            if message.interaction_id == EHR_REQUEST_COMPLETED:
                self._consume_ehr_request_completed(message)
            if message.interaction_id == APP_ACKNOWLEDGEMENT and message.message_ref == self.req_complete_message.guid:
                self._consume_final_ack(message)
                break

        if self.req_complete_message is not None and self.final_ack is not None:
            return self.final_ack.time - self.req_complete_message.time

    def _consume_ehr_request_completed(self, message):
        self.req_complete_message = message

    def _consume_final_ack(self, message):
        self.final_ack = message

"""

class SpineConversationParser:

    def __init__(self, messages: Iterator[Message]):
        self._messages = messages

    def _advance_until_interaction(self, interaction_id):
        return self._advance_until(lambda m: m.interaction_id == interaction_id)

    def _advance_until_acknowledgment_of(self, message):
        return self._advance_until(lambda m: m.interaction_id == APP_ACKNOWLEDGEMENT and m.message_ref == message.guid)

    def _advance_until(self, func):
        next_message = next(self._messages)
        while not func(next_message):
            next_message = next(self._messages)
        return next_message

    def parse(self):
        #TODO: validate conversation starts with REQ
        req_complete_message = self._advance_until_interaction(EHR_REQUEST_COMPLETED)
        final_ack = self._advance_until_acknowledgment_of(req_complete_message)
        return final_ack.time - req_complete_message.time