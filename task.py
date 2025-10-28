from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Iterable, List, Optional, Set


@dataclass(slots=True)
class Teacher:
    first_name: str
    last_name: str
    age: int
    email: str
    can_teach_subjects: Set[str]
    assigned_subjects: Set[str] = field(default_factory=set)


def create_schedule(req_subjects: Iterable[str], teacher_list: List[Teacher]) -> Optional[List[Teacher]]:
    uncovered: Set[str] = set(req_subjects)
    if not uncovered:
        return []

    chosen: List[Teacher] = []
    used_indices: Set[int] = set()

    can_sets = [teacher.can_teach_subjects for teacher in teacher_list]
    ages = [teacher.age for teacher in teacher_list]

    while uncovered:
        best_idx = -1
        best_assigned: Set[str] = set()
        best_cover = 0
        best_age = 10**9

        for idx, can_set in enumerate(can_sets):
            if idx in used_indices:
                continue
            assigned_now = can_set & uncovered
            cover = len(assigned_now)
            if cover == 0:
                continue

            age = ages[idx]
            if cover > best_cover or (cover == best_cover and age < best_age):
                best_idx = idx
                best_assigned = assigned_now
                best_cover = cover
                best_age = age

        if best_idx == -1:
            return None

        base_teacher = teacher_list[best_idx]
        picked = replace(base_teacher, assigned_subjects=set(best_assigned))

        uncovered.difference_update(best_assigned)
        used_indices.add(best_idx)
        chosen.append(picked)

    return chosen


def main() -> None:
    # Множина предметів
    subjects_input = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}

    # Список викладачів
    teachers_input = [
        Teacher('Олександр', 'Іваненко', 45, 'o.ivanenko@example.com', {'Математика', 'Фізика'}),
        Teacher('Марія', 'Петренко', 38, 'm.petrenko@example.com', {'Хімія'}),
        Teacher('Сергій', 'Коваленко', 50, 's.kovalenko@example.com', {'Інформатика', 'Математика'}),
        Teacher('Наталія', 'Шевченко', 29, 'n.shevchenko@example.com', {'Біологія', 'Хімія'}),
        Teacher('Дмитро', 'Бондаренко', 35, 'd.bondarenko@example.com', {'Фізика', 'Інформатика'}),
        Teacher('Олена', 'Гриценко', 42, 'o.grytsenko@example.com', {'Біологія'}),
    ]

    # Створення розкладу
    schedule = create_schedule(subjects_input, teachers_input)

    # Виведення
    if schedule:
        print("Розклад занять:")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(sorted(teacher.assigned_subjects))}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")


if __name__ == '__main__':
    main()
