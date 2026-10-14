from datetime import datetime
import re


def analyze_logs(filename):
    failed_logins = {}

    try:
        with open(filename, "r") as file:
            for line in file:
                if "Failed password" in line:
                    ip_match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
                    if ip_match:
                        ip = ip_match.group(1)
                        failed_logins[ip] = failed_logins.get(ip, 0) + 1

    except FileNotFoundError:
        return {
            "error": f"File '{filename}' was not found."
        }

    results = []

    for ip, count in failed_logins.items():
        if count >= 5:
            status = "BRUTE FORCE"
        elif count >= 3:
            status = "SUSPICIOUS"
        else:
            status = "NORMAL"

        results.append({
            "ip": ip,
            "attempts": count,
            "status": status
        })

    suspicious_ips = sum(
        1 for count in failed_logins.values() if count >= 3
    )

    return {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_ips": len(failed_logins),
        "suspicious_ips": suspicious_ips,
        "results": results
    }


if __name__ == "__main__":
    filename = input(
        "Enter log file name (or press Enter for demo): "
    ).strip()

    if not filename:
        filename = "sample_auth.log"

    report = analyze_logs(filename)

    if "error" in report:
        print(report["error"])
    else:
        print("\n" + "=" * 50)
        print("        SECURITY LOG ANALYSIS")
        print("=" * 50)
        print(f"Generated: {report['generated']}\n")
        print("Failed Login Attempts:")
        print("-" * 30)

        for item in report["results"]:
            print(
                f"[{item['status']}] {item['ip']} - "
                f"{item['attempts']} attempts"
            )

        print("\n" + "=" * 50)
        print("              SUMMARY")
        print("=" * 50)
        print(f"Total IPs analyzed: {report['total_ips']}")
        print(f"Suspicious IPs: {report['suspicious_ips']}")
        print("=" * 50)