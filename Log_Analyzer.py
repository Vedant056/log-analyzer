from datetime import datetime
import re


def analyze_logs(filename):
    failed_logins = {}

    print("\n" + "=" * 50)
    print("        SECURITY LOG ANALYSIS")
    print("=" * 50)
    print(f"Generated: {datetime.now()}\n")

    try:
        with open(filename, "r") as file:
            for line in file:

                # Check for failed SSH login
                if "Failed password" in line:

                    # Extract IP address from the log line
                    ip_match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)

                    if ip_match:
                        ip = ip_match.group(1)

                        # Count failed attempts for each IP
                        failed_logins[ip] = failed_logins.get(ip, 0) + 1

    except FileNotFoundError:
        print(f"Error: File '{filename}' was not found.")
        return

    # Display results
    print("Failed Login Attempts:")
    print("-" * 30)

    for ip, count in failed_logins.items():

        if count >= 5:
            print(f"[BRUTE FORCE] {ip} - {count} attempts")

        elif count >= 3:
            print(f"[SUSPICIOUS] {ip} - {count} attempts")

        else:
            print(f"[NORMAL] {ip} - {count} attempts")

    print("\n" + "=" * 50)
    print("              SUMMARY")
    print("=" * 50)

    print(f"Total IPs analyzed: {len(failed_logins)}")

    suspicious_ips = sum(1 for count in failed_logins.values() if count >= 3)

    print(f"Suspicious IPs: {suspicious_ips}")
    print("=" * 50)


# Ask the user for the log file
filename = input("Enter log file name (or press Enter for demo): ").strip()
if not filename:
    filename = "sample_auth.log"

analyze_logs(filename)