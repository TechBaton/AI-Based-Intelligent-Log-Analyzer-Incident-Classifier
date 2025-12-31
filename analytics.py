from collections import defaultdict
from datetime import timedelta

# --------------------------------------------------
# 1. Executive Summary
# --------------------------------------------------
def generate_executive_summary(logs):
    services = set()
    incident_types = set()
    timestamps = []

    for log in logs:
        services.add(log["service"])
        incident_types.add(log["clean_message"])
        timestamps.append(log["timestamp"])

    if not timestamps:
        return "No significant incidents detected."

    return (
        f"Between {min(timestamps)} and {max(timestamps)}, "
        f"the system recorded {len(incident_types)} distinct incident types "
        f"across {len(services)} services. "
        f"Some incidents occurred repeatedly, indicating potential system instability "
        f"that may require investigation."
    )




# --------------------------------------------------
# 2. Priority Ranking (What to look at first)
# --------------------------------------------------
def rank_incidents(logs):
    incident_map = defaultdict(list)

    for log in logs:
        key = (log["service"], log["clean_message"])
        incident_map[key].append(log["timestamp"])

    ranked = []

    for (service, message), times in incident_map.items():
        ranked.append({
            "service": service,
            "message": message[:120],
            "frequency": len(times),
            "last_seen": max(times)
        })

    ranked.sort(
        key=lambda x: (x["frequency"], x["last_seen"]),
        reverse=True
    )

    return ranked
