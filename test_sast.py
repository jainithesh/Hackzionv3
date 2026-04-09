# test_sast.py
from ai_sast import analyze_raw_code

print("Scanning new package for zero-day threats...")
is_safe, report = analyze_raw_code("malicious_payload.js")

if not is_safe:
    print("\n🚨 SYSTEM BLOCKED INSTALLATION 🚨")
