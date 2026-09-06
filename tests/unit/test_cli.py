import pytest

from numia import cli


def test_no_subcommand_prints_banner(capsys):
    cli.main([])

    captured = capsys.readouterr()
    assert "Numia" in captured.out


def test_init_prints_the_given_path(capsys):
    cli.main(["init", "."])

    captured = capsys.readouterr()
    assert captured.out.strip() == "."


def test_init_prints_an_arbitrary_path(capsys):
    cli.main(["init", "/some/path"])

    captured = capsys.readouterr()
    assert captured.out.strip() == "/some/path"


def test_init_without_path_exits_with_error():
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["init"])

    assert exc_info.value.code != 0


def test_unknown_subcommand_exits_with_error():
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["bogus"])

    assert exc_info.value.code != 0


def test_report_prints_placeholder(capsys):
    cli.main(["report"])

    captured = capsys.readouterr()
    assert "Report" in captured.out
