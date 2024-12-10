import time
import logging
from tensorboard import program

log_path = "logs"


def launch_tensorboard_pipeline():
    logging.getLogger("root").setLevel(logging.WARNING)
    logging.getLogger("tensorboard").setLevel(logging.WARNING)

    tb = program.TensorBoard()
    tb.configure(argv=[None, "--logdir", log_path, "--host", "0.0.0.0"])
    url = tb.launch()


    while True:
        time.sleep(600)
