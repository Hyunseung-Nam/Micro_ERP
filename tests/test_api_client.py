"""
목적: ApiClient의 HTTP 통신 로직을 Mock으로 검증한다.
대상: modules/api_client.py
"""
import io
import json
import os
import unittest
import urllib.error
import urllib.request
from unittest.mock import MagicMock, patch

from modules.api_client import ApiClient


def _make_http_response(body: dict, status: int = 200):
    """urllib.request.urlopen 응답을 흉내 내는 context manager Mock을 반환한다."""
    raw = json.dumps(body).encode("utf-8")
    mock_resp = MagicMock()
    mock_resp.read.return_value = raw
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


def _make_http_error(code: int, body: dict | None = None):
    """urllib.error.HTTPError를 생성한다."""
    raw = json.dumps(body).encode("utf-8") if body else b""
    fp = io.BytesIO(raw)
    return urllib.error.HTTPError(url="http://x", code=code, msg="err", hdrs={}, fp=fp)


class ApiClientEnabledTests(unittest.TestCase):
    """enabled 프로퍼티 환경변수 처리 검증."""

    def test_enabled_true_by_default(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("ERP_USE_API", None)
            client = ApiClient()
            self.assertTrue(client.enabled)

    def test_enabled_false_when_env_is_false(self):
        with patch.dict(os.environ, {"ERP_USE_API": "false"}):
            client = ApiClient()
            self.assertFalse(client.enabled)

    def test_enabled_true_when_env_is_1(self):
        with patch.dict(os.environ, {"ERP_USE_API": "1"}):
            client = ApiClient()
            self.assertTrue(client.enabled)


class ApiClientLoginTests(unittest.TestCase):
    """login 메서드 검증."""

    def _client(self):
        return ApiClient()

    @patch("urllib.request.urlopen")
    def test_successful_login_stores_token_and_returns_ok(self, mock_urlopen):
        login_body = {"token": "tok123", "username": "admin", "role": "ADMIN"}
        me_body = {"scopes": ["READ", "WRITE"], "role": "ADMIN"}

        call_count = [0]

        def side_effect(req, timeout=10):
            call_count[0] += 1
            if call_count[0] == 1:
                return _make_http_response(login_body)
            return _make_http_response(me_body)

        mock_urlopen.side_effect = side_effect

        client = self._client()
        result = client.login("admin", "pass")

        self.assertTrue(result.ok)
        self.assertEqual(client.token, "tok123")
        self.assertEqual(client.current_user, "admin")
        self.assertEqual(client.current_role, "ADMIN")
        self.assertIn("READ", client.current_scopes)

    @patch("urllib.request.urlopen")
    def test_failed_login_http_error_returns_not_ok(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(401, {"message": "인증 실패"})
        client = self._client()
        result = client.login("bad", "wrong")
        self.assertFalse(result.ok)
        self.assertIn("인증 실패", result.message)


class ApiClientRequestTests(unittest.TestCase):
    """_request 메서드 공통 동작 검증."""

    def _authed_client(self, token="test-token"):
        client = ApiClient()
        client.token = token
        return client

    def test_request_without_token_returns_error(self):
        client = ApiClient()
        result = client.me()  # token 없음
        self.assertFalse(result.ok)
        self.assertIn("토큰", result.message)

    @patch("urllib.request.urlopen")
    def test_successful_get_returns_ok_with_payload(self, mock_urlopen):
        mock_urlopen.return_value = _make_http_response({"items": []})
        client = self._authed_client()
        result = client.get_inventory()
        self.assertTrue(result.ok)
        self.assertIn("items", result.payload)

    @patch("urllib.request.urlopen")
    def test_http_error_with_message_field_returned(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(403, {"message": "권한 없음"})
        client = self._authed_client()
        result = client.get_inventory()
        self.assertFalse(result.ok)
        self.assertIn("권한 없음", result.message)

    @patch("urllib.request.urlopen")
    def test_http_error_without_body_returns_generic_message(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(500)
        client = self._authed_client()
        result = client.get_inventory()
        self.assertFalse(result.ok)
        self.assertIn("500", result.message)

    @patch("urllib.request.urlopen")
    def test_connection_error_returns_not_ok(self, mock_urlopen):
        mock_urlopen.side_effect = ConnectionRefusedError("refused")
        client = self._authed_client()
        result = client.get_inventory()
        self.assertFalse(result.ok)
        self.assertIn("연결 실패", result.message)

    @patch("urllib.request.urlopen")
    def test_auth_header_sent_when_token_present(self, mock_urlopen):
        mock_urlopen.return_value = _make_http_response({})
        client = self._authed_client("mytoken")
        client.get_inventory()
        req = mock_urlopen.call_args[0][0]
        self.assertIn("Bearer mytoken", req.get_header("Authorization"))

    @patch("urllib.request.urlopen")
    def test_empty_response_body_returns_empty_payload(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.read.return_value = b""
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp
        client = self._authed_client()
        result = client.get_inventory()
        self.assertTrue(result.ok)
        self.assertEqual(result.payload, {})


class ApiClientApprovalTests(unittest.TestCase):
    """승인 관련 메서드 검증."""

    def _authed_client(self):
        c = ApiClient()
        c.token = "tok"
        return c

    @patch("urllib.request.urlopen")
    def test_list_approvals_passes_status_param(self, mock_urlopen):
        mock_urlopen.return_value = _make_http_response([])
        client = self._authed_client()
        client.list_approvals(status="PENDING")
        req = mock_urlopen.call_args[0][0]
        self.assertIn("PENDING", req.full_url)

    @patch("urllib.request.urlopen")
    def test_approve_calls_correct_path(self, mock_urlopen):
        mock_urlopen.return_value = _make_http_response({"status": "APPROVED"})
        client = self._authed_client()
        result = client.approve("APR-123")
        self.assertTrue(result.ok)
        req = mock_urlopen.call_args[0][0]
        self.assertIn("APR-123", req.full_url)

    @patch("urllib.request.urlopen")
    def test_reject_sends_reason_in_payload(self, mock_urlopen):
        mock_urlopen.return_value = _make_http_response({})
        client = self._authed_client()
        client.reject("APR-999", "재고 부족")
        req = mock_urlopen.call_args[0][0]
        sent_body = json.loads(req.data.decode("utf-8"))
        self.assertEqual(sent_body["reason"], "재고 부족")


if __name__ == "__main__":
    unittest.main()
