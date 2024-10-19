import random
import time 
import sys
from pathlib import Path
import json 

root_folder = Path(__file__, "../../..").resolve()
sys.path.append(str(root_folder))

from src.matching_algorithm.matching_algorithm import solve_timetable
from src.matching_algorithm.quality_assurance import are_conflicts
from src.matching_algorithm.quality_assurance import diagnose_infeasibility
from src.matching_algorithm.quality_assurance import check_solution
from tests.matching_algorithm_test.util import convert_teachers_and_classes_dict_to_model

subjects = [
    {"subject": "Arq1", "role": ["Theory", "Practice"]},
    {"subject": "Arq2", "role": ["Theory", "Practice"]},
    {"subject": "Agil1", "role": ["Theory"]},
    {"subject": "Agil2", "role": ["Theory"]},
    {"subject": "IngSoft1", "role": ["Theory"]},
    {"subject": "Da1", "role": ["Theory", "Practice"]},
    {"subject": "Da2", "role": ["Theory", "Practice"]},
    {"subject": "Algorithms", "role": ["Theory", "Practice"]},
    {"subject": "Algorithms2", "role": ["Theory", "Practice"]},
    {"subject": "RandomSubject", "role": ["Theory"]}
]

class TeachersGenerator():
    # Randomly select available times between 8-12 or 17-23 for each day
    def generate_available_times(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        hours = list(range(8, 12)) + list(range(17, 24))
        available_times = {}
        for day in days:
            if random.choice([True, True, False]):  # Teacher may or may not be available on this day
                available_times[day] = sorted(random.sample(hours, random.randint(1, 6)))
        return available_times

    def create_symmetric_groups(self, teachers, teacher_name, other_teacher_name):
        if not teachers[teacher_name].get("groups"):
            teachers[teacher_name]["groups"] = []
        
        if not teachers[other_teacher_name].get("groups"):
            teachers[other_teacher_name]["groups"] = []
        
        # Choose random subject and role for both teachers
        subject_knowledge = teachers[teacher_name]["subject_he_know_how_to_teach"]
        subject_role = random.choice(subject_knowledge)

        # Create group entry for both teachers
        teachers[teacher_name]["groups"].append({
            "my_role": subject_role["role"],
            "subject": subject_role["subject"],
            "other_teacher": [{"teacher": other_teacher_name, "role": subject_role["role"]}]
        })

        teachers[other_teacher_name]["groups"].append({
            "my_role": subject_role["role"],
            "subject": subject_role["subject"],
            "other_teacher": [{"teacher": teacher_name, "role": subject_role["role"]}]
        })

    # Generate teachers
    def create_teachers(self, num_teachers):
        teachers = {}
        
        for i in range(1, num_teachers + 1):
            teacher_name = f"teacher{i}"
            seniority = random.randint(1, 10)
            amount_of_subject_he_know = random.randint(1, len(subjects))
            subject_knowledge = random.sample(subjects, amount_of_subject_he_know)
            weekly_hours_max_work = random.randint(10, 40)
            available_times = self.generate_available_times()

            teachers[teacher_name] = {
                "seniority": seniority,
                "subject_he_know_how_to_teach": subject_knowledge,
                "available_times": available_times,
                "weekly_hours_max_work": weekly_hours_max_work,
                "groups": []  # Initialize empty groups
            }

        # Create symmetric groups for teachers
        for i in range(1, num_teachers):
            teacher_name = f"teacher{i}"
            other_teacher_name = f"teacher{random.randint(i+1, num_teachers)}"
            self.create_symmetric_groups(teachers, teacher_name, other_teacher_name)

        return teachers

class ClassesGenerator():
    # Function to generate continuous times for a sub-class with up to 3 hours per day
    def generate_continuous_times(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        selected_days = random.sample(days, random.randint(1, 2))  # Choose 1 or 2 days
        
        times = {}
        for day in selected_days:
            # Generate a continuous block of up to 3 hours
            if random.choice([True, False]):  # Randomly choose morning or evening
                # Morning: start between 8 and 9 (to fit within 3 hours)
                start_hour = random.choice(range(8, 10))  # Start at 8 or 9
                duration = random.randint(1, min(3, 12 - start_hour))  # Ensure max 3 hours, fits before noon
            else:
                # Evening: start between 17 and 20 (to fit within 3 hours)
                start_hour = random.choice(range(17, 21))  # Start between 17 and 20
                duration = random.randint(1, min(3, 24 - start_hour))  # Ensure max 3 hours, fits before 24

            times[day] = list(range(start_hour, start_hour + duration))
        
        return times

    # Generate sub-classes for a given subject with continuous hours and the 3-hour per day limit
    def generate_sub_classes(self, subject_roles):
        sub_classes = []
        total_hours_used = {}  # To track the number of hours used on each day
        
        for role in subject_roles:
            class_times = self.generate_continuous_times()
            
            # Ensure total hours per day across sub-classes do not exceed 3
            for day, hours in class_times.items():
                total_hours_used[day] = total_hours_used.get(day, 0) + len(hours)
                if total_hours_used[day] > 3:
                    # Adjust the hours to ensure the total doesn't exceed 3
                    class_times[day] = class_times[day][:3 - (total_hours_used[day] - len(hours))]

            sub_class = {
                "role": role,
                "times": {day: hours for day, hours in class_times.items() if hours},  # Only keep non-empty days
                "num_teachers": random.choice([1, 1, 1, 2])  # Randomly choose 1 or 2 teachers
            }
            sub_classes.append(sub_class)
        
        return sub_classes

    # Generate classes
    def create_classes(self, num_classes):
        classes = {}
        
        for i in range(1, num_classes + 1):
            class_name = f"class{i}"
            
            # Randomly select a subject
            subject_info = random.choice(subjects)
            
            # Create sub-classes for the selected subject, ensuring the constraints
            sub_classes = self.generate_sub_classes(subject_info["role"])

            classes[class_name] = {
                "subject": subject_info["subject"],
                "subClasses": sub_classes
            }

        return classes
    


if __name__ == "__main__":
    # Create 60 teachers
    teachers_generator = TeachersGenerator()
    teachers = teachers_generator.create_teachers(60)

    classes_generator = ClassesGenerator()
    classes = classes_generator.create_classes(40)

    # # Print sample output
    # pprint.pprint(teachers)
    # pprint.pprint(classes)

    # Now, let's solve the timetable
    start_time = time.time()
    teachers, classes = convert_teachers_and_classes_dict_to_model(teachers, classes)
    assignments = solve_timetable(teachers, classes)
    algorithm_duration = time.time() - start_time
    print(f"Results:")
    print(assignments.matches)
    print(f"Conflicts:")
    print(assignments.conflicts)
    print("unassigned: ", assignments.unassigned)
    print(f"Algorithm duration: {algorithm_duration} seconds")
    assert not are_conflicts(assignments.matches, teachers, classes), "Error, there are conflicts in the timetable"
    issues = diagnose_infeasibility(teachers, classes)
    for issue in issues:
        print(f"- {issue}")

    check_solution(teachers, classes, assignments)   

    results_path = root_folder / "json_input_tests"
    results_path.mkdir(exist_ok=True)
    json.dump({name: teacher.dict() for name, teacher in teachers.items()}, open(results_path.joinpath("teachers.json"), "w"), indent=4)
    json.dump({name: class_.dict() for name, class_ in classes.items()}, open(results_path.joinpath("classes.json"), "w"), indent=4)
