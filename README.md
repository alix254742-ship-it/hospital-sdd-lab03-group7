# Lab 03: Secure Coding and Static Analysis (Group 7)

## Group Members
*   **Ali Hamza** (UW-24-CY-BS-027)
*   **Saim Ali Shahid** (UW-24-CY-BS-020)
*   **M. Hammad** (UW-24-CY-BS-051)

## Scenario Description
We are auditing the **Hospital Patient Record Portal (Scenario 1)**. This Flask application allows doctors, nurses, lab technicians, and admins to manage patient records, prescriptions, and lab reports. The goal of this lab is to identify security vulnerabilities using Semgrep, fix them using OWASP secure coding practices, and prove the fixes with a re-scan.

## Findings Summary
*   **Baseline Scan:** 10 findings (High and Medium severity)
*   **After Fixes:** 0 findings

### Key Vulnerabilities Fixed:
1.  **SQL Injection:** Parameterized queries.
2.  **Weak Cryptography:** Replaced MD5 with Werkzeug's `generate_password_hash`.
3.  **Command Injection:** Removed `subprocess` and used strict `if/elif` allow-lists.
4.  **Path Traversal:** Used `send_from_directory`.
5.  **Broken Access Control:** Added `@require_role` to enforce RBAC.

## Repository Structure
*   `app/app.py` - The fixed, secure Flask application.
*   `reports/baseline.json` - The initial Semgrep scan results.
*   `rules/no-md5.yml` - Custom Semgrep rule to prevent MD5 usage.
*   `tests/test_login.py` - Test file demonstrating a false positive.
*   `screenshots/` - All evidence screenshots (Fig 1 to Fig 9).

## Top 3 Risks & Mitigations
1.  **SQL Injection (Critical):** Mitigated by using parameterized queries.
2.  **Broken Access Control (High):** Mitigated by adding `@require_role` decorators.
3.  **Command Injection (High):** Mitigated by removing `subprocess` and using safe string mapping.

## How to Run
1. Activate virtual environment: `source venv/bin/activate`
2. Scan the code: `semgrep --config p/owasp-top-ten --config p/python --config p/secrets --metrics=off app/`
