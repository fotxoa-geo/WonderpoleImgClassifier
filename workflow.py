import argparse
import os
import time
from download import run_dowloand_slpit

def create_directory(directory: str):
    if os.path.isdir(directory):
        pass
    else:
        os.mkdir(directory)

def display_menu():
    print("Welcome to the Interactive Menu")
    print("A... Download wonderpole images")
    print("B... Run image classification")
    print('C... Run fractional cover')
    print("D... Exit")


def main():
    parser = argparse.ArgumentParser(description='Run workflow file')
    args = parser.parse_args()

    for i in ['wonderpole_images', 'quadrats', 'rgb_image_endmembers', 'objects', 'plot_landscape']:
        create_directory(os.path.join(i))

    while True:
        display_menu()
        choice = input("Enter desired mode: ").upper()

        if choice == "A":
            run_dowloand_slpit()

        elif choice == 'B':
            print('download coming soon...')

        elif choice == 'C':
            print('farctional cover coming soon...')

        elif choice == "D":
            outro = "Exiting... Thanks for using the tool!"
            print(outro)
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == '__main__':
    main()
