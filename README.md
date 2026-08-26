Security Log Analyzer

A beginner-friendly Python cybersecurity tool that analyzes authentication logs and detects repeated failed SSH login attempts.

Features

- Reads authentication log files
- Detects failed SSH login attempts
- Extracts IP addresses using Regular Expressions
- Counts failed login attempts for each IP
- Identifies potentially suspicious IP addresses
- Detects possible brute-force activity
- Displays a summary of analyzed IP addresses
- Shows the analysis date and time

How It Works

The program reads the selected log file line by line.

When it finds a line containing "Failed password", it extracts the source IP address and counts the failed attempt.

If an IP address has 3 or more failed attempts, the program classifies it as a possible brute-force source.

Example Output

==================================================
             SECURITY LOG ANALYSIS
==================================================
Generated: 2026-08-26 ...

Failed Login Attempts:

[BRUTE FORCE] 192.168.1.10 - 5 attempts
[NORMAL] 10.0.0.5 - 2 attempts
[NORMAL] 172.16.0.20 - 1 attempts

==================================================
                    SUMMARY
==================================================
Total IPs analyzed: 3
Suspicious IPs: 1
==================================================

Requirements

- Python 3.x
- No external Python libraries are required.

How to Run

Open Terminal in the project directory:

python3 Log_Analyzer.py

When prompted for a log file, enter the filename.

For the included demo file, simply press Enter:

Enter log file name (or press Enter for demo):

The program will use:

sample_auth.log

Project Structure

Log Analyzer/
├── Log_Analyzer.py
├── sample_auth.log
├── README.md
├── .gitignore
└── screenshots/
    └── output.png

Disclaimer

This project is created for educational and defensive cybersecurity purposes. The sample log data is for testing and demonstration only.