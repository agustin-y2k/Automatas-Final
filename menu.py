import functions as f

def menu():

    print("""
        Choose an option:

        1- List all sessions of a User through the ID.
        2- List all logins in a specific time.
        3- Total time of session of a user.
        4- List all of the differents MAC of a User.
        5- List all Users connected to an AP.
        6- Show traffic of a User.
        7- List APs sorted by total traffic
        8- Quit.
            """)

    try:
        option = int(input("Enter an option: "))
        if option == 1:
            f.list_session_id()
            menu()
        elif option == 2:
            f.list_login_time()
            menu()
        elif option == 3:
            f.total_time_session()
            menu()
        elif option == 4:
            f.list_user_macs()
            menu()
        elif option == 5:
            f.user_conected_ap()
            menu()
        elif option == 6:
            f.user_traffic()
            menu()
        elif option == 7:
            f.list_ap_byTraffic()
            menu()
        elif option == 8:
            print("\nGoodbye!")
            exit()
        else:
            print("\nThe option is not valid.")
            menu()
    except ValueError:
        print("\nPlease enter a numeric option.")
        menu()