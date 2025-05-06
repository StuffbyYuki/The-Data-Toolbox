def cents_to_dollars(cents):
    """
    Convert cents to dollars with 2 decimal places.

    Args:
        cents (int, float, or Decimal): The amount in cents

    Returns:
        Decimal: The amount in dollars with 2 decimal places
    """
    if cents is None:
        return None
    return round(float(cents) / 100, 2)
