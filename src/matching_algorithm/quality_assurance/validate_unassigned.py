from typing import Any, Optional

from ..models import TeacherModel, ClassModel, RoleModel, SubClassModel, Assignments, RoleType

def validate_unassigned_classes(
    teachers: dict[str, TeacherModel],
    classes: dict[str, ClassModel],
    assignments: Assignments
) -> list[dict[str, Any]]:
    validation_issues = []
    
    def can_teacher_take_class(
        teacher: str,
        teacher_info: TeacherModel,
        class_info: ClassModel,
        subclass: SubClassModel,
        current_assignments: dict[str, dict[RoleType, list[str]]]
    ) -> tuple[bool, Optional[str]]:
        # Check if teacher can teach this subject and role
        can_teach = any(
            subject.subject == class_info.subject and 
            subclass.role in subject.role
            for subject in teacher_info.subject_he_know_how_to_teach
        )
        if not can_teach:
            return False, "Cannot teach subject"
            
        # Check time availability
        subclass_times = subclass.times.dict(exclude_none=True)
        teacher_times = teacher_info.available_times.dict(exclude_none=True)
        
        for day, times in subclass_times.items():
            if times:  # Check if times is not None
                for time in times:
                    if time not in teacher_times.get(day, []):
                        return False, "Time conflict with availability"
                    
        # Check weekly hours
        current_hours = sum(
            len(sub.times.dict(exclude_none=True).get(day, []))
            for c_name, c_assignments in current_assignments.items()
            for r, assigned_teachers in c_assignments.items()
            for sub in classes[c_name].subClasses if sub.role == r
            for day in sub.times.dict(exclude_none=True)
            if teacher in assigned_teachers
        )
        
        class_hours = sum(
            len(times) for times in subclass_times.values() if times is not None
        )
        
        if current_hours + class_hours > teacher_info.weekly_hours_max_work:
            return False, "Exceeds weekly hours"
            
        # Check for time conflicts with already assigned classes
        for day, times in subclass_times.items():
            if times:  # Check if times is not None
                for time in times:
                    for c_name, c_assignments in current_assignments.items():
                        for r, assigned_teachers in c_assignments.items():
                            if teacher in assigned_teachers:
                                conflict_subclass = next(s for s in classes[c_name].subClasses if s.role == r)
                                conflict_times = conflict_subclass.times.dict(exclude_none=True)
                                if day in conflict_times and time in conflict_times[day]:
                                    return False, "Time conflict with other assignments"
                                
        return True, None

    # Check completely unassigned classes
    for class_name, role in assignments.unassigned:
        class_info = classes[class_name]
        subclass = next(s for s in class_info.subClasses if s.role == role)
        
        potential_teachers = []
        for teacher, teacher_info in teachers.items():
            can_teach, reason = can_teacher_take_class(teacher, teacher_info, class_info, subclass, assignments.matches)
            if can_teach:
                current_hours = sum(
                    len(sub.times.dict(exclude_none=True).get(day, []))
                    for c_name, c_assignments in assignments.matches.items()
                    for r, assigned_teachers in c_assignments.items()
                    for sub in classes[c_name].subClasses if sub.role == r
                    for day in sub.times.dict(exclude_none=True)
                    if teacher in assigned_teachers
                )
                potential_teachers.append({
                    'teacher': teacher,
                    'current_hours': current_hours,
                    'available_hours': teacher_info.weekly_hours_max_work - current_hours
                })
        
        if potential_teachers:
            validation_issues.append({
                'class_name': class_name,
                'role': role,
                'subject': class_info.subject,
                'type': 'completely_unassigned',
                'teachers_needed': subclass.num_teachers,
                'potential_teachers': potential_teachers
            })

    # Check partially unassigned classes
    for partial in assignments.conflicts.partially_unassigned:
        class_name = partial.class_name
        role = partial.role
        class_info = classes[class_name]
        subclass = next(s for s in class_info.subClasses if s.role == role)
        potential_teachers = []
        
        for teacher, teacher_info in teachers.items():
            if teacher in assignments.matches[class_name][role]:
                continue  # Skip already assigned teachers
                
            can_teach, reason = can_teacher_take_class(teacher, teacher_info, class_info, subclass, assignments.matches)
            if can_teach:
                current_hours = sum(
                    len(sub.times.dict(exclude_none=True).get(day, []))
                    for c_name, c_assignments in assignments.matches.items()
                    for r, assigned_teachers in c_assignments.items()
                    for sub in classes[c_name].subClasses if sub.role == r
                    for day in sub.times.dict(exclude_none=True)
                    if teacher in assigned_teachers
                )
                potential_teachers.append({
                    'teacher': teacher,
                    'current_hours': current_hours,
                    'available_hours': teacher_info.weekly_hours_max_work - current_hours
                })
        
        if potential_teachers:
            validation_issues.append({
                'class_name': class_name,
                'role': role,
                'subject': class_info.subject,
                'type': 'partially_unassigned',
                'teachers_assigned': partial.assigned,
                'teachers_needed': partial.needed,
                'potential_teachers': potential_teachers
            })

    return validation_issues

def check_solution(
    teachers: dict[str, TeacherModel],
    classes: dict[str, ClassModel],
    assignments: Assignments,
) -> None:
    validation_issues = validate_unassigned_classes(teachers, classes, assignments)
    
    if validation_issues:
        print("\nPotential issues found:")
        for issue in validation_issues:
            print(f"\nClass: {issue['class_name']}, Role: {issue['role']}, Subject: {issue['subject']}")
            if issue['type'] == 'partially_unassigned':
                print(f"Currently assigned: {issue['teachers_assigned']} of {issue['teachers_needed']} teachers")
            else:
                print(f"Completely unassigned. Needs {issue['teachers_needed']} teachers")
            print("Could potentially be taught by:")
            for pt in issue['potential_teachers']:
                print(f"  - {pt['teacher']}")
                print(f"    Current hours: {pt['current_hours']}")
                print(f"    Available hours: {pt['available_hours']}")
    else:
        if assignments.unassigned or assignments.conflicts.partially_unassigned:
            print("No issues found. All unassigned or partially assigned classes appear to be correctly handled.")
        else:
            print("No issues found. All classes were fully assigned successfully.")