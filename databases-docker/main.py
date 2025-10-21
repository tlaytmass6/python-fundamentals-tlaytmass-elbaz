# main.py
# test script for the database and ORM assignment
from db import get_all_users, find_user, add_user, update_user

def show_users(users):
    for u in users:
        print(f"{u.id:2} | {u.username:10} | {u.email:30} | {u.fullname}")

if __name__ == "__main__":
    print("=== All users currently in the database ===")
    show_users(get_all_users())

    print("\n=== Adding a new user (layla) ===")
    add_user("layla", "layla.karim@school.edu", "Layla Karim")

    print("\n=== Checking if layla exists now ===")
    u = find_user("layla")
    if u:
        print("Found:", u)

    print("\n=== Updating Layla's name ===")
    if u:
        update_user(u.id, fullname="Layla K.")

    print("\n=== Final user list ===")
    show_users(get_all_users())
