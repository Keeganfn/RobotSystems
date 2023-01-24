import picarx_improved 
import atexit

if __name__ == "__main__":
    car = picarx_improved.Picarx()
    choice = -1
    while choice != 0:
        print(f"Choose a maneuver: \n 1. Forward and Back \n 2. Parallel Park Left \n 3. Parallel Park Right \n 4. K-Turn \n 0. Quit")
        choice = input()
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                print("FORWARD AND BACK")
                car.maneuver_move_forward_back()
            elif choice == 2:
                print("PARK LEFT")
                car.maneuver_park_left()
            elif choice == 3:
                print("PARK RIGHT")
                car.maneuver_park_right()
            elif choice == 4:
                print("K-TURN")
                car.maneuver_k_turn()
            elif choice == 0:
                print("QUITTING")
                break
            else:
                print("Not a valid input!")
        else:
            print("Not a valid input!")
    atexit.register(car.stop)