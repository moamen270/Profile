"""Section 1 — Work authorization / sponsorship hard filter.

Wrong answer on the form = instant auto-rejection, before any parsing.

API:
    work_authorization_filter(authorized, requires_authorization,
                              needs_sponsorship=False, offers_sponsorship=False)
        -> FilterResult
"""
from __future__ import annotations

from ..models import FilterResult


def work_authorization_filter(
    authorized: bool | None,
    requires_authorization: bool = True,
    needs_sponsorship: bool = False,
    offers_sponsorship: bool = False,
) -> FilterResult:
    if not requires_authorization:
        return FilterResult("work_authorization", True, "Role does not require work authorization", "filter")
    if authorized is None:
        return FilterResult("work_authorization", False, "Authorization question unanswered", "knockout")
    if not authorized:
        return FilterResult(
            "work_authorization", False,
            "Not authorized to work — instant auto-reject (knockout form question)",
            "knockout",
        )
    if needs_sponsorship and not offers_sponsorship:
        return FilterResult(
            "work_authorization", False,
            "Requires sponsorship and employer does not sponsor — instant auto-reject",
            "knockout",
        )
    return FilterResult("work_authorization", True, "Authorized", "knockout")


if __name__ == "__main__":
    print(work_authorization_filter(True))
    print(work_authorization_filter(False))
    print(work_authorization_filter(True, needs_sponsorship=True))
    print(work_authorization_filter(True, needs_sponsorship=True, offers_sponsorship=True))
