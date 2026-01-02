import time
from tensorboard import program

import custom_logging  # Centralized logging initialization

log_path = "logs"


def launch_tensorboard_pipeline():

    tb = program.TensorBoard()
    tb.configure(argv=[None, "--logdir", log_path, "--host", "0.0.0.0"])
    url = tb.launch()


    while True:
        time.sleep(600)
