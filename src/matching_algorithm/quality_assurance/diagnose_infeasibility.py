from ..models import ClassModel, TeacherModel


def diagnose_infeasibility(
    teachers: dict[str, TeacherModel], classes: dict[str, ClassModel]
) -> list[str]:
    issues: list[str] = []

    # Check if there are enough teachers for each subject
    for class_name, class_info in classes.items():
        for subclass in class_info.subClasses:
            required_teachers = subclass.num_teachers
            available_teachers = sum(
                1
                for teacher_info in teachers.values()
                if any(
                    subject.subject == class_info.subject and subclass.role in subject.role
                    for subject in teacher_info.subject_he_know_how_to_teach
                )
            )
            if available_teachers < required_teachers:
                issues.append(
                    f"Not enough teachers for {class_name} {subclass.role}. "
                    f"Need {required_teachers}, have {available_teachers}"
                )

    # Check if class times match teacher availability
    for class_name, class_info in classes.items():
        for subclass in class_info.subClasses:
            teachers_available = False
            subclass_times = subclass.times.dict(exclude_none=True)

            for teacher_info in teachers.values():
                # Check if teacher can teach the subject and role
                can_teach = any(
                    subject.subject == class_info.subject and subclass.role in subject.role
                    for subject in teacher_info.subject_he_know_how_to_teach
                )

                if can_teach:
                    # Get teacher's available times
                    teacher_times = teacher_info.available_times.dict(exclude_none=True)

                    # Check if teacher is available at all required times
                    is_available = all(
                        all(time in teacher_times.get(day, []) for time in times)
                        for day, times in subclass_times.items()
                        if times is not None  # Handle optional times
                    )

                    if is_available:
                        teachers_available = True
                        break

            if not teachers_available:
                issues.append(
                    f"No available teachers found for {class_name} {subclass.role} "
                    f"at specified times"
                )

    return issues
