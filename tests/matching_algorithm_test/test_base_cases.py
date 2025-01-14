import sys
import unittest
from pathlib import Path
from typing import Optional

root_folder = Path(__file__, "../../..").resolve()
sys.path.append(str(root_folder))

from src.matching_algorithm import ConflictModel, Module, solve_timetable
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

    def get_modules(self) -> list[Module]:
        return [Module(id=i, time=f"{i}:00 - {i+1}:00", turn="test") for i in range(24)]

    def test_no_teachers_no_classes(self) -> None:
        teachers_dict: dict = {}
        classes_dict: dict = {}
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(assignments.matches, {})
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)

    def test_one_teacher_one_class_match(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Math", "role": ["Teórico", "Tecnología"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 10,
            }
        }
        classes_dict = {
            "class1": {
                "subject": "Math",
                "subClasses": [
                    {"role": "Teórico", "times": {"Monday": [9, 10]}, "num_teachers": 1}
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.matches, {"class1": {"Teórico": ["teacher1"]}})
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)

    def test_one_teacher_one_class_match_only_one_role_of_two(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico", "Tecnología"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 10,
            }
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Teórico", "times": {"Monday": [9, 10]}, "num_teachers": 1},
                    {"role": "Tecnología", "times": {"Friday": [9, 10]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(
            assignments.matches, {"class1": {"Teórico": ["teacher1"], "Tecnología": []}}
        )
        self.assertEqual(assignments.unassigned, [("class1", "Tecnología")])

    def test_one_teacher_one_class_match_only_one_role_of_two_need_2_teachers(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico", "Tecnología"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 10,
            }
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Teórico", "times": {"Monday": [9, 10]}, "num_teachers": 1},
                    {"role": "Tecnología", "times": {"Friday": [9, 10]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(
            assignments.matches, {"class1": {"Teórico": ["teacher1"], "Tecnología": []}}
        )
        self.assertEqual(assignments.unassigned, [("class1", "Tecnología")])

    def test_one_teacher_one_class_two_days_match(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
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
                        "role": "Teórico",
                        "times": {"Monday": [9, 10], "Friday": [9, 10]},
                        "num_teachers": 1,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(assignments.matches, {"class1": {"Teórico": ["teacher1"]}})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)

    def test_one_teacher_two_class_two_days_match(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
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
                        "role": "Teórico",
                        "times": {"Monday": [9, 10], "Friday": [9, 10]},
                        "num_teachers": 1,
                    }
                ],
            },
            "class2": {
                "subject": "Arq1",
                "subClasses": [
                    {
                        "role": "Teórico",
                        "times": {"Tuesday": [9, 10], "Friday": [11, 12]},
                        "num_teachers": 1,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(
            assignments.matches,
            {"class1": {"Teórico": ["teacher1"]}, "class2": {"Teórico": ["teacher1"]}},
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
                    {"subject": "Arq1", "role": ["Teórico"]},
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
                    {"subject": "Arq1", "role": ["Teórico"]},
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
                    {"subject": "Arq1", "role": ["Teórico"]},
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
                        "role": "Teórico",
                        "times": {"Monday": [9, 10], "Friday": [9, 10]},
                        "num_teachers": 2,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(assignments.matches, {"class1": {"Teórico": ["teacher1", "teacher2"]}})
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
                    {"subject": "Arq1", "role": ["Teórico"]},
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
                    {"subject": "Arq1", "role": ["Teórico"]},
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
                    {"subject": "Arq1", "role": ["Teórico"]},
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
                        "role": "Teórico",
                        "times": {"Monday": [9, 10], "Friday": [9, 10]},
                        "num_teachers": 2,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(assignments.matches, {"class1": {"Teórico": ["teacher2", "teacher3"]}})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher1"])
        self.check_no_conflicts(assignments.conflicts, ["teacher_without_any_classes"])

    def test_select_group_over_seniority_class_with_2_teachers(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Teórico"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher2", "role": ["Teórico"]}],
                    }
                ],
            },
            "teacher2": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Teórico"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher1", "role": ["Teórico"]}],
                    }
                ],
            },
            "teacher3": {
                "seniority": 8,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
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
                    {"role": "Teórico", "times": {"Monday": [9, 10]}, "num_teachers": 2},
                ],
            },
        }

        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(assignments.matches, {"class1": {"Teórico": ["teacher1", "teacher2"]}})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher3"])
        self.check_no_conflicts(assignments.conflicts, ["teacher_without_any_classes"])

    def test_select_group_over_seniority(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Tecnología"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Tecnología"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher2", "role": ["Teórico"]}],
                    }
                ],
            },
            "teacher2": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Teórico"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher1", "role": ["Tecnología"]}],
                    }
                ],
            },
            "teacher3": {
                "seniority": 8,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico", "Tecnología"]},
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
                    {"role": "Teórico", "times": {"Monday": [9, 10]}, "num_teachers": 1},
                    {"role": "Tecnología", "times": {"Friday": [9, 10]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(
            assignments.matches, {"class1": {"Teórico": ["teacher2"], "Tecnología": ["teacher1"]}}
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
                    {"subject": "Arq1", "role": ["Tecnología"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Tecnología"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher2", "role": ["Teórico"]}],
                    }
                ],
            },
            "teacher2": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                    "Tuesday": [9, 10],
                    "Friday": [9, 10, 11, 12],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Teórico"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher1", "role": ["Tecnología"]}],
                    }
                ],
            },
            "teacher3": {
                "seniority": 8,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico", "Tecnología"]},
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
                    {"role": "Teórico", "times": {"Monday": [9, 10]}, "num_teachers": 1},
                    {"role": "Tecnología", "times": {"Friday": [9, 10]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(
            assignments.matches, {"class1": {"Teórico": ["teacher2"], "Tecnología": ["teacher3"]}}
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
                    {"subject": "Arq1", "role": ["Teórico"]},
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
                        "role": "Teórico",
                        "times": {"Monday": [9, 10], "Friday": [9, 10]},
                        "num_teachers": 2,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(assignments.matches, {"class1": {"Teórico": ["teacher1"]}})
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(
            assignments.conflicts.partially_unassigned,
            [PartiallyUnassignedConflict("class1", "Teórico", 1, 2)],
        )
        self.check_no_conflicts(assignments.conflicts, ["partially_unassigned"])

    def test_two_teacher_two_class_two_days_match(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [{"subject": "Arq1", "role": ["Teórico"]}],
                "available_times": {"Monday": [9, 10], "Tuesday": [9, 11], "Friday": [9, 10, 12]},
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [{"subject": "Agil1", "role": ["Teórico"]}],
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
                        "role": "Teórico",
                        "times": {"Monday": [9, 10], "Friday": [9]},
                        "num_teachers": 1,
                    }
                ],
            },
            "class2": {
                "subject": "Arq1",
                "subClasses": [
                    {
                        "role": "Teórico",
                        "times": {"Monday": [9, 10], "Friday": [9]},
                        "num_teachers": 1,
                    }
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(
            assignments.matches, {"class1": {"Teórico": []}, "class2": {"Teórico": ["teacher1"]}}
        )
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [("class1", "Teórico")])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher2"])

    def test_one_teacher_one_class_no_match_because_subject(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [{"subject": "Arq1", "role": ["Teórico"]}],
                "available_times": {"Monday": [8, 9, 10]},
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Math",
                "subClasses": [{"role": "Teórico", "times": {"Monday": [9]}, "num_teachers": 1}],
            }
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(assignments.matches, {"class1": {"Teórico": []}})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [("class1", "Teórico")])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher1"])

    def test_multiple_teachers_classes(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [{"subject": "Arq1", "role": ["Teórico"]}],
                "available_times": {"Monday": [9, 10], "Tuesday": [9, 10]},
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "DA2", "role": ["Teórico"]},
                    {"subject": "Arq1", "role": ["Teórico"]},
                ],
                "available_times": {"Monday": [9, 10], "Tuesday": [9, 10]},
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [{"role": "Teórico", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
            "class2": {
                "subject": "DA2",
                "subClasses": [{"role": "Teórico", "times": {"Monday": [10]}, "num_teachers": 1}],
            },
            "class3": {
                "subject": "DA2",
                "subClasses": [{"role": "Teórico", "times": {"Tuesday": [9]}, "num_teachers": 1}],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertIn(assignments.matches["class1"]["Teórico"][0], ["teacher1", "teacher2"])
        self.assertEqual(assignments.matches["class2"], {"Teórico": ["teacher2"]})
        self.assertIn(assignments.matches["class3"]["Teórico"][0], ["teacher1", "teacher2"])
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)

    def test_multiple_teachers_classes_2(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
                    {"subject": "Agil1", "role": ["Teórico"]},
                ],
                "available_times": {"Monday": [9]},
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
                ],
                "available_times": {"Monday": [9]},
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [{"role": "Teórico", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
            "class2": {
                "subject": "Agil1",
                "subClasses": [{"role": "Teórico", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
            "class3": {
                "subject": "Agil1",
                "subClasses": [{"role": "Teórico", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(assignments.matches["class1"]["Teórico"], ["teacher2"])
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        # 2 possibilities: class2: {"Teórico": ["teacher1"]} or class3: {"Teórico": ["teacher1"]}
        if assignments.matches["class2"]["Teórico"] == ["teacher1"]:
            self.assertEqual(assignments.unassigned, [("class3", "Teórico")])
        else:
            self.assertEqual(assignments.unassigned, [("class2", "Teórico")])
            self.assertEqual(assignments.matches["class3"]["Teórico"], ["teacher1"])

    def test_multiple_teachers_max_hours(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
                    {"subject": "Agil1", "role": ["Teórico"]},
                ],
                "available_times": {"Monday": [8, 9, 10], "Tuesday": [9, 10], "Wednesday": [9, 10]},
                "weekly_hours_max_work": 5,
            },
            "teacher2": {
                "seniority": 3,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 5,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [{"role": "Teórico", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
            "class2": {
                "subject": "Agil1",
                "subClasses": [
                    {"role": "Teórico", "times": {"Monday": [8, 9, 10]}, "num_teachers": 1}
                ],
            },
            "class3": {
                "subject": "Agil1",
                "subClasses": [
                    {"role": "Teórico", "times": {"Tuesday": [9, 10]}, "num_teachers": 1}
                ],
            },
            "class4": {
                "subject": "Agil1",
                "subClasses": [
                    {"role": "Teórico", "times": {"Wednesday": [9, 10]}, "num_teachers": 1}
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(assignments.matches["class1"], {"Teórico": ["teacher2"]})
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(len(assignments.unassigned), 1)
        self.assertIn(
            assignments.unassigned[0],
            [("class2", "Teórico"), ("class3", "Teórico"), ("class4", "Teórico")],
        )

    def test_select_group_of_2_over_seniority_on_subject_of_3(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Tecnología"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Tecnología"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher2", "role": ["Tecnología"]}],
                    },
                    {
                        "my_role": ["Tecnología"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher3", "role": ["Teórico"]}],
                    },
                ],
            },
            "teacher2": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Tecnología"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
                "groups": [
                    {
                        "my_role": ["Tecnología"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher1", "role": ["Tecnología"]}],
                    },
                    {
                        "my_role": ["Tecnología"],
                        "subject": "Arq1",
                        "other_teacher": [{"teacher": "teacher3", "role": ["Teórico"]}],
                    },
                ],
            },
            "teacher3": {
                "seniority": 8,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico", "Tecnología"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
            },
            "teacher4": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [{"subject": "Arq1", "role": ["Teórico"]}],
                "available_times": {"Monday": [9, 10, 11], "Tuesday": [9, 10, 11]},
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Tecnología", "times": {"Monday": [9, 10, 11]}, "num_teachers": 2},
                    {"role": "Teórico", "times": {"Tuesday": [9, 10, 11]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules)
        self.assertEqual(
            assignments.matches,
            {"class1": {"Tecnología": ["teacher1", "teacher2"], "Teórico": ["teacher4"]}},
        )
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher3"])
        self.check_no_conflicts(assignments.conflicts, ["teacher_without_any_classes"])

    def test_teacher_with_class_already_assigned(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 8,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Tecnología"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Tecnología"]},
                ],
                "available_times": {
                    "Monday": [9, 10, 11],
                },
                "weekly_hours_max_work": 10,
            },
            "teacher3": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Tecnología"]},
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
                    {"role": "Tecnología", "times": {"Monday": [9, 10, 11]}, "num_teachers": 2},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        teacher_names_with_classes = ["teacher1"]
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules, teacher_names_with_classes)
        self.assertEqual(
            assignments.matches,
            {"class1": {"Tecnología": ["teacher2", "teacher3"]}},
        )
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)

    def test_teacher_same_class_at_same_time(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 8,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico"]},
                ],
                "available_times": {
                    "Monday": [5],
                },
                "weekly_hours_max_work": 80,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Teórico", "times": {"Monday": [5]}, "num_teachers": 1},
                ],
            },
            "class2": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Teórico", "times": {"Monday": [5]}, "num_teachers": 1},
                ],
            },
        }
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules, [])
        self.assertEqual(
            assignments.matches,
            {"class1": {"Teórico": []}, "class2": {"Teórico": ["teacher1"]}},
        )
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.unassigned, [("class1", "Teórico")])
        self.check_no_conflicts(assignments.conflicts, ["classes_without_teachers"])

    def test_pre_assignments_teachers(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico", "Tecnología"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico", "Tecnología"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Teórico", "times": {"Monday": [9, 10]}, "num_teachers": 1}
                ],
            },
        }
        pre_assignments = {"class1": {"Teórico": ["teacher2"]}}
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules, pre_assignments=pre_assignments)
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.matches, {"class1": {"Teórico": ["teacher2"]}})
        self.assertEqual(assignments.unassigned, [])
        self.assertEqual(assignments.conflicts.teacher_without_any_classes, ["teacher1"])
        self.check_no_conflicts(assignments.conflicts, ["teacher_without_any_classes"])

    def test_pre_assignments_teachers_add_one_more_teacher(self) -> None:
        teachers_dict = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico", "Tecnología"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 10,
            },
            "teacher2": {
                "seniority": 1,
                "subject_he_know_how_to_teach": [
                    {"subject": "Arq1", "role": ["Teórico", "Tecnología"]},
                ],
                "available_times": {"Monday": [9, 10]},
                "weekly_hours_max_work": 10,
            },
        }
        classes_dict = {
            "class1": {
                "subject": "Arq1",
                "subClasses": [
                    {"role": "Teórico", "times": {"Monday": [9, 10]}, "num_teachers": 2}
                ],
            },
        }
        pre_assignments = {"class1": {"Teórico": ["teacher1"]}}
        teachers, classes = convert_teachers_and_classes_dict_to_model(teachers_dict, classes_dict)
        modules = self.get_modules()
        assignments = solve_timetable(teachers, classes, modules, pre_assignments=pre_assignments)
        self.assertFalse(are_conflicts(assignments.matches, teachers, classes))
        self.assertEqual(assignments.matches, {"class1": {"Teórico": ["teacher1", "teacher2"]}})
        self.assertEqual(assignments.unassigned, [])
        self.check_no_conflicts(assignments.conflicts)


if __name__ == "__main__":
    unittest.main()
