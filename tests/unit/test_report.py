from numia import report


def test_main_runs_without_error(capsys):
    report.main()

    captured = capsys.readouterr()
    assert "Report" in captured.out
