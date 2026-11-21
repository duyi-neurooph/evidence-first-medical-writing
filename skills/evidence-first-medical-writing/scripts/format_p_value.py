"""Format a verified unrounded P value using the skill default, not journal overrides."""

import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def format_p_value(unrounded: str, *, exact_one: bool = False) -> str:
    """Accept a decimal source string, never a rounded display or a threshold."""
    if not isinstance(unrounded, str):
        raise ValueError("Supply the original decimal string, not a binary float.")
    try:
        value = Decimal(unrounded)
    except InvalidOperation:
        raise ValueError("Supply an unrounded number, not a threshold or label.") from None
    if not value.is_finite() or not 0 <= value <= 1:
        raise ValueError("P must be a finite number from 0 to 1.")
    if value == 1:
        if not exact_one:
            raise ValueError("Confirm exact equality to 1; a rounded 1.000 is insufficient.")
        return "P = 1.000"
    if exact_one:
        raise ValueError("Exact equality to 1 conflicts with the supplied value.")
    if value < Decimal("0.001"):
        return "P < 0.001"
    if value > Decimal("0.999"):
        return "P > 0.999"
    rounded = value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    return f"P = {rounded:.3f}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unrounded", required=True, metavar="VALUE",
                        help="Verified unrounded decimal output; do not use a rounded display.")
    parser.add_argument("--exact-one", action="store_true",
                        help="The source analysis confirms that VALUE is exactly 1.")
    args = parser.parse_args()
    try:
        print(format_p_value(args.unrounded, exact_one=args.exact_one))
    except ValueError as error:
        parser.error(str(error))
