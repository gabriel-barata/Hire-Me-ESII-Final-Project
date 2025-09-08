from tkinter import Tk
from unittest.mock import MagicMock, patch

import pytest

from app.modules import recruiter


@pytest.fixture
def root():
    root_instance = Tk()
    root_instance.withdraw()
    yield root_instance
    root_instance.destroy()


def test_get_details(mock_db_connection):
    mock_db_connection.fetchall.return_value = [
        ("Test Recruiter", "Test Company", "F", 1)
    ]
    recruiter.get_details("recruiter@example.com")
    assert recruiter.name == "Test Recruiter"
    assert recruiter.company == "Test Company"


@patch("tkinter.messagebox.showinfo")
def test_submit_job_success(mock_showinfo, mock_db_connection):
    with patch.multiple(
        "app.modules.recruiter",
        create=True,
        role=MagicMock(),
        jtype=MagicMock(),
        qual=MagicMock(),
        exp=MagicMock(),
        sal=MagicMock(),
        recid=1,
    ):
        recruiter.role.get.return_value = "Developer"
        recruiter.jtype.get.return_value = "FullTime"
        recruiter.qual.get.return_value = "BSc"
        recruiter.exp.get.return_value = "2"
        recruiter.sal.get.return_value = "5000"

        recruiter.submit_job()

        mock_db_connection.execute.assert_called_once()
        mock_showinfo.assert_called_with(
            "SUCCESS!", "You have successfully created a Job"
        )


@patch("tkinter.messagebox.showinfo")
def test_submit_job_missing_fields(mock_showinfo):
    with patch.multiple(
        "app.modules.recruiter",
        create=True,
        role=MagicMock(),
        jtype=MagicMock(),
        qual=MagicMock(),
        exp=MagicMock(),
        sal=MagicMock(),
    ):
        recruiter.role.get.return_value = ""
        recruiter.jtype.get.return_value = "FullTime"
        recruiter.qual.get.return_value = "CS"
        recruiter.exp.get.return_value = "1"
        recruiter.sal.get.return_value = "1000"

        recruiter.submit_job()
        mock_showinfo.assert_called_with(
            "ALERT!", "ALL FIELDS ARE MUST BE FILLED"
        )


@patch("tkinter.messagebox.showinfo")
def test_submit_job_type_not_selected(mock_showinfo):
    with patch.multiple(
        "app.modules.recruiter",
        create=True,
        role=MagicMock(),
        jtype=MagicMock(),
        qual=MagicMock(),
        exp=MagicMock(),
        sal=MagicMock(),
    ):
        recruiter.role.get.return_value = "Developer"
        recruiter.jtype.get.return_value = "Select"
        recruiter.qual.get.return_value = "CS"
        recruiter.exp.get.return_value = "1"
        recruiter.sal.get.return_value = "1000"

        recruiter.submit_job()
        mock_showinfo.assert_called_with("ALERT!", "Please provide Job Type")


@patch("app.modules.recruiter.posted")
@patch("tkinter.messagebox.showinfo")
def test_deletjob(mock_showinfo, mock_posted, mock_db_connection):
    table = MagicMock()
    table.focus.return_value = "item1"
    table.item.return_value = (
        1,
        "Developer",
    )

    recruiter.deletjob(table)

    assert mock_db_connection.execute.call_count == 2
    mock_showinfo.assert_called_with("Thanks", "Your Job has been Deleted")
    mock_posted.assert_called_once()


def test_deletjob_no_item_selected(mock_db_connection):
    table = MagicMock()
    table.focus.return_value = ""

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        recruiter.deletjob(table)
        mock_showinfo.assert_called_with(
            "ALERT!", "Please select a job to delete."
        )


def test_show_all(mock_db_connection):
    table = MagicMock()
    mock_db_connection.fetchall.return_value = [
        (1, 101, "Dev", "FullTime", "BSc", 2, 5000),
    ]
    recruiter.recid = 1

    recruiter.show_all(table)

    assert table.insert.call_count == 1
    table.insert.assert_called_with(
        "", 0, text="", values=(101, "Dev", "FullTime", "BSc", 2, 5000)
    )


def test_show_applicants(mock_db_connection):
    table = MagicMock()
    mock_db_connection.fetchall.return_value = [
        (
            "Dev",
            "John Doe",
            "john@mail.com",
            30,
            "City A",
            "M",
            5,
            "Python",
            "MSc",
        ),
    ]
    recruiter.recid = 1

    recruiter.show_applicants(table)

    assert table.insert.call_count == 1
    table.insert.assert_called_with(
        "",
        0,
        text="",
        values=(
            "Dev",
            "John Doe",
            "john@mail.com",
            30,
            "City A",
            "M",
            5,
            "Python",
            "MSc",
        ),
    )


