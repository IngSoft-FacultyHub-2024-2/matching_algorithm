
def diagnose_infeasibility(teachers, classes):
    issues = []
    
    # Check if there are enough teachers for each subject
    for class_name, class_info in classes.items():
        for subclass in class_info['subClasses']:
            required_teachers = subclass['num_teachers']
            available_teachers = sum(
                1 for teacher, info in teachers.items()
                if any(subject['subject'] == class_info['subject'] and 
                       subclass['role'] in subject['role']
                       for subject in info['subject_he_know_how_to_teach'])
            )
            if available_teachers < required_teachers:
                issues.append(f"Not enough teachers for {class_name} {subclass['role']}. "
                             f"Need {required_teachers}, have {available_teachers}")

    # Check if class times match teacher availability
    for class_name, class_info in classes.items():
        for subclass in class_info['subClasses']:
            teachers_available = False
            for teacher, info in teachers.items():
                can_teach = any(subject['subject'] == class_info['subject'] and 
                               subclass['role'] in subject['role']
                               for subject in info['subject_he_know_how_to_teach'])
                if can_teach:
                    is_available = all(
                        all(time in info['available_times'].get(day, [])
                            for time in times)
                        for day, times in subclass['times'].items()
                    )
                    if is_available:
                        teachers_available = True
                        break
            if not teachers_available:
                issues.append(f"No available teachers found for {class_name} {subclass['role']} "
                             f"at specified times")

    return issues