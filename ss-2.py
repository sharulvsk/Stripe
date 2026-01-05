from dataclasses import dataclass
from typing import List, Dict, Callable


@dataclass
class UserAccount:
    name: str
    plan: str
    start_date: int
    duration: int


@dataclass
class PlanChange:
    name: str
    new_plan: str
    change_date: int


@dataclass
class Event:
    day: int
    message: str


def schedule_events(
    name: str,
    plan: str,
    start: int,
    end: int,
    send_schedule: Dict[str, str],
    events: List[Event],
    day_filter: Callable[[int], bool]
):
    for key, type_ in send_schedule.items():
        if key == "start":
            day = start
        elif key == "end":
            day = end
        else:
            offset = int(key)  # negative offset relative to end
            day = end + offset

        if day_filter(day):
            events.append(
                Event(day, f"[{type_}] Subscription for {name} ({plan})")
            )


def schedule(
    users: List[UserAccount],
    changes: List[PlanChange],
    send_schedule: Dict[str, str],
) -> List[Event]:

    change_map = {c.name: c for c in changes}
    events: List[Event] = []

    for user in users:
        original_start = user.start_date
        original_end = user.start_date + user.duration

        change = change_map.get(user.name)

        # 1. Events BEFORE plan change
        cutoff = change.change_date if change else float("inf")

        schedule_events(
            user.name,
            user.plan,
            original_start,
            original_end,
            send_schedule,
            events,
            lambda d, cutoff=cutoff: d < cutoff,
        )

        # 2. Handle plan change
        if change:
            events.append(
                Event(
                    change.change_date,
                    f"[Changed] Subscription for {user.name} ({change.new_plan})",
                )
            )

            remaining_duration = original_end - change.change_date
            new_start = change.change_date
            new_end = new_start + remaining_duration

            # Events AFTER (or on) plan-change day
            schedule_events(
                user.name,
                change.new_plan,
                new_start,
                new_end,
                send_schedule,
                events,
                lambda d, cd=change.change_date: d >= cd,
            )

    return events


def main():
    send_schedule = {
        "start": "WELCOME",
        "-10": "UPCOMING_EXPIRY",
        "end": "EXPIRED",
    }

    users = [
        UserAccount("Alice", "Gold", 10, 30),
    ]

    changes = [
        PlanChange("Alice", "Platinum", 25),
    ]

    events = schedule(users, changes, send_schedule)

    # Sort by day (like Comparator.comparingInt)
    events.sort(key=lambda e: e.day)

    for e in events:
        print(f"{e.day}: {e.message}")


if __name__ == "__main__":
    main()
