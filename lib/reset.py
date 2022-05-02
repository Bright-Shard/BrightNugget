def reset():
    with open("boot.py", "w") as file:
        file.write('from storage import remount \n remount("/", True)')
        file.close()
    with open("brightnugget.conf", "w") as file:
        file.write("{}")
        file.close()
