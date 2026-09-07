# REST API Quality Validation & Flask Endpoint Testing

A comprehensive API verification and automated testing framework validating RESTful HTTP endpoints, JSON payload schemas, latency SLAs, error handling, and concurrency stability.

## API Endpoint Reference
| Method | Endpoint | Description | Expected Status |
|---|---|---|---|
| `GET` | `/api/status` | Service health, version, uptime | `200 OK` |
| `GET` | `/api/telemetry` | Environmental & voltage telemetry | `200 OK` |
| `POST` | `/api/command` | Dispatch command (`start`, `stop`, `reset`) | `200 OK` / `400 Bad Request` |
| `GET` | `/api/stream/frame`| Video frame metadata and stream status | `200 OK` |
| `GET` | `/api/devices` | Connected hardware devices inventory | `200 OK` |
| `DELETE`| `/api/log` | Purges command history log | `204 No Content` |

## Test Suite Coverage
The pytest suite (`tests/test_api.py`) contains **25 comprehensive automated test cases**:
- **Status & Uptime:** Verifies JSON content type, required fields, and uptime continuity.
- **Telemetry Boundaries:** Physical range sanity checks for temperature, humidity, and supply voltage.
- **Command Sanitization:** Asserts rejection of malformed or unauthorized commands.
- **HTTP Contract Adherence:** Explicit verification of `404`, `405`, and `204` return codes.
- **Latency Benchmarks:** Sub-150ms latency assertion on health and telemetry calls.
- **Concurrency Testing:** Simulates multi-threaded burst requests without race conditions.

## Running Tests
```bash
# Install dependencies
pip install -r requirements.txt

# Run full test suite with verbose output
python run_tests.py

# Or directly with pytest
pytest tests/ -v

# Generate formal QA markdown report
python reports/generate_report.py
```
