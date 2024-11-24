import inspect
import sys
import os

def add_root_to_pythonpath(n_up: int = 0, return_root: bool = False, verbose: bool = False) -> None | str:
    """
    Add the root directory to the sys.path (PYTHONPATH)
    :param n_up: number of directories to go up (0 - current directory)
    :param return_root: if True, return the root directory
    :param verbose: if True, print the root directory

    Note: This function will consider the directory of the caller
    That is, if you call this function from a file $DIR/file.py, it will add $DIR to sys.path given n_up=0

    Example:
    # file.py
    from magic import set_root
    set_root(n_up=1)

    # $DIR/.. is added to sys.path
    ... (other imports)
    """
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_dir = os.path.dirname(caller_filename)
    root_dir = os.path.abspath(os.path.join(caller_dir, *['..' for _ in range(n_up)]))
    sys.path.insert(0, root_dir)

    if verbose:
        print(f"Added {root_dir} to sys.path")
    
    if return_root:
        return root_dir