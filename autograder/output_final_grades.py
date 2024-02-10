#!/usr/bin/env python
# coding: utf-8
"""
https://gradescope-autograders.readthedocs.io/en/latest/troubleshooting/
"""

import numpy as np
import pandas as pd
import json


sid_json = json.load(open("/autograder/submission/SID.json", "r"))
sid = int(sid_json["SID"])
grades = pd.read_csv("/autograder/source/grades.csv", index_col="SID").loc[sid]


# grades.loc['Rubric1'] = .4*grades['Homework Total'] + .1*grades['Lab Total'] + .1 * grades['Discussion Total'] + .16*grades['Midterm'] + .24*grades['Final']
# grades.loc['Rubric2'] = .4*grades['Homework Total'] + .1*grades['Lab Total'] + 0 * grades['Discussion Total'] + .2*grades['Midterm'] + .3*grades['Final']
# grades.loc['Overall'] = np.max(grades.loc[['Rubric1', 'Rubric2']])


gs_output = {"tests": []}

def output_readme(grades, gs_output):
    outputs = []
    outputs.append(
        "Congratulations on completing Data 101 🥳🎉! Your final score report is available below."
    )
    outputs.append(
        "Scores include Lecture Attendance (Lectures 2 - 28), Multivitamins (1 - 5), Projects (1 - 4), and the Final Exam."
    )
    outputs.append(
        "The scores are out of 100 points."
    )
    gs_output["tests"].append(
        {"name": "README", "score": 0, "max_score": 0, "output": "\n".join(outputs)}
    )


def output_slip_days(grades, gs_output):
    outputs = []
    outputs.append(
        "Notes about Slip Days:"
    )
    outputs.append(
        "Your slip days have been allocated in a way that most benefits your grades."
    )
    outputs.append(
        "Unless you received an extension or accommodation, which might affect the number of slip days you have, everyone starts with 9 slip days across all projects and multivitamins."
    )
    outputs.append(
        "If you received an extension or accommodation, the report will reflect the applied slip days and any grade deductions, if applicable. You should verify the slip days and/or deductions corrspond with the records in our previous email communications."
    )
    outputs.append(
        f"Based on our records, you submitted assignments late by a total of {int(grades.loc['Total Lateness'])} days."
    )
    outputs.append(
        f"After applying slip days to late assignments, you currently have {int(grades.loc['Total Slip Days Remaining'])} slip days remaining."
    )
    gs_output["tests"].append(
        {"name": "README - Slip Days", "score": 0, "max_score": 0, "output": "\n".join(outputs)}
    )


# Final MV Grades
def output_multivitamin_grades(grades, gs_output):
    multivitamins = [f"Multivitamin {i}" for i in range(1, 6)]
    multivitamin_outputs = []
    for mv in multivitamins:
        if grades.loc[mv + ' Notes'] == 'N':
            multivitamin_outputs.append(
                f"Your {mv} score is {grades.loc[mv + ' Score']}. You submitted {int(grades.loc[mv + ' Lateness'])} days late. {int(grades.loc[mv + ' Auto-Allocated Slip Days'])} slip days were automatically applied."
            )
            if grades.loc[mv + ' Late Penalty'] > 0:
                multivitamin_outputs.append(
                f"    Because you have used up slip days, you received a {int(grades.loc[mv + ' Late Penalty'])}% deduction in your {mv} grade."
            )
        else:
            multivitamin_outputs.append(
                f"Your {mv} score is {grades.loc[mv + ' Score']}. You submitted {int(grades.loc[mv + ' Lateness'])} days late. You traded in {int(grades.loc[mv + ' Traded-in Slip Days'])} slip days and used an additional {int(grades.loc[mv + ' Auto-Allocated Slip Days'])}. You received a {int(grades.loc[mv + ' Late Penalty'])}% deduction in your {mv} grade."
        )
            multivitamin_outputs.append(
                f"    Here are the notes we have on file: {grades.loc[mv + ' Notes']}"
        )
    multivitamin_outputs = np.append(
        multivitamin_outputs,
        [
            f"Your overall final multivitamin score is {grades.loc['Final Multivitamin Score']}."
        ],
    )
    gs_output["tests"].append(
        {
            "name": "Multivitamins",
            "score": round(grades.loc['Final Multivitamin Score'], 6),
            "max_score": 25,
            "output": "\n".join(multivitamin_outputs),
        }
    )


