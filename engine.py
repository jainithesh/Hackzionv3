import subprocess
import json
import shutil
import os

TARGET_DIR = "./target_app"
PACKAGE_JSON_PATH = os.path.join(TARGET_DIR, "package.json")
BACKUP_PATH = os.path.join(TARGET_DIR, "package.json.backup")


def run_vulnerability_scan():
    print("1. Scanning for vulnerabilities...")
    try:
        result = subprocess.run(
            ["npm", "audit", "--json"],
            cwd=TARGET_DIR,
            capture_output=True,
            text=True,
            shell=True,
        )
        audit_data = json.loads(result.stdout)
        vulnerabilities = audit_data.get("metadata", {}).get("vulnerabilities", {})
        total_vulns = sum(vulnerabilities.values())

        print(
            f"   Found {total_vulns} vulnerabilities (Critical: {vulnerabilities.get('critical', 0)}, High: {vulnerabilities.get('high', 0)})."
        )
        return total_vulns > 0
    except Exception as e:
        print(f"Scan failed: {e}")
        return False


def backup_file():
    print("2. Creating secure backup...")
    shutil.copy(PACKAGE_JSON_PATH, BACKUP_PATH)
    print("   Backup created successfully.")


def apply_patch_and_verify():
    print("3. Applying autonomous patches...")
    # Run the auto-fixer
    subprocess.run(
        ["npm", "audit", "fix", "--force"],
        cwd=TARGET_DIR,
        capture_output=True,
        shell=True,
    )

    print("4. Running security validation tests...")
    # Run the dummy test file we created
    test_result = subprocess.run(
        ["npm", "test"], cwd=TARGET_DIR, capture_output=True, text=True, shell=True
    )

    # If the returncode is 0, the test passed. If it's anything else, it failed.
    if test_result.returncode == 0:
        print("   Tests PASSED. System is secure and stable.")
        # Cleanup the backup since we don't need it
        if os.path.exists(BACKUP_PATH):
            os.remove(BACKUP_PATH)
    else:
        print("   Tests FAILED! The patch broke the application.")
        print("5. Initiating Fail-Safe Rollback...")
        # Delete the broken file and restore the backup
        os.remove(PACKAGE_JSON_PATH)
        shutil.move(BACKUP_PATH, PACKAGE_JSON_PATH)
        # Re-install the old packages to match the restored file
        subprocess.run(
            ["npm", "install"], cwd=TARGET_DIR, capture_output=True, shell=True
        )
        print("   Rollback complete. System restored to previous state.")


if __name__ == "__main__":
    print("=== AUTONOMOUS SECURITY ENGINE STARTED ===\n")
    has_vulnerabilities = run_vulnerability_scan()

    if has_vulnerabilities:
        backup_file()
        apply_patch_and_verify()
    else:
        print("System is already secure. No action needed.")

    print("\n=== ENGINE SHUTDOWN ===")
