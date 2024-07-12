# example of waiting for all tasks to complete
from random import random
import asyncio

# coroutine to execute in a new task
async def task_coro(arg):
    # generate a random value between 0 and 1
    value = 1 + random()
    # block for a moment
    print(f'Microwave {arg}: Cooking {value} seconds...')
    await asyncio.sleep(value)
    print(f'Microwave {arg}: Finish')
    # report the value
    return arg, value

# main coroutine
async def main():
    # create many tasks
    menu = ["Rice", "Noodle", "Curry"]
    tasks = [asyncio.create_task(task_coro(i)) for i in menu]
    # wait for the first task to complete
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    # get the first completed task
    print(f'Complete task, {len(done)} tasks.')
    first_ready_task = done.pop()
    print(f'- {first_ready_task.result()[0]} is the first to complete in {first_ready_task.result()[1]}')
    print(f'Uncomplete task, {len(pending)} tasks.')

# start the asyncio program
asyncio.run(main())