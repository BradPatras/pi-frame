import time


# logging util, output to console and write to log file
def log(message: str):
    line = str(time.time()) + ": " + message + "\n"
    print(line)
    # write to log file
    with open("frame.log", "a") as f:
        f.write(line)
