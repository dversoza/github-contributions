from dotenv import load_dotenv

load_dotenv()


def main():
    import ui

    ui.welcome_message()
    ui.select_and_execute_task()


if __name__ == "__main__":
    main()
