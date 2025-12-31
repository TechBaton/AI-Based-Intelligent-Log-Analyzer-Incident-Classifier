import re
from datetime import datetime

log_file_path = "app.log"
parsed_logs = []

# Common patterns (optional matches)
TIMESTAMP_PATTERNS = [
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",     # 2016-09-29 00:01:47
    r"\d{4}/\d{2}/\d{2}:\d{2}:\d{2}:\d{2}",     # 2016/09/27:20:30:31
]

LEVEL_PATTERN = r"\b(INFO|ERROR|WARN|WARNING|DEBUG|FATAL|TRACE)\b"

SERVICE_PATTERN = r"\b(CBS|CSI|auth-service|payment-service|inventory-service)\b"

with open(log_file_path, "r", encoding="utf-8", errors="ignore") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue

        timestamp = "UNKNOWN"
        level = "UNKNOWN"
        service = "UNKNOWN"
        message = line

        # 1️⃣ Timestamp detection
        for pattern in TIMESTAMP_PATTERNS:
            match = re.search(pattern, line)
            if match:
                timestamp = match.group()
                break

        # 2️⃣ Log level detection
        level_match = re.search(LEVEL_PATTERN, line, re.IGNORECASE)
        if level_match:
            level = level_match.group().upper()

        # 3️⃣ Service / component detection
        service_match = re.search(SERVICE_PATTERN, line)
        if service_match:
            service = service_match.group()

        # 4️⃣ Message extraction (remove detected fields)
        message = line
        if timestamp != "UNKNOWN":
            message = message.replace(timestamp, "")
        if level != "UNKNOWN":
            message = re.sub(level, "", message, flags=re.IGNORECASE)
        if service != "UNKNOWN":
            message = message.replace(service, "")

        message = re.sub(r"\s+", " ", message).strip()

        parsed_logs.append({
            "timestamp": timestamp,
            "level": level,
            "service": service,
            "message": message
        })

# Preview safely
for log in parsed_logs[:20]:
    print(log)
