import asyncio
import inspect
from abc import ABCMeta, abstractmethod


class InitAsync(metaclass=ABCMeta):
    """A class that can be initialized asynchronously."""

    def __subclasscheck__(self, subclass):
        return hasattr(subclass, '__await__')

    def __init__(self, *args, **kwargs):
        """This method is called synchronously before awaiting __await__."""
        pass

    @abstractmethod
    async def __init_async__(self):
        pass

    async def __callback__(self):
        pass

    def __await__(self):
        yield from self.__init_async__().__await__()


async def init_async(t, *args):
    """Initialize an object, await on it, and return it.
    If the object has a callback, call/await it."""
    instance = await init_async_no_callback(t, *args)
    if hasattr(instance, '__callback__'):
        # if callback is awaitable
        if inspect.iscoroutinefunction(instance.__callback__):
            await instance.__callback__()
        elif inspect.isfunction(instance.__callback__):
            instance.__callback__()
        else:
            raise TypeError(
                f"Callback is not a function or coroutine function: {instance.__callback__}"
            )
    return instance


async def init_async_no_callback(t, *args):
    """Initialize an object, await on it, and return it.
    Do not call the object's callback."""

    loop = asyncio.get_running_loop()
    instance = await loop.run_in_executor(None, t, *args)
    if hasattr(instance, '__init_async__'):
        await instance.__init_async__()
    elif hasattr(instance, '__await__'):
        await instance
    return instance
