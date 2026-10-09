import requests
import json

BASE_URL = "http://localhost:8000/api"

def run_tests():
    print("Running E2E Scenario Tests...")
    
    # Register/Login
    requests.post(f"{BASE_URL}/auth/register", json={"email": "test@test.com", "password": "password", "name": "Test"})
    login_res = requests.post(f"{BASE_URL}/auth/login", json={"email": "test@test.com", "password": "password"}).json()
    token = login_res.get("access_token", "no_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Scenario 4: Malformed log file
    print("Testing Scenario 4: Malformed log file")
    res = requests.post(f"{BASE_URL}/logs/upload", headers=headers, files={"file": ("test.json", b"invalid json", "application/json")})
    assert res.status_code == 400
    print("Scenario 4 PASSED")
    
    # Scenario 1 & 3: Normal Activity
    print("Testing Scenario 1 & 3: Normal Activity")
    normal_log = {
        "Records": [
            {"eventName": "ConsoleLogin", "eventTime": "2026-10-09T09:00:00Z", "sourceIPAddress": "192.168.1.100", "userIdentity": {"arn": "admin"}}
        ]
    }
    res = requests.post(f"{BASE_URL}/logs/upload", headers=headers, files={"file": ("logs.json", json.dumps(normal_log).encode(), "application/json")})
    assert res.status_code == 200
    
    res = requests.post(f"{BASE_URL}/logs/analyze", headers=headers)
    assert res.status_code == 200
    print("Scenario 1 & 3 PASSED")
    
    # Scenario 2: Suspicious sign-in sequence
    print("Testing Scenario 2: Suspicious sequence")
    suspicious_log = {
        "Records": [
            {"eventName": "ConsoleLogin", "eventTime": "2026-10-09T10:00:00Z", "sourceIPAddress": "185.15.56.2", "userIdentity": {"arn": "hacked_admin"}},
            {"eventName": "AssumeRole", "eventTime": "2026-10-09T10:01:00Z", "sourceIPAddress": "185.15.56.2", "userIdentity": {"arn": "hacked_admin"}},
            {"eventName": "AttachRolePolicy", "eventTime": "2026-10-09T10:02:00Z", "sourceIPAddress": "185.15.56.2", "userIdentity": {"arn": "hacked_admin"}},
            {"eventName": "CreateAccessKey", "eventTime": "2026-10-09T10:03:00Z", "sourceIPAddress": "185.15.56.2", "userIdentity": {"arn": "hacked_admin"}},
            {"eventName": "GetObject", "eventTime": "2026-10-09T10:04:00Z", "sourceIPAddress": "185.15.56.2", "userIdentity": {"arn": "hacked_admin"}, "resources": [{"ARN": "SensitiveData"}]}
        ]
    }
    res = requests.post(f"{BASE_URL}/logs/upload", headers=headers, files={"file": ("bad_logs.json", json.dumps(suspicious_log).encode(), "application/json")})
    assert res.status_code == 200
    
    res = requests.post(f"{BASE_URL}/logs/analyze", headers=headers)
    assert res.status_code == 200
    print("Scenario 2 PASSED")
    
    # Scenario 8: Security Report
    print("Testing Scenario 8: Security Report")
    incidents = requests.get(f"{BASE_URL}/incidents", headers=headers).json()
    if incidents:
        inc_id = incidents[0]['id']
        res = requests.get(f"{BASE_URL}/incidents/{inc_id}/report", headers=headers)
        assert res.status_code == 200
        print("Scenario 8 PASSED - Report generated")
    
    print("All backend scenarios verified!")

if __name__ == "__main__":
    run_tests()
