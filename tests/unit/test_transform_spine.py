from datetime import datetime

from gp2gp.models.spine import Conversation
from gp2gp.transformers.spine import group_into_conversations
from tests.builders.spine import build_message


def group_into_conversations_produces_correct_number_of_conversations():
    message_one = build_message(conversation_id="abc")
    message_two = build_message(conversation_id="xyz")
    messages = [message_one, message_two]

    expected = [Conversation("abc", [message_one]), Conversation("xyz", [message_two])]

    actual = group_into_conversations(messages)

    assert list(actual) == expected


def group_into_conversations_produces_correct_number_of_messages_within_conversations():
    message_one = build_message(conversation_id="abc")
    message_two = build_message(conversation_id="abc")
    messages = [message_one, message_two]

    expected = [Conversation("abc", [message_one, message_two])]

    actual = group_into_conversations(messages)

    assert list(actual) == expected


def group_into_conversations_sorts_messages_within_conversations():
    message_one = build_message(conversation_id="abc", time=datetime(year=2020, month=6, day=6))
    message_two = build_message(conversation_id="abc", time=datetime(year=2020, month=6, day=5))
    messages = [message_one, message_two]

    expected = [Conversation("abc", [message_two, message_one])]

    actual = group_into_conversations(messages)

    assert list(actual) == expected
