from datetime import datetime, timedelta

from gp2gp.service.transformers import derive_transfer
from tests.builders.spine import build_parsed_conversation, build_message


def test_derive_transfer_extracts_conversation_id():
    conversation = build_parsed_conversation(id="1234")
    transfer = derive_transfer(conversation)

    expected = "1234"
    actual = transfer.conversation_id
    assert actual == expected


def test_derive_transfer_produces_sla_of_successful_conversation():
    conversation = build_parsed_conversation(
        request_completed=build_message(
            time=datetime(year=2020, month=6, day=1, hour=12, minute=42, second=0),
        ),
        request_completed_ack=build_message(
            time=datetime(year=2020, month=6, day=1, hour=13, minute=52, second=0), error_code=None
        ),
    )

    transfer = derive_transfer(conversation)

    expected = timedelta(hours=1, minutes=10)
    actual = transfer.sla_duration
    assert actual == expected


def test_derive_transfer_produces_no_sla_given_pending_ehr_completed():
    conversation = build_parsed_conversation(
        request_started=build_message(), request_completed=None, request_completed_ack=None,
    )
    transfer = derive_transfer(conversation)

    expected = None
    actual = transfer.sla_duration
    assert actual == expected


def test_derive_transfer_produces_no_sla_given_pending_request_completed_ack():
    conversation = build_parsed_conversation(
        request_started=build_message(),
        request_completed=build_message(),
        request_completed_ack=None,
    )
    transfer = derive_transfer(conversation)

    expected = None
    actual = transfer.sla_duration
    assert actual == expected


def test_derive_transfer_extracts_requesting_practice_ods():
    conversation = build_parsed_conversation(request_started=build_message(from_party_ods="A12345"))

    transfer = derive_transfer(conversation)

    expected = "A12345"
    actual = transfer.requesting_practice_ods
    assert actual == expected


def test_derive_transfer_extracts_sending_practice_ods():
    conversation = build_parsed_conversation(request_started=build_message(to_party_ods="A12377"))

    transfer = derive_transfer(conversation)

    expected = "A12377"
    actual = transfer.sending_practice_ods
    assert actual == expected


def test_derive_transfer_extracts_error_code():
    conversation = build_parsed_conversation(request_completed_ack=build_message(error_code=99))

    transfer = derive_transfer(conversation)

    expected = 99
    actual = transfer.error_code
    assert actual == expected


def test_derive_transfer_doesnt_extract_error_code_given_pending_request_completed_ack():
    conversation = build_parsed_conversation(request_completed_ack=None)

    transfer = derive_transfer(conversation)

    expected = None
    actual = transfer.error_code
    assert actual == expected


def test_derive_transfer_flags_pending_request_completed_as_pending():
    conversation = build_parsed_conversation(
        request_started=build_message(), request_completed=None, request_completed_ack=None
    )

    transfer = derive_transfer(conversation)

    expected = True
    actual = transfer.pending
    assert actual == expected


def test_derive_transfer_flags_pending_request_completed_ack_as_pending():
    conversation = build_parsed_conversation(
        request_started=build_message(),
        request_completed=build_message(),
        request_completed_ack=None,
    )

    transfer = derive_transfer(conversation)

    expected = True
    actual = transfer.pending
    assert actual == expected


def test_derive_transfer_flags_completed_conversation_as_not_pending():
    conversation = build_parsed_conversation(
        request_started=build_message(),
        request_completed=build_message(),
        request_completed_ack=build_message(),
    )

    transfer = derive_transfer(conversation)

    expected = False
    actual = transfer.pending
    assert actual == expected