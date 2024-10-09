from ortools.sat.python import cp_model

def solve_timetable(teachers, classes):
    model = cp_model.CpModel()

    # Create variables
    assignments = {}
    for teacher in teachers:
        for class_name, class_info in classes.items():
            for subclass in class_info['subClasses']:
                for i in range(subclass['num_teachers']):
                    assignments[(teacher, class_name, subclass['role'], i)] = model.NewBoolVar(f'{teacher}_{class_name}_{subclass["role"]}_{i}')

    # Create 'is_assigned' variables for each subclass
    is_assigned = {}
    partially_assigned = {}
    for class_name, class_info in classes.items():
        for subclass in class_info['subClasses']:
            if subclass['num_teachers'] > 1:
                # For multi-teacher classes, create variables for partial assignment
                for i in range(1, subclass['num_teachers'] + 1):
                    partially_assigned[(class_name, subclass['role'], i)] = model.NewBoolVar(
                        f'partially_assigned_{class_name}_{subclass["role"]}_{i}')
            
            # Keep the original is_assigned variable for fully assigned classes
            is_assigned[(class_name, subclass['role'])] = model.NewBoolVar(
                f'is_assigned_{class_name}_{subclass["role"]}')
            
    # Create 'has_any_class' variables for each teacher
    has_any_class = {}
    for teacher in teachers:
        has_any_class[teacher] = model.NewBoolVar(f'has_any_class_{teacher}')
        # A teacher has a class if they're assigned to any subclass
        teacher_assignments = []
        for class_name, class_info in classes.items():
            for subclass in class_info['subClasses']:
                for i in range(subclass['num_teachers']):
                    teacher_assignments.append(assignments[(teacher, class_name, subclass['role'], i)])
        model.Add(sum(teacher_assignments) >= 1).OnlyEnforceIf(has_any_class[teacher])
        model.Add(sum(teacher_assignments) == 0).OnlyEnforceIf(has_any_class[teacher].Not())

    # Constraints
    conflicts = {"teacher_without_any_classes": [], 
                 "teacher_has_more_than_weekly_hours": [], 
                 "classes_without_teachers": [],
                 "partially_unassigned": []}
    seniority_preference = model.NewIntVar(0, 1000000, 'seniority_preference')
    seniority_terms = []
    
    for class_name, class_info in classes.items():
        for subclass in class_info['subClasses']:
            num_teachers_needed = subclass['num_teachers']
            # A subclass is assigned if exactly num_teachers are assigned to it
            actual_teachers = sum(assignments[(teacher, class_name, subclass['role'], i)]
                                 for teacher in teachers
                                 for i in range(num_teachers_needed))
            
            # Constraint for full assignment
            model.Add(actual_teachers == num_teachers_needed).OnlyEnforceIf(
                is_assigned[(class_name, subclass['role'])])
            model.Add(actual_teachers < num_teachers_needed).OnlyEnforceIf(
                is_assigned[(class_name, subclass['role'])].Not())
            
            # Constraints for partial assignments if multiple teachers are needed
            if num_teachers_needed > 1:
                for i in range(1, num_teachers_needed + 1):
                    model.Add(actual_teachers >= i).OnlyEnforceIf(
                        partially_assigned[(class_name, subclass['role'], i)])
                    model.Add(actual_teachers < i).OnlyEnforceIf(
                        partially_assigned[(class_name, subclass['role'], i)].Not())
            
            # Each teacher can be assigned at most once to each subclass
            for teacher in teachers:
                model.Add(sum(assignments[(teacher, class_name, subclass['role'], i)]
                              for i in range(subclass['num_teachers'])) <= 1)
                
            assigned_teachers = []
            for teacher, teacher_info in teachers.items():
                can_teach_info = next((subject for subject in teacher_info['subject_he_know_how_to_teach']
                                      if subject['subject'] == class_info['subject'] and 
                                      subclass['role'] in subject['role']), None)
                
                if not can_teach_info:
                    for i in range(subclass['num_teachers']):
                        model.Add(assignments[(teacher, class_name, subclass['role'], i)] == 0)
                    continue

                # Teacher must be available at the class times
                is_available = True
                for day, times in subclass['times'].items():
                    for time in times:
                        if time not in teacher_info['available_times'].get(day, []):
                            for i in range(subclass['num_teachers']):
                                model.Add(assignments[(teacher, class_name, subclass['role'], i)] == 0)
                            is_available = False
                            break
                    if not is_available:
                        break

                if is_available:
                    assigned_teachers.append(teacher)
                    # Add seniority preference - now using teacher's overall seniority
                    for i in range(subclass['num_teachers']):
                        seniority_terms.append(assignments[(teacher, class_name, subclass['role'], i)] * 
                                              teacher_info['seniority'])

            if not assigned_teachers:
                conflicts["classes_without_teachers"].append({
                    "class_name": class_name, 
                    "role": subclass['role'], 
                    "subject": class_info['subject']
                    })

    # Add the sum of all seniority terms
    if seniority_terms:
        model.Add(seniority_preference == sum(seniority_terms))

    # A teacher can't teach multiple classes at the same time
    for teacher in teachers:
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            for time in range(24):  # Assuming 24-hour clock
                conflicting_subclasses = [
                    (class_name, subclass['role'], subclass['num_teachers'])
                    for class_name, class_info in classes.items()
                    for subclass in class_info['subClasses']
                    if day in subclass['times'] and time in subclass['times'][day]
                ]
                if conflicting_subclasses:
                    model.Add(sum(assignments[(teacher, class_name, role, i)] 
                                  for class_name, role, num_teachers in conflicting_subclasses
                                  for i in range(num_teachers)) <= 1)
                    
    # Weekly hours constraint
    for teacher, teacher_info in teachers.items():
        weekly_hours = sum(
            assignments[(teacher, class_name, subclass['role'], i)] * sum(len(times) for times in subclass['times'].values())
            for class_name, class_info in classes.items()
            for subclass in class_info['subClasses']
            for i in range(subclass['num_teachers'])
        )
        model.Add(weekly_hours <= teacher_info['weekly_hours_max_work'])
    
    # Group preference
    group_preference = model.NewIntVar(0, len(teachers) * len(classes) * 2, 'group_preference')
    group_matches = []

    for teacher, teacher_info in teachers.items():
        for group in teacher_info.get('groups', []):
            for class_name, class_info in classes.items():
                if class_info['subject'] == group['subject']:
                    # For each group configuration, create a new boolean variable
                    group_match = model.NewBoolVar(f'group_match_{teacher}_{class_name}')
                    
                    # Create variables for teacher assignment and other teachers' assignments
                    teacher_role_assignments = []
                    other_teacher_role_assignments = []
                    
                    # Check this teacher's assignments
                    for subclass in class_info['subClasses']:
                        if subclass['role'] in group['my_role']:
                            for i in range(subclass['num_teachers']):
                                teacher_role_assignments.append(
                                    assignments[(teacher, class_name, subclass['role'], i)])
                    
                    # Check other teachers' assignments
                    for other_teacher_info in group['other_teacher']:
                        other_teacher = other_teacher_info['teacher']
                        other_teacher_assignments = []
                        for subclass in class_info['subClasses']:
                            if subclass['role'] in other_teacher_info['role']:
                                for i in range(subclass['num_teachers']):
                                    other_teacher_assignments.append(
                                        assignments[(other_teacher, class_name, subclass['role'], i)])
                        if other_teacher_assignments:
                            other_teacher_role_assignments.append(model.NewBoolVar(f'other_{other_teacher}_{class_name}'))
                            model.Add(sum(other_teacher_assignments) >= 1).OnlyEnforceIf(
                                other_teacher_role_assignments[-1])
                            model.Add(sum(other_teacher_assignments) == 0).OnlyEnforceIf(
                                other_teacher_role_assignments[-1].Not())
                    
                    # Group match occurs when this teacher and at least one other teacher are assigned
                    if teacher_role_assignments and other_teacher_role_assignments:
                        teacher_assigned = model.NewBoolVar(f'teacher_{teacher}_assigned_{class_name}')
                        model.Add(sum(teacher_role_assignments) >= 1).OnlyEnforceIf(teacher_assigned)
                        model.Add(sum(teacher_role_assignments) == 0).OnlyEnforceIf(teacher_assigned.Not())
                        
                        # Group match is true if teacher is assigned and at least one other teacher is assigned
                        model.AddBoolAnd([teacher_assigned] + other_teacher_role_assignments).OnlyEnforceIf(group_match)
                        model.AddBoolOr([teacher_assigned.Not()] + 
                                       [x.Not() for x in other_teacher_role_assignments]).OnlyEnforceIf(group_match.Not())
                        
                        group_matches.append(group_match)

    if group_matches:
        model.Add(group_preference == sum(group_matches))
    else:
        model.Add(group_preference == 0)

    # Multi-objective optimization
    teacher_assignment_preference = sum(has_any_class.values())
    total_assigned = sum(is_assigned.values())
    partial_assignment_preference = sum(
        partially_assigned[(class_name, subclass['role'], i)] * i
        for class_name, class_info in classes.items()
        for subclass in class_info['subClasses']
        if subclass['num_teachers'] > 1
        for i in range(1, subclass['num_teachers'])
    )

    
    # Priorities: 
    # 1. Maximize total assigned classes (weight: 1000000)
    # 2. Maximize total assigned of partial classes (need 2 professors but only one is assigned) (weight: 100000)
    # 3. Try to give each teacher at least one class (weight: 10000)
    # 4. Maximize group preferences (weight: 10000)
    # 5. Maximize seniority preferences (weight: 1)   
    model.Maximize(total_assigned * 1000000 +
                   partial_assignment_preference * 100000 +
                   teacher_assignment_preference * 10000 +
                   group_preference * 100 +
                   seniority_preference)


    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Prepare the output
    result = {}
    if status == cp_model.INFEASIBLE:
        print("The problem is infeasible")
        # You can get some information about why it might be infeasible
        print(solver.ResponseStats())
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for class_name, class_info in classes.items():
            result[class_name] = {}
            for subclass in class_info['subClasses']:
                result[class_name][subclass['role']] = []
                assigned_teachers = []
                for teacher in teachers:
                    for i in range(subclass['num_teachers']):
                        if solver.Value(assignments[(teacher, class_name, subclass['role'], i)]):
                            assigned_teachers.append(teacher)
                
                result[class_name][subclass['role']] = assigned_teachers
                
                if len(assigned_teachers) < subclass['num_teachers'] and len(assigned_teachers) > 0:
                    conflicts["partially_unassigned"].append({
                        'class_name': class_name,
                        'role': subclass['role'],
                        'assigned': len(assigned_teachers),
                        'needed': subclass['num_teachers']
                    })

        # Check for unassigned subclasses
        unassigned = [(class_name, subclass['role']) 
                      for class_name, class_info in classes.items() 
                      for subclass in class_info['subClasses'] 
                      if not result[class_name][subclass['role']]]
        
        # Check for weekly hours conflicts
        for teacher, teacher_info in teachers.items():
            teacher_hours = sum(
                len(subclass['times'].get(day, []))
                for class_name, class_assignments in result.items()
                for role, assigned_teachers in class_assignments.items()
                for subclass in classes[class_name]['subClasses'] if subclass['role'] == role
                for day in subclass['times']
                if teacher in assigned_teachers
            )
            if teacher_hours > teacher_info['weekly_hours_max_work']:
                conflicts['teacher_has_more_than_weekly_hours'].append({"teacher": teacher, "assigned_hours": teacher_hours, "weekly_hours_max_work":teacher_info['weekly_hours_max_work']})

        # Add information about teachers without any classes
        teachers_without_classes = [teacher for teacher in teachers if not solver.Value(has_any_class[teacher])]
        if teachers_without_classes:
            conflicts['teacher_without_any_classes'] = teachers_without_classes
        
        return result, unassigned, conflicts
    else:
        return {}, [(class_name, subclass['role']) for class_name, class_info in classes.items() for subclass in class_info['subClasses']], conflicts