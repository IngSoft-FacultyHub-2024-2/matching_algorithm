# assignment: {class: {'Theory': ['teacher1'], 'Practice': ['teacher1']}}

def are_conflicts(assignment, teachers, classes):
    for class_name, class_assigned_teachers in assignment.items():
        for selected_role, teachers_assigned in class_assigned_teachers.items():
            for teacher_name in teachers_assigned:
                if not teacher_can_teach_class(teachers[teacher_name], classes[class_name], selected_role):
                    print("teacher_can_teach_class")
                    return True
        
    # iterate over all teachers check if they have more than weekly hours and if they teach more than one class at the same time
    teachers_classes = {}
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

def teacher_has_more_than_weekly_hours(teacher, classes_that_he_teach):
    weekly_hours = sum(sum(len(times) for times in get_subclass(class_, role)["times"].values()) for class_, role in classes_that_he_teach)
    return weekly_hours > teacher["weekly_hours_max_work"]

def teacher_teach_more_than_one_class_at_same_time(teacher, classes_that_he_teach):
    booked_time = {"Monday": {}, "Tuesday": {}, "Wednesday": {}, "Thursday": {}, "Friday": {}}
    for class_, role in classes_that_he_teach:
        subclasses = get_subclass(class_, role)
        for day, times in subclasses["times"].items():
            for time in times:
                if time in booked_time[day]:
                    return True
                booked_time[day][time] = True
    return False

def teacher_can_teach_class(teacher, class_, selected_role):
    if not teacher_know_subject(teacher, class_["subject"], selected_role):
        return False
    # it free at the time
    subclass = get_subclass(class_, selected_role)
    for day, times in subclass["times"].items():
        if not teacher_is_available_at_time(teacher, day, times):
            return False
    return True

def get_subclass(class_, role):
    return next(subclass for subclass in class_["subClasses"] if subclass["role"] == role)

def teacher_know_subject(teacher, subject, selected_role):
    subject_he_know_how_to_teach = teacher["subject_he_know_how_to_teach"]
    return any(filter(lambda x: x["subject"] == subject and selected_role in x["role"], subject_he_know_how_to_teach))

def teacher_is_available_at_time(teacher, day, times):
    return all(time in teacher["available_times"].get(day, []) for time in times)

if __name__ == "__main__":
    pass