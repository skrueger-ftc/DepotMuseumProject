import threading
import argparse
import logging
import os
from queue import Queue

from hardware.buttons import ButtonHandler
from ui.video_handler import VideoHandler

user = os.environ.get('USER')
if user == "wind":
    from displays.wind_water import WindNWater as Display
elif user == "coal":
    from displays.coal import Coal as Display
elif user == "nuclear":
    from displays.nuclear import Nuclear as Display
else:
    from displays.display import Display

def main(args):
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    if args.vlclog:
        os.environ["VLC_VERBOSE"] = str("0")
    else:
        os.environ["VLC_VERBOSE"] = str("-1")

    display = Display(60)
    q = Queue()

    buttons = ButtonHandler(args, display, q)
    threading.Thread(target=buttons.run, args=(), name="Buttons").start()

    if args.video:
        video = VideoHandler(q)
        threading.Thread(target=video.run, args=(), name="Video").start()

    logging.info("Started all threads")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument("--model", default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument("--vlclog", default=False, action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    main(args)
