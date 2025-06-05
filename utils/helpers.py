import random
import time

def random_delay(min_delay, max_delay):
    time.sleep(random.uniform(min_delay, max_delay))