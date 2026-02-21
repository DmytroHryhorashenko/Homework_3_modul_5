import sys
from typing import List, Dict


def parse_log_line(line: str) -> Dict[str, str]:

    parts = line.strip().split(" ", 3)

    if len(parts) < 4:
        raise ValueError(f"Неправильний формат рядка: {line}")

    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "message": parts[3],
    }


def load_logs(file_path: str) -> List[Dict[str, str]]:

    logs = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    logs.append(parse_log_line(line))
    except FileNotFoundError:
        print(f"Помилка: файл '{file_path}' не знайдено.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)

    return logs


def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:

    level = level.upper()
    return list(filter(lambda log: log["level"] == level, logs))


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:

    counts = {}

    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1

    return counts


def display_log_counts(counts: Dict[str, int]) -> None:

    print("\nРівень логування | Кількість")
    print("-----------------|----------")

    for level, count in counts.items():
        print(f"{level:<17}| {count}")


def main():
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях_до_файлу> [рівень]")
        sys.exit(1)

    file_path = sys.argv[1]
    level_filter = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)

    display_log_counts(counts)

    if level_filter:
        filtered_logs = filter_logs_by_level(logs, level_filter)

        print(f"\nДеталі логів для рівня '{level_filter.upper()}':")

        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()