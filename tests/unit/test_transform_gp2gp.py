from datetime import datetime, timedelta
from dateutil.tz import tzutc

from gp2gp.models.gp2gp import Transfer
from gp2gp.models.spine import Conversation, Message
from gp2gp.transformers.gp2gp import summarise_conversation


def test_summarise_conversation():
    messages = [
        Message(
            time=datetime(2019, 12, 31, 18, 44, 46, 647000, tzinfo=tzutc()),
            conversation_id="F8DAFCAA-5012-427B-BDB4-354256A4874B",
            guid="F8DAFCAA-5012-427B-BDB4-354256A4874B",
            interaction_id="urn:nhs:names:services:gp2gp/RCMR_IN010000UK05",
            from_party_ods="G85055",
            to_party_ods="G85674",
            message_ref="NotProvided",
            error_code=None,
        ),
        Message(
            time=datetime(2019, 12, 31, 18, 44, 58, 53000, tzinfo=tzutc()),
            conversation_id="F8DAFCAA-5012-427B-BDB4-354256A4874B",
            guid="54F949C0-DC7F-4EBC-8AE2-72BF2D0AF4EE",
            interaction_id="urn:nhs:names:services:gp2gp/RCMR_IN030000UK06",
            from_party_ods="G85674",
            to_party_ods="G85055",
            message_ref="NotProvided",
            error_code=None,
        ),
        Message(
            time=datetime(2019, 12, 31, 18, 44, 59, 381000, tzinfo=tzutc()),
            conversation_id="F8DAFCAA-5012-427B-BDB4-354256A4874B",
            guid="A5A34B66-9481-4F92-AB11-6494328B3C38",
            interaction_id="urn:nhs:names:services:gp2gp/MCCI_IN010000UK13",
            from_party_ods="G85674",
            to_party_ods="G85055",
            message_ref="F8DAFCAA-5012-427B-BDB4-354256A4874B",
            error_code=None,
        ),
        Message(
            time=datetime(2019, 12, 31, 19, 36, 52, 995000, tzinfo=tzutc()),
            conversation_id="F8DAFCAA-5012-427B-BDB4-354256A4874B",
            guid="209520E3-D6D5-4343-BA8F-AF857A8F9652",
            interaction_id="urn:nhs:names:services:gp2gp/MCCI_IN010000UK13",
            from_party_ods="G85055",
            to_party_ods="",
            message_ref="54F949C0-DC7F-4EBC-8AE2-72BF2D0AF4EE",
            error_code=None,
        ),
    ]

    conversation = Conversation("F8DAFCAA-5012-427B-BDB4-354256A4874B", messages)

    expected = Transfer(
        conversation_id="F8DAFCAA-5012-427B-BDB4-354256A4874B",
        sla_duration=timedelta(seconds=3114, microseconds=942000),
    )
    actual = summarise_conversation(conversation)

    assert actual == expected
