from dataclasses import dataclass
from typing import List, Dict


@dataclass
class UserAccount:
    name: str
    plan: str
    account_date: int
    duration: int


@dataclass
class EmailEvent:
    day: int
    message: str


def schedule_emails(send_schedule: Dict[str, str],
                    users: List[UserAccount]) -> List[EmailEvent]:
    events = []

    for user in users:
        start_day = user.account_date
        end_day = user.account_date + user.duration

        for key, email_type in send_schedule.items():
            if key == "start":
                send_day = start_day
            elif key == "end":
                send_day = end_day
            else:
                # Negative offset relative to end
                offset = int(key)
                send_day = end_day + offset

            message = f"[{email_type}] Subscription for {user.name} ({user.plan})"
            events.append(EmailEvent(send_day, message))

    return events


def main():
    # Example input (mirrors your Java example)
    send_schedule = {
        "start": "WELCOME",
        "-15": "RENEWAL_REMINDER",
        "end": "EXPIRATION"
    }

    users = [
        UserAccount("Alice", "Gold", 10, 30),
        UserAccount("Bob", "Silver", 5, 20),
    ]

    events = schedule_emails(send_schedule, users)

    # Sort by day
    events.sort(key=lambda e: e.day)

    # Output
    for e in events:
        print(f"{e.day}: {e.message}")


if __name__ == "__main__":
    main()
