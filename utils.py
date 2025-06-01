def format_rupiah(amount):
    try:
        amount = float(amount)
        return f"{amount:,.0f}".replace(",", ".")
    except Exception:
        return f"{amount}"
