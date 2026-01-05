from dataclasses import dataclass
from typing import List, Dict, Callable


# ===================== MODELS =====================

@dataclass
class UserAccount:
    name: str
    plan: str
    start: int
    duration: int


class ChangeEvent:
    def name(self) -> str: ...
    def date(self) -> int: ...


@dataclass
class PlanChange(ChangeEvent):
    name_val: str
    new_plan: str
    change_date: int

    def name(self) -> str:
        return self.name_val

    def date(self) -> int:
        return self.change_date


@dataclass
class Renewal(ChangeEvent):
    name_val: str
    extension: int
    change_date: int

    def name(self) -> str:
        return self.name_val

    def date(self) -> int:
        return self.change_date


@dataclass
class Event:
    day: int
    message: str


# ===================== SCHEDULER =====================

def schedule_emails(
    events: List[Event],
    schedule: Dict[str, str],
    name: str,
    plan: str,
    start: int,
    end: int,
    day_filter: Callable[[int], bool]
):
    for key, label in schedule.items():
        if key == "start":
            day = start
        elif key == "end":
            day = end
        else:
            day = end + int(key)

        if day_filter(day):
            events.append(
                Event(day, f"[{label}] Subscription for {name} ({plan})")
            )


def schedule(
    users: List[UserAccount],
    changes: List[ChangeEvent],
    send_schedule: Dict[str, str]
) -> List[Event]:

    events: List[Event] = []

    # Group changes by user and sort by date
    changes_by_user: Dict[str, List[ChangeEvent]] = {}
    for c in changes:
        changes_by_user.setdefault(c.name(), []).append(c)

    for lst in changes_by_user.values():
        lst.sort(key=lambda c: c.date())

    for user in users:
        start = user.start
        end = user.start + user.duration
        plan = user.plan

        # Initial schedule
        schedule_emails(events, send_schedule, user.name, plan, start, end, lambda d: True)

        user_changes = changes_by_user.get(user.name, [])

        for change in user_changes:
            change_date = change.date()

            # Remove future notifications beyond change date
            events[:] = [
                e for e in events
                if not (
                    e.day > change_date
                    and f"Subscription for {user.name}" in e.message
                )
            ]

            # Renewal
            if isinstance(change, Renewal):
                events.append(
                    Event(change_date, f"[Renewed] Subscription for {user.name} ({plan})")
                )
                end += change.extension

            # Plan change
            if isinstance(change, PlanChange):
                events.append(
                    Event(change_date, f"[Changed] Subscription for {user.name} ({change.new_plan})")
                )
                remaining = end - change_date
                start = change_date
                end = start + remaining
                plan = change.new_plan

            # Reschedule with updated timeline
            schedule_emails(
                events,
                send_schedule,
                user.name,
                plan,
                start,
                end,
                lambda d, cd=change_date: d >= cd
            )

    return events


# ===================== DEMO / MAIN =====================

def main():
    send_schedule = {
        "start": "WELCOME",
        "-10": "UPCOMING_EXPIRY",
        "end": "EXPIRED",
    }

    users = [
        UserAccount("Alice", "Gold", 10, 30)
    ]

    changes = [
        Renewal("Alice", 10, 20),
        PlanChange("Alice", "Platinum", 30)
    ]

    result = schedule(users, changes, send_schedule)
    result.sort(key=lambda e: e.day)

    for e in result:
        print(f"{e.day}: {e.message}")


if __name__ == "__main__":
    main()
