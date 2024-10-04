def validate_unassigned_classes(teachers, classes, result, unassigned):
    validation_issues = []
    
    for class_name, role in unassigned:
        class_info = classes[class_name]
        subclass = next(s for s in class_info['subClasses'] if s['role'] == role)
        
        # Find potential teachers for this class
        potential_teachers = []
        for teacher, teacher_info in teachers.items():
            # Check if teacher can teach this subject and role
            can_teach = any(
                subject['subject'] == class_info['subject'] and 
                subclass['role'] in subject['role']
                for subject in teacher_info['subject_he_know_how_to_teach']
            )
            
            if not can_teach:
                continue
                
            # Check time availability
            is_available = True
            for day, times in subclass['times'].items():
                for time in times:
                    if time not in teacher_info['available_times'].get(day, []):
                        is_available = False
                        break
                if not is_available:
                    break
            
            if not is_available:
                continue
                
            # Check if teacher hasn't exceeded weekly hours
            current_hours = sum(
                len(sub['times'].get(day, []))
                for c_name, c_assignments in result.items()
                for r, assigned_teachers in c_assignments.items()
                for sub in classes[c_name]['subClasses'] if sub['role'] == r
                for day in sub['times']
                if teacher in assigned_teachers
            )
            
            class_hours = sum(len(times) for times in subclass['times'].values())
            if current_hours + class_hours <= teacher_info['weekly_hours_max_work']:
                # Check for time conflicts with already assigned classes
                has_conflict = False
                for day, times in subclass['times'].items():
                    for time in times:
                        for c_name, c_assignments in result.items():
                            for r, assigned_teachers in c_assignments.items():
                                if teacher in assigned_teachers:
                                    conflict_subclass = next(s for s in classes[c_name]['subClasses'] if s['role'] == r)
                                    if day in conflict_subclass['times'] and time in conflict_subclass['times'][day]:
                                        has_conflict = True
                                        break
                            if has_conflict:
                                break
                    if has_conflict:
                        break
                
                if not has_conflict:
                    potential_teachers.append({
                        'teacher': teacher,
                        'current_hours': current_hours,
                        'available_hours': teacher_info['weekly_hours_max_work'] - current_hours
                    })
        
        if potential_teachers:
            validation_issues.append({
                'class_name': class_name,
                'role': role,
                'subject': class_info['subject'],
                'potential_teachers': potential_teachers
            })
    
    return validation_issues

# Example usage function
def check_solution(teachers, classes, result, unassigned):
    if unassigned:
        print(f"Found {len(unassigned)} unassigned classes. Validating...")
        validation_issues = validate_unassigned_classes(teachers, classes, result, unassigned)
        
        if validation_issues:
            print("\nPotential issues found:")
            for issue in validation_issues:
                print(f"\nClass: {issue['class_name']}, Role: {issue['role']}, Subject: {issue['subject']}")
                print("Could potentially be taught by:")
                for pt in issue['potential_teachers']:
                    print(f"  - {pt['teacher']}")
                    print(f"    Current hours: {pt['current_hours']}")
                    print(f"    Available hours: {pt['available_hours']}")
        else:
            print("No issues found. All unassigned classes appear to be correctly unassigned.")
    else:
        print("All classes were assigned successfully.")