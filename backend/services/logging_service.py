
from datetime import datetime, timezone

search_logs = []


def add_search_log(user_id, query):
    log = {
        "user_id": user_id,
        "query": query,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    search_logs.append(log)
    return log


def get_user_search_history(user_id):
    return [
        log for log in reversed(search_logs)
        if log["user_id"] == user_id
    ]


def clear_user_search_history(user_id):
    global search_logs

    previous_count = len(search_logs)

    search_logs = [
        log for log in search_logs
        if log["user_id"] != user_id
    ]

    return previous_count - len(search_logs)
