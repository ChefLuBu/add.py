def divide():
    try:
        a = int(input("Enter a number to be divided: "))
        b = int(input("Enter another number to divide it by: "))
        result = a/b
    except ValueError:
        print("One or more of your inputs aren't numbers.")
        return None
    except ZeroDivisionError:
        print("Can't divide by zero!")
        return None
    except:
        print("Oops, we've stumbled on some unexpected error.")
        return None
    else:
        return result
    finally:
        print("Function complete!")


print("Result: " + str(divide()))