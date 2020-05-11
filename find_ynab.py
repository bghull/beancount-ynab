#!/usr/bin/env python

import json
import sys
from pathlib import Path


def find_budget(ynab4):
    try:
        meta = (ynab4 / "Budget.ymeta").read_text()
    except FileNotFoundError:
        print("No Budget.ymeta found. Are you sure this is a .ynab4 directory?")
        sys.exit(1)
    meta_text = json.loads(meta)
    # if meta_text["formatVersion"] != "2":
    #     print("Data not in YNAB format version 2.")
    #     sys.exit(1)
    data_dir = meta_text["relativeDataFolderName"]
    devices = (ynab4 / data_dir / "devices").glob("*.ydevice")
    possible_budgets = []
    for d in devices:
        details = json.loads(d.read_text())
        if details["hasFullKnowledge"]:
            possible_budgets.append(details["deviceGUID"])
    has_budget_file = [
        pb for pb in possible_budgets if (ynab4 / data_dir / pb / "Budget.yfull").exists()
    ]
    if has_budget_file:
        if len(has_budget_file) == 1:
            return ynab4 / data_dir / has_budget_file[0] / "Budget.yfull"
        else:
            print("More than one Budget.yfull found. Open YNAB on desktop to refresh knowledge.")
    else:
        print(f"No Budget.yfull found? Expected to find it in one of:")
        for pb in possible_budgets:
            print(f"{ynab4 / data_dir / pb}")
        print("Is the latest file mobile only? Open the desktop app to sync.")
        sys.exit(1)


if __name__ == "__main__":
    ynab4 = sys.argv[1]
    fn = find_budget(ynab4)
    print(fn)
