import threading

class JobThreadUtils:

    @staticmethod
    def resurrect_thread(thread, thread_name, target_function):
        if not thread.is_alive():
            message = "Thread {} is not alive. Resurrecting it.".format(thread_name)
            new_thread = threading.Thread(target=target_function, name=thread_name)
            new_thread.start()
            return new_thread, message
        else:
            message = "Thread {} is still running.".format(thread_name)
        return thread, message
