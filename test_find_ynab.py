import json
from pathlib import Path

import pytest

import find_ynab
from conftest import Vars


def test_find_budget_happy_path(ynab4file):
    result = find_ynab.find_budget(ynab4file["home"])
    assert result == ynab4file["home"] / Vars.DATA_FOLDER / Vars.BUDGET_FOLDER / "Budget.yfull"


@pytest.mark.skip
def test_find_budget_wrong_version(ynab4file):
    (ynab4file["home"] / "Budget.ymeta").write_text(
        '{\n\t"formatVersion": "1.2",\n'
        f'\t"relativeDataFolderName": "{Vars.DATA_FOLDER}",\n'
        '\t"TED": 17347566400000\n}'
    )
    with pytest.raises(SystemExit):
        result = find_ynab.find_budget(ynab4file["home"])


def test_find_budget_missing_ymeta(ynab4file):
    (ynab4file["home"] / "Budget.ymeta").unlink()
    with pytest.raises(SystemExit):
        result = find_ynab.find_budget(ynab4file["home"])


def test_find_budget_missing_ybudget(ynab4file):
    (ynab4file["budget"] / "Budget.yfull").unlink()
    with pytest.raises(SystemExit):
        result = find_ynab.find_budget(ynab4file["home"])
