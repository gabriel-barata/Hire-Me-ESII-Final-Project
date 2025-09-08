from tkinter import Tk
from unittest.mock import MagicMock, patch

import pytest

from app.modules import client


@pytest.fixture
def root():
    return Tk()


def test_get_details(mock_db_connection):
    mock_db_connection.fetchall.return_value = [
        ("Test Client", "Test Location", "M", 1)
    ]
    client.get_details("test@example.com")
    assert client.name == "Test Client"
    assert client.location == "Test Location"
    assert client.gen == "M"
    assert client.clicid == 1


def test_apply_success(mock_db_connection):
    table = MagicMock()
    table.focus.return_value = "item1"
    table.item.return_value = (1, "Developer", "FullTime")
    mock_db_connection.fetchall.return_value = []

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        client.apply(table)
        mock_showinfo.assert_called_with(
            "Thanks", "Your application has been submitted"
        )


def test_apply_no_item_selected():
    table = MagicMock()
    table.focus.return_value = ""

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        client.apply(table)
        mock_showinfo.assert_called_with(
            "ALERT!", "Please select a job to apply."
        )


def test_apply_already_applied(mock_db_connection):
    table = MagicMock()
    table.focus.return_value = "item1"
    table.item.return_value = (1, "Developer", "FullTime")
    mock_db_connection.fetchall.return_value = [(1,)]

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        client.apply(table)
        mock_showinfo.assert_called_with(
            "Oops", "It seems like you have already applied to this job"
        )


def test_delet(mock_db_connection):
    table = MagicMock()
    table.focus.return_value = "item1"
    table.item.return_value = (1, "Developer", "FullTime")

    with (
        patch("tkinter.messagebox.showinfo") as mock_showinfo,
        patch("app.modules.client.myapp") as mock_myapp,
    ):
        client.delet(table)
        mock_showinfo.assert_called_with(
            "Thanks", "Your application has been Deleted"
        )
        mock_myapp.assert_called_once()


def test_delet_no_item_selected(mock_db_connection):
    table = MagicMock()
    table.focus.return_value = ""

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        client.delet(table)
        mock_showinfo.assert_called_with(
            "ALERT!", "Please select an application to delete."
        )


def test_showalljobs(mock_db_connection):
    table = MagicMock()
    mock_db_connection.fetchall.return_value = [
        (1, "Dev", "FullTime", "Corp A", "City A", "BSc", "1", 5000),
        (2, "QA", "PartTime", "Corp B", "City B", "MSc", "3", 6000),
    ]

    client.showalljobs(table)

    assert table.insert.call_count == 2
    table.insert.assert_any_call(
        "",
        0,
        text="",
        values=(1, "Dev", "FullTime", "Corp A", "City A", "BSc", "1", 5000),
    )


def test_show_myapplications(mock_db_connection):
    table = MagicMock()
    mock_db_connection.fetchall.return_value = [
        (10, "Analyst", "FullTime", "Data Inc.", "Remote", "Stats", "2", 7000),
    ]
    client.clicid = 1

    client.show_myapplications(table)

    assert table.insert.call_count == 1
    table.insert.assert_called_with(
        "",
        0,
        text="",
        values=(
            10,
            "Analyst",
            "FullTime",
            "Data Inc.",
            "Remote",
            "Stats",
            "2",
            7000,
        ),
    )


def test_sort_alljobs(mock_db_connection):
    table = MagicMock()
    with patch("app.modules.client.search_d", create=True) as mock_search_d:
        mock_search_d.get.return_value = "JobRole"

        client.sort_alljobs(table)
        table.delete.assert_called_once_with(*table.get_children())
        mock_db_connection.execute.assert_called_with(
            "select job.JID,job.JobRole,job.JobType, recruiter.CompanyName"
            ", recruiter.CompanyLocation, job.Qualification, job.MinExp,"
            " job.Salary from hireme.job JOIN hireme.recruiter ON "
            "job.rid=recruiter.rid order by JobRole"
        )


def test_sort_myapplications(mock_db_connection):
    table = MagicMock()
    client.clicid = 1
    with patch("app.modules.client.search_d", create=True) as mock_search_d:
        mock_search_d.get.return_value = "JobRole"

        client.sort_myapplications(table)
        table.delete.assert_called_once_with(*table.get_children())
        mock_db_connection.execute.assert_called_with(
            "SELECT application.aid,job.JobRole, job.JobType,"
            "recruiter.CompanyName, recruiter.CompanyLocation, "
            "job.qualification, job.minexp, job.salary FROM application "
            "JOIN recruiter ON application.rid=recruiter.rid JOIN job ON"
            " application.jid=job.jid where "
            "application.CID=1 order by JobRole"
        )


@patch("app.modules.client.showalljobs")
@patch("app.modules.client.ttk")
@patch("app.modules.client.Button")
@patch("app.modules.client.Label")
@patch("app.modules.client.Scrollbar")
def test_available_ui_creation(
    mock_scrollbar, mock_label, mock_button, mock_ttk, mock_showalljobs, root
):
    with patch.multiple(
        "app.modules.client",
        create=True,
        rt=MagicMock(),
        tab=MagicMock(),
        bgr=MagicMock(),
    ):
        client.available()

        assert client.bgr.destroy.called
        assert mock_label.called
        assert mock_button.call_count == 2
        assert mock_ttk.Treeview.called
        mock_showalljobs.assert_called_once()


@patch("app.modules.client.ttk")
@patch("app.modules.client.Button")
@patch("app.modules.client.Label")
@patch("app.modules.client.Scrollbar")
def test_myapp_ui_creation(
    mock_scrollbar, mock_label, mock_button, mock_ttk, root
):
    with patch.multiple(
        "app.modules.client",
        create=True,
        rt=MagicMock(),
        tab=MagicMock(),
        bgr=MagicMock(),
    ):
        client.myapp()

        assert client.bgr.destroy.called
        assert mock_label.called
        assert mock_button.call_count == 2
        assert mock_ttk.Treeview.called


@patch("app.modules.client.get_details")
@patch("app.modules.client.logi")
@patch("app.modules.client.PhotoImage")
@patch("app.modules.client.Button")
@patch("app.modules.client.Label")
@patch("app.modules.client.Frame")
def test_cli_ui_initialization(
    mock_frame,
    mock_label,
    mock_button,
    mock_photoimage,
    mock_logi,
    mock_get_details,
    root,
):
    test_email = "client@test.com"
    client.gen = "M"

    client.cli(root, test_email)

    mock_get_details.assert_called_once_with(test_email)

    texts = [c.kwargs.get("text") for c in mock_button.call_args_list]
    assert "LOGOUT" in texts
    assert "Available Jobs" in texts
    assert "My Applications" in texts
