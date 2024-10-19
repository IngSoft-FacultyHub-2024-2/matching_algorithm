from ..models import TeacherModel, RoleModel, SubClassModel, RoleType

def are_conflicts(assignment: dict[str, dict[str, list[str]]], teachers: dict[str, TeacherModel], 
                 classes: dict[str, RoleModel]) -> bool:
    for class_name, class_assigned_teachers in assignment.items():
        for selected_role, teachers_assigned in class_assigned_teachers.items():
            for teacher_name in teachers_assigned:
                if not teacher_can_teach_class(teachers[teacher_name], classes[class_name], selected_role):
                    print("teacher_cannot_teach_class")
                    return True
    # Check for weekly hours and time conflicts
    teachers_classes: dict[str, list[tuple[RoleModel, RoleType]]] = {}
    for class_name, class_assigned_teachers in assignment.items():
        for selected_role, teachers_assigned in class_assigned_teachers.items():
            for teacher_name in teachers_assigned:
                if teacher_name not in teachers_classes:
                    teachers_classes[teacher_name] = []
                teachers_classes[teacher_name].append((classes[class_name], selected_role))
    for teacher_name, classes_that_he_teach in teachers_classes.items():
        if teacher_has_more_than_weekly_hours(teachers[teacher_name], classes_that_he_teach):
            print("teacher_has_more_than_weekly_hours")
            return True
        if teacher_teach_more_than_one_class_at_same_time(teachers[teacher_name], classes_that_he_teach):
            print("teacher_teach_more_than_one_class_at_same_time")
            return True
    return False


def teacher_has_more_than_weekly_hours(teacher: TeacherModel, 
        classes_that_he_teach: list[tuple[RoleModel, RoleType]]) -> bool:
    weekly_hours = sum(
        sum(
            len(times) for times in get_subclass(class_, role).times.dict(exclude_none=True).values()
            if times is not None
        )
        for class_, role in classes_that_he_teach
    )
    return weekly_hours > teacher.weekly_hours_max_work


def teacher_teach_more_than_one_class_at_same_time(teacher: TeacherModel, 
        classes_that_he_teach: list[tuple[RoleModel, RoleType]]) -> bool:
    booked_time = {
        "Monday": {}, "Tuesday": {}, "Wednesday": {}, "Thursday": {}, "Friday": {}
    }
    
    for class_, role in classes_that_he_teach:
        subclass = get_subclass(class_, role)
        times_dict = subclass.times.dict(exclude_none=True)
        for day, times in times_dict.items():
            if times:  # Check if times is not None
                for time in times:
                    if time in booked_time[day]:
                        return True
                    booked_time[day][time] = True
    return False


def teacher_can_teach_class(teacher: TeacherModel, class_: RoleModel, selected_role: RoleType) -> bool:
    if not teacher_know_subject(teacher, class_.subject, selected_role):
        return False
    
    # Check if teacher is free at the time
    subclass = get_subclass(class_, selected_role)
    times_dict = subclass.times.dict(exclude_none=True)
    for day, times in times_dict.items():
        if times and not teacher_is_available_at_time(teacher, day, times):
            return False
    return True


def get_subclass(class_: RoleModel, role: RoleType) -> SubClassModel:
    return next(subclass for subclass in class_.subClasses if subclass.role == role)


def teacher_know_subject(teacher: TeacherModel, subject: str, selected_role: RoleType) -> bool:
    return any(
        subject_model.subject == subject and selected_role in subject_model.role
        for subject_model in teacher.subject_he_know_how_to_teach
    )


def teacher_is_available_at_time(teacher: TeacherModel, day: str, times: list[int]) -> bool:
    teacher_times = teacher.available_times.dict(exclude_none=True).get(day, [])
    return all(time in teacher_times for time in times)


if __name__ == "__main__":
    pass