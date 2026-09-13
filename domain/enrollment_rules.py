def determine_enrollment_status(current_credits, requested_credits, has_prereqs, override_code, max_credits):
    if current_credits + requested_credits > max_credits:
        return "FAILED - CREDIT LIMIT EXCEEDED"
    if has_prereqs:
        return "ENROLLED"
    if override_code == "DEAN_APPROVED":
        return "ENROLLED (OVERRIDE)"
    return "FAILED - MISSING PREREQS"