def output_project_grades(grades, gs_output):
    projects = [f"Project {i}" for i in range(1, 5)]
    project_outputs = []
    for project in projects:
        if grades.loc[project + ' Notes'] == 'N':
            project_outputs.append(
                f"Your {project} score is {grades.loc[project + ' Score']}. You submitted {int(grades.loc[project + ' Lateness'])} days late. {int(grades.loc[project + ' Auto-Allocated Slip Days'])} slip days were automatically applied."
            )
            if grades.loc[project + ' Late Penalty'] > 0:
                project_outputs.append(
                f"    Because you have used up slip days, you received a {int(grades.loc[project + ' Late Penalty'])}% deduction in your {project} grade."
            )
        else:
            project_outputs.append(
                f"Your {project} score is {grades.loc[project + ' Score']}. You submitted {int(grades.loc[project + ' Lateness'])} days late. You traded in {int(grades.loc[project + ' Traded-in Slip Days'])} slip days and used an additional {int(grades.loc[project + ' Auto-Allocated Slip Days'])}. You received a {int(grades.loc[project + ' Late Penalty'])}% deduction in your {project} grade."
        )
            project_outputs.append(
                f"    Here are the notes we have on file: {grades.loc[project + ' Notes']}"
        )
    project_outputs = np.append(
        project_outputs,
        [f"Your overall final project score is {grades.loc['Final Project Score']}."],
    )
    gs_output["tests"].append(
        {
            "name": "Projects",
            "score": round(grades.loc['Final Project Score'], 6),
            "max_score": 52,
            "output": "\n".join(project_outputs),
        }
    )


def output_lecture_attendance_grades(grades, gs_output):
    lecture_outputs = []
    lecture_outputs = np.append(
        lecture_outputs,
        [
            f"Your overall lecture attendance score is {grades.loc['Lecture Attendance Score']}."
        ],
    )
    gs_output["tests"].append(
        {
            "name": "Lecture Attendance",
            "score": round(grades.loc['Lecture Attendance Score'], 6),
            "max_score": 8,
            "output": "\n".join(lecture_outputs),
        }
    )

def output_final_exam_grades(grades, gs_output):
    exam_outputs = []
    exam_outputs = np.append(
        exam_outputs,
        [
            f"Your final exam score is {grades.loc['Final Exam Score']}."
        ],
    )
    gs_output["tests"].append(
        {
            "name": "Final Exam",
            "score": round(grades.loc['Final Exam Score'], 6),
            "max_score": 15,
            "output": "\n".join(exam_outputs),
        }
    )


def output_final_total_score(grades, gs_output):
    outputs = [f"Your total score is {grades.loc['Final Total Score']}, out of 100 points."]
    # score = grades.loc["final Total Score"]
    gs_output["tests"].append(
        {
            "name": "Final Total Score",
            "score": 0,
            "max_score": 0,
            "output": "\n".join(outputs),
        }
    )

    # for staff use when viewing on Gradescope
    print(grades)
    print(gs_output)

output_readme(grades, gs_output)
output_slip_days(grades, gs_output)
output_multivitamin_grades(grades, gs_output)
output_project_grades(grades, gs_output)
output_lecture_attendance_grades(grades, gs_output)
output_final_exam_grades(grades, gs_output)
output_final_total_score(grades, gs_output)

out_path = "/autograder/results/results.json"
with open(out_path, "w") as f:
    f.write(json.dumps(gs_output))
