from matching_algorithm import solve_timetable

teachers = {
    "teacher1": {
        "seniority": 1,
        "subject_he_know_how_to_teach": [
            {"subject": "Arq1", "role": ["Theory"]},
        ],
        "available_times": {
            "Monday": [9, 10, 11], 
        },
        "weekly_hours_max_work": 10,
        "groups": [{
            "my_role": ["Theory"],
            "subject": "Arq1",
            "other_teacher": [{"teacher": "teacher2", "role": ["Theory"]}]
        }]
    },
    "teacher2": {
        "seniority": 1,
        "subject_he_know_how_to_teach": [
            {"subject": "Arq1", "role": ["Theory"]},
        ],
        "available_times": {
            "Monday": [9, 10, 11], 
        },
        "weekly_hours_max_work": 10,
        "groups": [{
            "my_role": ["Theory"],
            "subject": "Arq1",
            "other_teacher": [{"teacher": "teacher1", "role": ["Theory"]}]
        }]
    },
    "teacher3": {
        "seniority": 8,
        "subject_he_know_how_to_teach": [
            {"subject": "Arq1", "role": ["Theory"]},
        ],
        "available_times": {
            "Monday": [9, 10, 11], 
        },
        "weekly_hours_max_work": 10
    }
}
classes = {
    "class1": {
        "subject": "Arq1",
        "subClasses": [
            {
                "role": "Theory",
                "times": {"Monday": [9, 10]},
                "num_teachers": 2
            },
        ]
    },
}

if __name__ == "__main__":
    result, unassigned, conflicts = solve_timetable(teachers, classes)
    print(result)
    assert result == {"class1": {'Theory': ['teacher1', 'teacher2']}}, result