def test_sort_all(mock_db_connection):
    table = MagicMock()
    recruiter.recid = 1

    with patch("app.modules.recruiter.search_d", create=True) as mock_search_d:
        mock_search_d.get.return_value = "JobRole"

        recruiter.sort_all(table)

        table.delete.assert_called_once_with(*table.get_children())
        mock_db_connection.execute.assert_called_once_with(
            "select RID,JID, JobRole, JobType, Qualification, MinExp,"
            "Salary FROM hireme.job where RID=1 order by JobRole"
        )


def test_sort_applicants(mock_db_connection):
    table = MagicMock()
    recruiter.recid = 1

    with patch("app.modules.recruiter.search_d", create=True) as mock_search_d:
        mock_search_d.get.return_value = "CName"

        recruiter.sort_applicants(table)

        table.delete.assert_called_once_with(*table.get_children())
        mock_db_connection.execute.assert_called_once_with(
            "SELECT job.JobRole, client.CName, client.CEmail, client.CAge,"
            "client.CLocation, client.CGender, client.CExp, "
            "client.CSkills, client.CQualification FROM application "
            "JOIN client ON application.cid=client.CID JOIN job ON "
            "job.jid=application.jid where job.rid=1 order by CName"
        )


@patch("app.modules.recruiter.show_all")
@patch("app.modules.recruiter.ttk")
@patch("app.modules.recruiter.Button")
@patch("app.modules.recruiter.Label")
@patch("app.modules.recruiter.Scrollbar")
def test_posted_ui_creation(
    mock_scrollbar, mock_label, mock_button, mock_ttk, mock_show_all, root
):
    with patch.multiple(
        "app.modules.recruiter",
        create=True,
        rt=MagicMock(),
        tab=MagicMock(),
        bgr=MagicMock(),
    ):
        recruiter.posted()
        assert recruiter.bgr.destroy.called
        assert mock_label.called
        assert mock_button.called
        assert mock_ttk.Treeview.called
        mock_show_all.assert_called_once()


@patch("app.modules.recruiter.show_applicants")
@patch("app.modules.recruiter.ttk")
@patch("app.modules.recruiter.Button")
@patch("app.modules.recruiter.Label")
@patch("app.modules.recruiter.Scrollbar")
def test_app_ui_creation(
    mock_scrollbar,
    mock_label,
    mock_button,
    mock_ttk,
    mock_show_applicants,
    root,
):
    with patch.multiple(
        "app.modules.recruiter",
        create=True,
        rt=MagicMock(),
        tab=MagicMock(),
        bgr=MagicMock(),
    ):
        recruiter.app()
        assert recruiter.bgr.destroy.called
        assert mock_label.called
        assert mock_button.called
        assert mock_ttk.Treeview.called
        mock_show_applicants.assert_called_once()


@patch("app.modules.recruiter.submit_job")
@patch("app.modules.recruiter.Button")
@patch("app.modules.recruiter.Entry")
@patch("app.modules.recruiter.ttk")
@patch("app.modules.recruiter.Label")
@patch("app.modules.recruiter.PhotoImage")
def test_create_ui_creation(
    mock_photo,
    mock_label,
    mock_ttk,
    mock_entry,
    mock_button,
    mock_submit_job,
    root,
):
    with patch.multiple(
        "app.modules.recruiter",
        create=True,
        rt=MagicMock(),
        tab=MagicMock(),
        bgr=MagicMock(),
    ):
        recruiter.create()
        assert recruiter.bgr.destroy.called
        assert mock_label.called
        mock_button.assert_called_with(
            recruiter.tab,
            text="Submit",
            font=(20),
            bg="#45CE30",
            fg="#FFFFFF",
            command=recruiter.submit_job,
        )


@patch("app.modules.recruiter.get_details")
@patch("app.modules.recruiter.logi")
@patch("app.modules.recruiter.PhotoImage")
@patch("app.modules.recruiter.Button")
@patch("app.modules.recruiter.Label")
@patch("app.modules.recruiter.Frame")
def test_rec_ui_initialization(
    mock_frame,
    mock_label,
    mock_button,
    mock_photoimage,
    mock_logi,
    mock_get_details,
    root,
):
    recruiter.rec(root, "recruiter@test.com")
    mock_get_details.assert_called_once_with("recruiter@test.com")
    assert mock_button.call_count >= 4
    logout_call = next(
        c
        for c in mock_button.call_args_list
        if c.kwargs.get("text") == "LOGOUT"
    )
    logout_command = logout_call.kwargs.get("command")
    assert logout_command is not None

    logout_command()
    mock_logi.assert_called_once_with(root)
