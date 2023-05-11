import time


def has_elapsed(start_time: float, interval_duration: float) -> bool:
    """Returns True if the time 'start_time' added to the interval duration elapsed.

        :param start_time: The start time of the interval.
        :type start_time: float.

        :param interval_duration: The duration of the interval.
        :type interval_duration: float.

        :return: True if elapsed.
        :rtype: bool.

    """
    return time.time() > start_time + interval_duration
