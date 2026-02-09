def print_table(rows):
    if not rows:
        print("No applications found.\n")
        return

    headers = ("ID", "Company", "Role", "Stage")
    str_rows = [(str(r[0]), r[1], r[2], r[3]) for r in rows]

    widths = [
        max(len(headers[0]), max(len(r[0]) for r in str_rows)),
        max(len(headers[1]), max(len(r[1]) for r in str_rows)),
        max(len(headers[2]), max(len(r[2]) for r in str_rows)),
        max(len(headers[3]), max(len(r[3]) for r in str_rows)),
    ]

    fmt = f"{{:<{widths[0]}}}  {{:<{widths[1]}}}  {{:<{widths[2]}}}  {{:<{widths[3]}}}"
    print(fmt.format(*headers))
    print("-" * (sum(widths) + 6))

    for r in str_rows:
        print(fmt.format(*r))

    print()

def print_stage_summary(rows):
    if not rows:
        return

    print("Stage summary:")
    for stage, count in rows:
        print(f"{stage}: {count}")
    print()
