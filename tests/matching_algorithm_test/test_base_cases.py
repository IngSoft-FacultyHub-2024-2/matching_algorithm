import sys
import unittest
from pathlib import Path
from typing import Optional

root_folder = Path(__file__, "../../..").resolve()
sys.path.append(str(root_folder))

from src.matching_algorithm import ConflictModel, solve_timetable
from src.matching_algorithm.models import PartiallyUnassignedConflict
from src.matching_algorithm.quality_assurance import are_conflicts
from tests.matching_algorithm_test.util import convert_teachers_and_classes_dict_to_model


class TestSolveTimetable(unittest.TestCase):
    def check_no_conflicts(
        self, conflicts: ConflictModel, except_conflict: Optional[list[str]] = None
    ) -> None:
        if except_conflict is None:
            except_conflict = []
        if "classes_without_teachers" not in except_conflict:
            self.assertEqual(conflicts.classes_without_teachers, [])
        if "teacher_without_any_classes" not in except_conflict:
            self.assertEqual(conflicts.teacher_without_any_classes, [])
        if "teacher_has_more_than_weekly_hours" not in except_conflict:
            self.assertEqual(conflicts.teacher_has_more_than_weekly_hours, [])
        if "partially_unassigned" not in except_conflict:
            self.assertEqual(conflicts.partially_unassigned, [])

    def test_no_teachers_no_classes(self) -> None:
        teachers_dict: dict = {}
        classes_dict: dict = {}
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(assignments.matches, {})
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)

    def test_one_teacher_one_class_match(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Math", "role": ["Theory", "Practice"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 10,
            }
        }
        classes_dict = {
            "class1": {
                "subject": "Math",
                "subClasses": [{"role": "Theory", "times": {"Monday": [9, 10]}, "num_teachers": 1}],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.matches, {"class1": {"Theory": ["teacher1"]}})
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)

    def test_one_teacher_one_class_match_only_one_role_of_two(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory", "Practice"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 10,
            }
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Theory", "times": {"Monday": [9, 10]}, "num_teachers": 1},
                    {"role": "Practice", "times": {"Friday": [9, 10]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.matches, {"class1": {"Theory": ["teacher1"], "Practice": []}})
        self.assertEqual(assignments.unassigned, [("class1", "Practice")])

    def test_one_teacher_one_class_match_only_one_role_of_two_need_2_teachers(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory", "Practice"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 10,
            }
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Theory", "times": {"Monday": [9, 10]}, "num_teachers": 1},
                    {"role": "Practice", "times": {"Friday": [9, 10]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.matches, {"class1": {"Theory": ["teacher1"], "Practice": []}})
        self.assertEqual(assignments.unassigned, [("class1", "Practice")])

    def test_one_teacher_one_class_two_days_match(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {"Monday": [9, 10, 11], "Friday": [9, 10, 11]},
                "weekly_hours_max_work": 10,
            }
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {
                        "role": "Theory",
                        "times": {"Monday": [9, 10], "Friday": [9, 10]},
                        "num_teachers": 1,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(assignments.matches, {"class1": {"Theory": ["teacher1"]}})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)

    def test_one_teacher_two_class_two_days_match(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
            }
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {
                        "role": "Theory",
                        "times": {"Monday": [9, 10], "Friday": [9, 10]},
                        "num_teachers": 1,
                    }
                ],
            },
            "class2": {
                "subject": "Arq1",
                "subClasses": [
                    {
                        "role": "Theory",
                        "times": {"Tuesday": [9, 10], "Friday": [11, 12]},
                        "num_teachers": 1,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(
            assignments.matches,
            {"class1": {"Theory": ["teacher1"]}, "class2": {"Theory": ["teacher1"]}},
        )
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)

    def test_constrains_a_subclass_can_be_assign_at_exactly_num_teachers_prefer_base_on_seniority(
        self,
    ) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
            },
            "teacher3": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {
                        "role": "Theory",
                        "times": {"Monday": [9, 10], "Friday": [9, 10]},
                        "num_teachers": 2,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(assignments.matches, {"class1": {"Theory": ["teacher1", "teacher2"]}})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher3"])
        self.check_no_conflicts(assignments.conflicts, ["teacher_without_any_classes"])

    def test_constrains_a_subclass_can_be_assign_at_exactly_num_teachers_prefer_base_on_seniority2(
        self,
    ) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
            },
            "teacher3": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {
                        "role": "Theory",
                        "times": {"Monday": [9, 10], "Friday": [9, 10]},
                        "num_teachers": 2,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(assignments.matches, {"class1": {"Theory": ["teacher2", "teacher3"]}})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher1"])
        self.check_no_conflicts(assignments.conflicts, ["teacher_without_any_classes"])

    def test_select_group_over_seniority_class_with_2_teachers(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Theory"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher2", "role": ["Theory"]}],
                    }
                ],
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
                "groups": [
                    {
                        "my_role": ["Theory"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher1", "role": ["Theory"]}],
                    }
                ],
            },
            "teacher3": {
                "seniority": 8,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Theory", "times": {"Monday": [9, 10]}, "num_teachers": 2},
                ],
            },
        }

        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(assignments.matches, {"class1": {"Theory": ["teacher1", "teacher2"]}})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher3"])
        self.check_no_conflicts(assignments.conflicts, ["teacher_without_any_classes"])

    def test_select_group_over_seniority(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Practice"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Practice"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher2", "role": ["Theory"]}],
                    }
                ],
            },
            "teacher2": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Theory"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher1", "role": ["Practice"]}],
                    }
                ],
            },
            "teacher3": {
                "seniority": 8,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory", "Practice"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Theory", "times": {"Monday": [9, 10]}, "num_teachers": 1},
                    {"role": "Practice", "times": {"Friday": [9, 10]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(
            assignments.matches, {"class1": {"Theory": ["teacher2"], "Practice": ["teacher1"]}}
        )
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher3"])
        self.check_no_conflicts(assignments.conflicts, ["teacher_without_any_classes"])

    def test_select_seniority_over_cannot_complete_group(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Practice"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Practice"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher2", "role": ["Theory"]}],
                    }
                ],
            },
            "teacher2": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Theory"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher1", "role": ["Practice"]}],
                    }
                ],
            },
            "teacher3": {
                "seniority": 8,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory", "Practice"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Theory", "times": {"Monday": [9, 10]}, "num_teachers": 1},
                    {"role": "Practice", "times": {"Friday": [9, 10]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(
            assignments.matches, {"class1": {"Theory": ["teacher2"], "Practice": ["teacher3"]}}
        )
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher1"])
        self.check_no_conflicts(assignments.conflicts, ["teacher_without_any_classes"])

    def test_constrains_teacher_can_be_assigned_at_most_once_to_each_subclass(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
            }
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {
                        "role": "Theory",
                        "times": {"Monday": [9, 10], "Friday": [9, 10]},
                        "num_teachers": 2,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(assignments.matches, {"class1": {"Theory": ["teacher1"]}})
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(
            assignments.conflicts.partially_unassigned,
            [PartiallyUnassignedConflict("class1", "Theory", 1, 2)],
        )
        self.check_no_conflicts(assignments.conflicts, ["partially_unassigned"])

    def test_two_teacher_two_class_two_days_match(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [{"subject": "Arq1", "role": ["Theory"]}],
                "available_times": {"Monday": [9, 10], "Tuesday": [9, 11], "Friday": [9, 10, 12]},
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [{"subject": "Agil1", "role": ["Theory"]}],
                "available_times": {
                    "Monday": [9, 10],
                    "Tuesday": [9, 10, 11],
                    "Friday": [9, 10, 12],
                },
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {
                        "role": "Theory",
                        "times": {"Monday": [9, 10], "Friday": [9]},
                        "num_teachers": 1,
                    }
                ],
            },
            "class2": {
                "subject": "Arq1",
                "subClasses": [
                    {
                        "role": "Theory",
                        "times": {"Monday": [9, 10], "Friday": [9]},
                        "num_teachers": 1,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(
            assignments.matches, {"class1": {"Theory": []}, "class2": {"Theory": ["teacher1"]}}
        )
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [("class1", "Theory")])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher2"])

    def test_one_teacher_one_class_no_match_because_subject(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [{"subject": "Arq1", "role": ["Theory"]}],
                "available_times": {"Monday": [8, 9, 10]},
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Math",
                "subClasses": [{"role": "Theory", "times": {"Monday": [9]}, "num_teachers": 1}],
            }
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(assignments.matches, {"class1": {"Theory": []}})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [("class1", "Theory")])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher1"])

    def test_multiple_teachers_classes(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [{"subject": "Arq1", "role": ["Theory"]}],
                "available_times": {"Monday": [9, 10], "Tuesday": [9, 10]},
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "DA2", "role": ["Theory"]},
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {"Monday": [9, 10], "Tuesday": [9, 10]},
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [{"role": "Theory", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
            "class2": {
                "subject": "DA2",
                "subClasses": [{"role": "Theory", "times": {"Monday": [10]}, "num_teachers": 1}],
            },
            "class3": {
                "subject": "DA2",
                "subClasses": [{"role": "Theory", "times": {"Tuesday": [9]}, "num_teachers": 1}],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertIn(assignments.matches["class1"]["Theory"][0], ["teacher1", "teacher2"])
        self.assertEqual(assignments.matches["class2"], {"Theory": ["teacher2"]})
        self.assertIn(assignments.matches["class3"]["Theory"][0], ["teacher1", "teacher2"])
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)

    def test_multiple_teachers_classes_2(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                    {"subject": "Agil1", "role": ["Theory"]},
                ],
                "available_times": {"Monday": [9]},
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {"Monday": [9]},
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [{"role": "Theory", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
            "class2": {
                "subject": "Agil1",
                "subClasses": [{"role": "Theory", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
            "class3": {
                "subject": "Agil1",
                "subClasses": [{"role": "Theory", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(assignments.matches["class1"]["Theory"], ["teacher2"])
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        # 2 possibilities: class2: {"Theory": ["teacher1"]} or class3: {"Theory": ["teacher1"]}
        if assignments.matches["class2"]["Theory"] == ["teacher1"]:
            self.assertEqual(assignments.unassigned, [("class3", "Theory")])
        else:
            self.assertEqual(assignments.unassigned, [("class2", "Theory")])
            self.assertEqual(assignments.matches["class3"]["Theory"], ["teacher1"])

    def test_multiple_teachers_max_hours(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                    {"subject": "Agil1", "role": ["Theory"]},
                ],
                "available_times": {"Monday": [8, 9, 10], "Tuesday": [9, 10], "Wednesday": [9, 10]},
                "weekly_hours_max_work": 5,
            },
            "teacher2": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 5,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [{"role": "Theory", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
            "class2": {
                "subject": "Agil1",
                "subClasses": [
                    {"role": "Theory", "times": {"Monday": [8, 9, 10]}, "num_teachers": 1}
                ],
            },
            "class3": {
                "subject": "Agil1",
                "subClasses": [
                    {"role": "Theory", "times": {"Tuesday": [9, 10]}, "num_teachers": 1}
                ],
            },
            "class4": {
                "subject": "Agil1",
                "subClasses": [
                    {"role": "Theory", "times": {"Wednesday": [9, 10]}, "num_teachers": 1}
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(assignments.matches["class1"], {"Theory": ["teacher2"]})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(len(assignments.unassigned), 1)
        self.assertIn(
            assignments.unassigned[0],
            [("class2", "Theory"), ("class3", "Theory"), ("class4", "Theory")],
        )

    def test_select_group_of_2_over_seniority_on_subject_of_3(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Practice"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Practice"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher2", "role": ["Practice"]}],
                    },
                    {
                        "my_role": ["Practice"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher3", "role": ["Theory"]}],
                    },
                ],
            },
            "teacher2": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Practice"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Practice"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher1", "role": ["Practice"]}],
                    },
                    {
                        "my_role": ["Practice"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher3", "role": ["Theory"]}],
                    },
                ],
            },
            "teacher3": {
                "seniority": 8,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Theory", "Practice"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
            },
            "teacher4": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [{"subject": "Arq1", "role": ["Theory"]}],
                "available_times": {"Monday": [9, 10, 11], "Tuesday": [9, 10, 11]},
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Practice", "times": {"Monday": [9, 10, 11]}, "num_teachers": 2},
                    {"role": "Theory", "times": {"Tuesday": [9, 10, 11]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        assignments = solve_timetable(teachers, classes)
        self.assertEqual(
            assignments.matches,
            {"class1": {"Practice": ["teacher1", "teacher2"], "Theory": ["teacher4"]}},
        )
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher3"])
        self.check_no_conflicts(assignments.conflicts, ["teacher_without_any_classes"])


if __name__ == "__main__":
    unittest.main()
