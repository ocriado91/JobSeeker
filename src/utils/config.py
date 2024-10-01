def read_stack_file(
    stack_file: str = "data/default_stack.dat",
) -> list:
    """Read stack file and export as list

    Parameters
    ----------
    stack_file (str): File with all target stack separated by newline.

    Returns
    ---------
    list: A list with all target stacks.

    """
    with open(stack_file, "r") as f:
        # Read all lines at the same time.
        target_stacks = f.readlines()

        # Remove new line characters
        target_stacks = [x.replace("\n", "") for x in target_stacks]

        return target_stacks