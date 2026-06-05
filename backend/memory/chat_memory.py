from collections import defaultdict



sessions = defaultdict(list)


def add_message(session_id, role, content):
    sessions[session_id].append(
        {
            "role": role,
            "content": content
        }
    )


def get_history(session_id):
    return sessions.get(session_id, [])


def clear_history(session_id):
    if session_id in sessions:
        del sessions[session_id]