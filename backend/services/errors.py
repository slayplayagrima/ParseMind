class DocumentError(ValueError):
    """
    Raised when an uploaded document can't be processed
    because of a problem with the document itself.

    The message is safe to show to the user.
    """
