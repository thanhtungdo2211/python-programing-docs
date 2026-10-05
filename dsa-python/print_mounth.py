"""Print a calendar month with Sunday as the first day of the week."""

import calendar


def print_month(month: int | str, year: int) -> None:
    """Print a month selected by its number or full English name."""
    if isinstance(month, str):
        try:
            month_number = list(calendar.month_name).index(month)
        except ValueError as error:
            raise ValueError(f"Unknown month name: {month!r}") from error
    else:
        month_number = month
    if not 1 <= month_number <= 12:
        raise ValueError("month must be between 1 and 12")

    month_name = calendar.month_name[month_number]
    weeks = calendar.Calendar(firstweekday=calendar.SUNDAY).monthdayscalendar(
        year, month_number
    )
    print(f"{month_name} {year}".center(20))
    print("Su Mo Tu We Th Fr Sa")
    for week in weeks:
        print(" ".join(f"{day:2}" if day else "  " for day in week).rstrip())


def main() -> None:
    print_month("February", 2020)
    print()
    print_month("December", 2021)


if __name__ == "__main__":
    main()
