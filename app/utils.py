def generateLeadingPaths(path):
    """
    Generator for leading paths

    Example:
    "test1/test2" generates ["test1", "test1/test2"]

    Args:
        path (str): a path delimited by slashes (/)
    """
    subPaths = path.split('/')
    currentPath = subPaths[0]
    subPaths.pop(0)

    for subPath in subPaths:
        currentPath = (currentPath + "/" + subPath)
        yield currentPath
