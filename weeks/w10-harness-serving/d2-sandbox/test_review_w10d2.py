import pytest

from review_w10d2 import safe_path


def test_review_sibling_prefix(tmp_path):
    (tmp_path / "work").mkdir()
    (tmp_path / "work-secrets").mkdir()
    with pytest.raises(PermissionError):
        safe_path(str(tmp_path / "work"), "../work-secrets/key")
