from typing import Annotated

from PLUGINS.SIRP.sirpapi import Case


def get_case_by_rowid(rowid: Annotated[str, "Case Rowid"]):
    """
    Retrieve a security case by its unique Case Rowid.
    
    This tool allows you to look up full details of a specific case when you have its ID.
    Useful for retrieving context, status, or artifacts associated with a known case identifier.

    Args:
        rowid: The unique string identifier of the case (e.g., '2101ff98-f52e-4f38-b107-fe53f7f77b5c').

    Returns:
        The Case object containing all case details if found, otherwise None.
    """
    return Case.get(rowid)


def get_case_by_case_id(case_id: Annotated[str, "Case Id"]):
    return Case.get_by_case_id(case_id)
