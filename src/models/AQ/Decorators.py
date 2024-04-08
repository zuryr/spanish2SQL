def repetition_decorator(f):
    def wrapper():
        flag = True
        while flag:
            f()
            flag = input("Do you want to execute again? (y/n): ") == "y"

    return wrapper
