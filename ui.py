import time
from typing import Tuple

import tasks


def welcome_message():
    print()
    print("=====================================================")
    print("Welcome to the Github Analytics Data Retriever!")
    print("=====================================================")
    print()
    print("What do you want to do?")
    print()

    for idx, task in enumerate(tasks.TASKS):
        print(f"\t{idx + 1} - {task[0]}")


def abort_message():
    print()
    print("Aborting...")


def finish_message(task_name: str, execution_end: float):
    print()
    print(f"Finished {task_name} in {execution_end:.2f} seconds")
    print()
    print("=====================================================")
    print("Thank you for using Github Analytics Data Retriever!")
    print("=====================================================")


def task_selector() -> Tuple[int, str]:
    print()

    task_id = int(input("Please enter the number of the task you want to execute: "))

    if task_id < 1 or task_id > len(tasks.TASKS):
        print("Invalid task number")
        return None, None

    return task_id, tasks.TASKS[task_id - 1][0]


def task_executor(task_id: int, task_name: str):
    print()
    print(f"\nExecuting task #{task_id} - {task_name} ...\n")
    print()

    time.sleep(1)

    execution_start = time.time()
    tasks.TASKS[task_id - 1][1]()
    execution_end = time.time() - execution_start

    finish_message(task_name, execution_end)


def select_and_execute_task():
    task_id, task_name = task_selector()

    if task_id is None:
        abort_message()
        return

    task_executor(task_id, task_name)
