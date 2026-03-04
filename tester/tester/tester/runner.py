import time
import json
from tester.client import APIClient
from tester.tests import *

def run_all_tests():
    client = APIClient("https://api.agify.io")
    results = []
    latencies = []

    tests = [
        test_status_ok,
        test_json_valid,
        test_fields_present,
        test_types,
        test_error_empty_name,
        test_timeout
    ]

    for test in tests:
        start = time.time()
        try:
            test(client)
            duration = time.time() - start
            results.append({"test": test.__name__, "status": "passed"})
            latencies.append(duration)
        except Exception as e:
            results.append({"test": test.__name__, "status": "failed", "error": str(e)})

    return {
        "passed": len([r for r in results if r["status"] == "passed"]),
        "failed": len([r for r in results if r["status"] == "failed"]),
        "latency_avg": sum(latencies) / len(latencies),
        "latency_p95": sorted(latencies)[int(len(latencies)*0.95)-1],
        "results": results
    }
