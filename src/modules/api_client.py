import json
import os
import urllib.error
import urllib.request

from modules.service_result import ServiceResult


class ApiClient:
    def __init__(self):
        self.base_url = os.getenv("ERP_API_BASE_URL", "http://localhost:8080")
        self.token = ""
        self.current_user = ""
        self.current_role = ""
        self.current_scopes = []

    @property
    def enabled(self):
        value = os.getenv("ERP_USE_API", "true").strip().lower()
        return value in {"1", "true", "yes", "y"}

    def login(self, username, password):
        result = self._request(
            "POST",
            "/api/auth/login",
            payload={"username": username, "password": password},
            with_auth=False,
        )
        if not result.ok:
            return result
        body = result.payload
        self.token = body.get("token", "")
        self.current_user = body.get("username", "")
        self.current_role = body.get("role", "")
        me = self.me()
        if me.ok:
            self.current_scopes = me.payload.get("scopes", [])
            self.current_role = me.payload.get("role", self.current_role)
        return ServiceResult(ok=True, message="로그인 성공", payload=body)

    def me(self):
        return self._request("GET", "/api/auth/me")

    def get_inventory(self):
        return self._request("GET", "/api/inventory")

    def adjust_inventory(self, item_id, location_id, delta):
        return self._request(
            "POST",
            "/api/inventory/adjust",
            payload={"itemId": item_id, "locationId": location_id, "deltaQuantity": int(delta)},
        )

    def create_order(self, partner_id, item_id, quantity, unit):
        return self._request(
            "POST",
            "/api/orders",
            payload={
                "partnerId": partner_id,
                "lines": [{"itemId": item_id, "quantity": int(quantity), "unit": unit}],
            },
        )

    def hospital_consume(self, item_id, location_id, quantity, department, note):
        return self._request(
            "POST",
            "/api/workflows/hospital/consume",
            payload={
                "itemId": item_id,
                "locationId": location_id,
                "quantity": int(quantity),
                "department": department,
                "note": note,
            },
        )

    def ecommerce_return_exchange(self, item_id, return_location_id, ship_location_id, return_qty, exchange_qty, order_no):
        return self._request(
            "POST",
            "/api/workflows/ecommerce/return-exchange",
            payload={
                "itemId": item_id,
                "returnLocationId": return_location_id,
                "shipLocationId": ship_location_id,
                "returnQuantity": int(return_qty),
                "exchangeQuantity": int(exchange_qty),
                "marketplaceOrderNo": order_no,
            },
        )

    def list_approvals(self, status="PENDING"):
        suffix = ""
        if status:
            suffix = "?status=" + status
        return self._request("GET", "/api/approvals" + suffix)

    def create_approval(self, request_type, payload_dict):
        return self._request(
            "POST",
            "/api/approvals",
            payload={"requestType": request_type, "requestPayload": json.dumps(payload_dict, ensure_ascii=False)},
        )

    def approve(self, approval_id):
        return self._request("POST", f"/api/approvals/{approval_id}/approve", payload={})

    def reject(self, approval_id, reason):
        return self._request("POST", f"/api/approvals/{approval_id}/reject", payload={"reason": reason})

    def _request(self, method, path, payload=None, with_auth=True):
        if with_auth and not self.token:
            return ServiceResult(ok=False, message="API 토큰이 없습니다. 다시 로그인해 주세요.")

        url = self.base_url.rstrip("/") + path
        data = None
        headers = {"Content-Type": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        if with_auth and self.token:
            headers["Authorization"] = "Bearer " + self.token

        request = urllib.request.Request(url=url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                raw = response.read().decode("utf-8")
                body = json.loads(raw) if raw else {}
                return ServiceResult(ok=True, payload=body)
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8") if exc.fp else ""
            message = f"API 오류({exc.code})"
            try:
                parsed = json.loads(raw) if raw else {}
                if isinstance(parsed, dict) and parsed.get("message"):
                    message = parsed["message"]
            except json.JSONDecodeError:
                pass
            return ServiceResult(ok=False, message=message)
        except Exception as exc:
            return ServiceResult(ok=False, message=f"서버 연결 실패: {exc}")
