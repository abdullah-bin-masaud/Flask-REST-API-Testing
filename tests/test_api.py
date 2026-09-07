"""
Quality Assurance and Validation Test Suite.
Validates HTTP response codes, payload structures, schema types, latency, and concurrency.
"""
import pytest
import time
import concurrent.futures


class TestStatusEndpoint:
    def test_status_code_200(self, client):
        res = client.get("/api/status")
        assert res.status_code == 200

    def test_status_content_type_json(self, client):
        res = client.get("/api/status")
        assert "application/json" in res.content_type

    def test_status_payload_keys(self, client):
        data = client.get("/api/status").get_json()
        assert "status" in data
        assert "uptime_seconds" in data
        assert "version" in data

    def test_status_value_online(self, client):
        data = client.get("/api/status").get_json()
        assert data["status"] == "online"

    def test_uptime_is_non_negative(self, client):
        data = client.get("/api/status").get_json()
        assert data["uptime_seconds"] >= 0


class TestTelemetryEndpoint:
    def test_telemetry_status_200(self, client):
        res = client.get("/api/telemetry")
        assert res.status_code == 200

    def test_telemetry_keys_present(self, client):
        data = client.get("/api/telemetry").get_json()
        for key in ["temperature", "humidity", "cpu_load", "voltage"]:
            assert key in data

    def test_temperature_within_physical_bounds(self, client):
        data = client.get("/api/telemetry").get_json()
        assert -40.0 <= data["temperature"] <= 85.0

    def test_humidity_percentage_valid(self, client):
        data = client.get("/api/telemetry").get_json()
        assert 0.0 <= data["humidity"] <= 100.0

    def test_voltage_nominal_5v(self, client):
        data = client.get("/api/telemetry").get_json()
        assert 4.5 <= data["voltage"] <= 5.5


class TestCommandEndpoint:
    def test_valid_command_start(self, client):
        res = client.post("/api/command", json={"command": "start"})
        assert res.status_code == 200
        assert res.get_json()["result"] == "acknowledged"

    def test_valid_command_stop(self, client):
        res = client.post("/api/command", json={"command": "stop"})
        assert res.status_code == 200

    def test_valid_command_reset(self, client):
        res = client.post("/api/command", json={"command": "reset"})
        assert res.status_code == 200

    def test_valid_command_calibrate(self, client):
        res = client.post("/api/command", json={"command": "calibrate"})
        assert res.status_code == 200

    def test_missing_json_payload_returns_400(self, client):
        res = client.post("/api/command", data="not json", content_type="text/plain")
        assert res.status_code == 400

    def test_unrecognized_command_returns_400(self, client):
        res = client.post("/api/command", json={"command": "malicious_hack"})
        assert res.status_code == 400
        assert "Invalid or missing command" in res.get_json()["error"]

    def test_command_wrong_http_method_returns_405(self, client):
        res = client.get("/api/command")
        assert res.status_code == 405


class TestStreamEndpoint:
    def test_stream_frame_status_200(self, client):
        res = client.get("/api/stream/frame")
        assert res.status_code == 200

    def test_stream_frame_schema(self, client):
        data = client.get("/api/stream/frame").get_json()
        assert "frame_id" in data
        assert "resolution" in data
        assert data["resolution"] == "640x480"


class TestDeviceInventory:
    def test_devices_list_returns_200(self, client):
        res = client.get("/api/devices")
        assert res.status_code == 200

    def test_devices_count_matches(self, client):
        data = client.get("/api/devices").get_json()
        assert data["count"] == len(data["devices"])


class TestErrorAndLifecycleHandling:
    def test_nonexistent_endpoint_returns_404(self, client):
        res = client.get("/api/nonexistent/route")
        assert res.status_code == 404

    def test_clear_log_returns_204(self, client):
        res = client.delete("/api/log")
        assert res.status_code == 204


class TestLatencyAndPerformance:
    def test_status_latency_under_150ms(self, client):
        start = time.perf_counter()
        res = client.get("/api/status")
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert res.status_code == 200
        assert elapsed_ms < 150.0

    def test_telemetry_latency_under_150ms(self, client):
        start = time.perf_counter()
        res = client.get("/api/telemetry")
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert res.status_code == 200
        assert elapsed_ms < 150.0


class TestConcurrency:
    def test_concurrent_status_requests(self, client):
        """Simulate concurrent client sessions."""
        def hit_endpoint():
            res = client.get("/api/status")
            return res.status_code

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(hit_endpoint) for _ in range(15)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        assert all(code == 200 for code in results)
