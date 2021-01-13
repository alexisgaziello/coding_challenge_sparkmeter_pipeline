import asyncio
import logging

'''
A little more context on the objective of the class would be ideal to correctly debug it.
'''

# Missing libraries
import os
from datetime import datetime

logger = logging.getLogger(__name__)
SLEEP_DURATION = os.getenv("SLEEP_DURATION")

# Added self variable, necessary in every class definition to refer to the instance itself
class Pipeline():
    
    def __init__(self, *args, **kwargs):
        
        if SLEEP_DURATION is not None:
            self.default_sleep_duration = SLEEP_DURATION
        # Couldn't retrieve sleep duration from environment.
        # Let's try from constructor.
        else:
            # We want to ensure that a default sleep duration exists
            # I am using kwargs instead of putting a parameter, in order to use the current infrastructure
            # Since I consider default sleep duration a necessary a parameter, an error is raised
            # if the value is not set.
            try:
                self.default_sleep_duration = kwargs["default_sleep_duration"]
            except:
                raise ValueError("Please specify a default sleep duration with the parameter 'default_sleep_duration'.")

        self.loop = asyncio.get_event_loop()

    # Create a non async function that calls async function as suggested in 
    # https://stackoverflow.com/questions/42009202/how-to-call-a-async-function-contained-in-a-class
    def sleep_for(self, coro, *args, **kwargs):
        return self.loop.run_until_complete(self.__async__sleep_for(coro, *args, **kwargs))

    async def __async__sleep_for(self, coro, *args, **kwargs):
        # sleep_duration can be set through kwargs.
        if kwargs.get("sleep_duration") is not None:
            sleep_duration = kwargs["sleep_duration"]
        # if not set, use default value
        else:
            sleep_duration = self.default_sleep_duration
        
        # Keyword await is necessary to sleep
        await asyncio.sleep(sleep_duration)
        logger.info("Slept for %s seconds", sleep_duration)
        
        start = datetime.now()
        # Execute coroutine
        await coro(*args, **kwargs) # Mistake in kwarg name (s missing)

        end = datetime.now()
        time_elapsed = (end - start).total_seconds() # time is end - start
        logger.debug(f"Executed the coroutine for {time_elapsed} seconds")


if __name__ == "__main__":

    ###########
    # Testing #
    ###########

    # Set logger output to console
    logger.setLevel(logging.DEBUG)
    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.info("TEST: pipeline.py\n")

    pipeline = Pipeline(default_sleep_duration = 2)

    async def say_after(*args, **kwargs):
        await asyncio.sleep(kwargs["delay"])
        print(kwargs["what"])

    pipeline.sleep_for(say_after, delay=0, what="Hello World!")