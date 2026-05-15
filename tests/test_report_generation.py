from pathlib import Path

import pytest
from httpx import Response
from starlette.testclient import TestClient

from src.config import get_settings
from src.main import app


def send_message_to_chat(client: TestClient, user_id, message: str) -> Response:
    response = client.post(f"/chat?user_id={user_id}&show_history=true", json={"prompt": message})

    assert response.status_code == 200
    assert response.json() is not None
    assert response.cookies is not None

    return response


def collect_report_files(reports_dir: Path) -> set[Path]:
    if not reports_dir.exists():
        return set()
    return {path.resolve() for path in reports_dir.rglob("*.txt")}


def report_matches_user(report_file: Path, user_id: str) -> bool:
    if not report_file.is_file():
        return False

    user_id_lower = user_id.lower()
    if user_id_lower in report_file.name.lower():
        return True

    content = report_file.read_text(encoding="utf-8", errors="ignore")
    return user_id_lower in content.lower()

def clear_files(reports_dir: Path, user_id: str):
    old_files = collect_report_files(reports_dir)
    old_matching_reports = [file for file in old_files if report_matches_user(file, user_id)]

    for report_file in old_matching_reports:
        report_file.unlink(missing_ok=True)

class TestChatPersistence:

    @pytest.fixture()
    def client(self):
        return TestClient(app)

    def test_report_generation(self, client):
        user_id = str("Kurt Cobain")

        reports_dir = Path(get_settings().reports_dir)

        clear_files(reports_dir, user_id)
        old_files = collect_report_files(reports_dir)

        send_message_to_chat(client, user_id, "take the path a!")
        send_message_to_chat(client, user_id, "take the path a!")
        send_message_to_chat(client, user_id, "take the path b!")
        send_message_to_chat(client, user_id, "hmm not sure what to do..")
        send_message_to_chat(client, user_id, "take the path a!")
        send_message_to_chat(client, user_id, "take the path b!")

        files_after = collect_report_files(reports_dir)

        new_files = files_after - old_files
        matching_reports = [file for file in new_files if report_matches_user(file, user_id)]

        assert reports_dir.exists()
        assert new_files, f"Expected at least one new report file under {reports_dir}"
        assert matching_reports, f"Expected at least one new txt report associated with user_id {user_id}"

