import time

import tasks


def main():
    print("\n=====================================================")
    print("Github Analytics Data Retriever")
    print("=====================================================")
    print("\nWelcome! What do you want to do?\n")

    for idx, task in enumerate(tasks.TASKS):
        print(f"\t{idx + 1} - {task[0]}")

    task = int(input("\nPlease enter the number of the task you want to execute: "))

    if task < 1 or task > len(tasks.TASKS):
        print("Invalid task number")
        return

    print(f"\nExecuting task \#{task} - {tasks.TASKS[task - 1][0]} ...\n")
    time.sleep(1)
    start_time = time.time()
    tasks.TASKS[task - 1][1]()
    print(
        f"\nFinished {tasks.TASKS[task - 1][0]} in {time.time() - start_time} seconds"
    )

    print("\n=====================================================")
    print("Thank you for using Github Analytics Data Retriever!")
    print("=====================================================")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    main()
