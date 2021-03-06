from gp2gp.service.transformers import filter_pending_transfers
from tests.builders.service import build_transfer


def test_filter_pending_transfers_excludes_pending():
    pending_transfer = build_transfer(pending=True)

    transfers = [pending_transfer]

    actual = filter_pending_transfers(transfers)
    expected = []

    assert list(actual) == expected


def test_filter_pending_transfers_doesnt_exclude_completed():
    pending_transfer = build_transfer(pending=True)
    completed_transfer = build_transfer(pending=False)

    transfers = [pending_transfer, completed_transfer]

    actual = filter_pending_transfers(transfers)
    expected = [completed_transfer]

    assert list(actual) == expected
