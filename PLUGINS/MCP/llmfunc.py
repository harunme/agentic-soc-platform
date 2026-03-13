from typing import Annotated, Optional

from PLUGINS.SIRP.nocolymodel import Group, Condition, Operator
from PLUGINS.SIRP.sirpapi import Case
from PLUGINS.SIRP.sirpmodel import CaseModel, Severity, CaseStatus


def get_case(case_id: Annotated[str, "Case Id"]):
    """
    Retrieve a security case by its Case ID (e.g. case_000005)

    Args:
        case_id: The case identifier string.

    Returns:
        The Case object if found, otherwise None.
    """
    model = Case.get_by_case_id(case_id)
    result = model.model_dump_json_for_ai()
    return result


def list_cases(
        status: Annotated[Optional[str], "Filter by case status"] = None,
        severity: Annotated[Optional[str], "Filter by severity level"] = None,
        limit: Annotated[int, "Maximum number of results to return"] = 10
):
    """
    List security cases with optional filters.

    Args:
        status: Filter cases by status (e.g., 'New', 'In Progress', 'Closed')
        severity: Filter cases by severity (e.g., 'Critical', 'High', 'Medium', 'Low')
        limit: Maximum number of cases to return (default: 10)

    Returns:
        List of Case objects matching the filters.
    """
    conditions = []

    if status:
        conditions.append(Condition(field="status", operator=Operator.EQ, value=status))

    if severity:
        conditions.append(Condition(field="severity", operator=Operator.EQ, value=severity))

    filter_model = Group(logic="AND", children=conditions) if conditions else Group(logic="AND", children=[])

    results = Case.list(filter_model)
    return results[:limit]


def create_case(
        title: Annotated[str, "Case title"],
        severity: Annotated[str, "Severity level: Critical, High, Medium, Low, Info"],
        description: Annotated[str, "Case description"] = "",
        status: Annotated[str, "Case status"] = "New"
):
    """
    Create a new security case.

    Args:
        title: The title of the case
        severity: Severity level (Critical, High, Medium, Low, Info)
        description: Detailed description of the case
        status: Initial status (default: New)

    Returns:
        The created Case object with its assigned rowid.
    """
    case_model = CaseModel(
        title=title,
        severity=Severity(severity),
        description=description,
        status=CaseStatus(status)
    )
    return Case.create(case_model)


def update_case(
        case_id: Annotated[str, "Case ID to update"],
        title: Annotated[Optional[str], "New title"] = None,
        severity: Annotated[Optional[str], "New severity"] = None,
        status: Annotated[Optional[str], "New status"] = None,
        description: Annotated[Optional[str], "New description"] = None
):
    """
    Update an existing security case.

    Args:
        case_id: The case ID to update
        title: New title (optional)
        severity: New severity level (optional)
        status: New status (optional)
        description: New description (optional)

    Returns:
        The updated Case object.
    """
    case = Case.get_by_case_id(case_id)
    if not case:
        return None

    if title:
        case.title = title
    if severity:
        case.severity = Severity(severity)
    if status:
        case.status = CaseStatus(status)
    if description:
        case.description = description

    return Case.update(case)


if __name__ == "__main__":
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ASP.settings")
    import django

    django.setup()
    result = get_case("case_000005")
    result = list_cases()
    print(result)
