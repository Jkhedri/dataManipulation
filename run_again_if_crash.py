from subprocess import run
from time import sleep

# Path and name to the script you are trying to start
file_path = "chatgpt/cgpt2.py" 

max_restarts = 5
restart_timer = 2

def start_script(restart_nums):
    try:
        # Make sure 'python' command is available
        run("python "+file_path, check=True) 
    except:
        # Script crashed, lets restart it!
        print("Script crashed, restarting...")
        handle_crash(restart_nums)

def handle_crash(restart_nums):
    sleep(restart_timer)  # Restarts the script after 2 seconds
    restart_nums += 1
    if restart_nums > max_restarts:
        print("Script crashed too many times, stopping...")
        return
    print("Restarting script...")
    start_script(restart_nums)

start_script(0)