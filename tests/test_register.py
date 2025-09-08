from tkinter import Tk
from unittest.mock import MagicMock, patch

import pytest

from app.modules import register


@pytest.fixture
def root():
    root_instance = Tk()
    root_instance.withdraw()
    yield root_instance
    root_instance.destroy()


@pytest.fixture
def mock_register_widgets():
    widget_names = [
        "name",
        "email",
        "pwd",
        "cpwd",
        "gender",
        "company",
        "loc",
        "age",
        "workxp",
        "qualification",
        "skills",
    ]

    with patch.multiple(
        "app.modules.register",
        create=True,
        **{name: MagicMock() for name in widget_names},
    ):
        register.gender.get.return_value = "M"
        yield


def test_recruiter_check_success(
    mock_db_connection, root, mock_register_widgets
):
    register.name.get.return_value = "Test Recruiter"
    register.email.get.return_value = "new@recruiter.com"
    register.pwd.get.return_value = "password123"
    register.cpwd.get.return_value = "password123"
    mock_db_connection.fetchall.return_value = []
    with patch(
        "app.modules.register.recruit_complete"
    ) as mock_recruit_complete:
        register.recruiter_check(root)
        mock_recruit_complete.assert_called_once_with(root)


def test_recruiter_check_email_exists(
    mock_db_connection, root, mock_register_widgets
):
    register.email.get.return_value = "exists@recruiter.com"
    mock_db_connection.fetchall.return_value = [("exists@recruiter.com",)]
    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        register.recruiter_check(root)
        mock_showinfo.assert_called_with("EMAIL ALREADY REGISTERED")


def test_recruiter_check_password_mismatch(root, mock_register_widgets):
    register.pwd.get.return_value = "password123"
    register.cpwd.get.return_value = "password456"
    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        register.recruiter_check(root)
        mock_showinfo.assert_called_with("PASSWORDS DO NOT MATCH")


def test_recruiter_check_missing_fields(root, mock_register_widgets):
    register.name.get.return_value = ""
    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        register.recruiter_check(root)
        mock_showinfo.assert_called_with("ALL FIELDS ARE MUST BE FILLED")


def test_recruiter_check_database_error(
    mock_db_connection, root, mock_register_widgets
):
    register.name.get.return_value = "Test Recruiter"
    register.email.get.return_value = "new@recruiter.com"
    register.pwd.get.return_value = "password123"
    register.cpwd.get.return_value = "password123"
    mock_db_connection.execute.side_effect = Exception("Database error")
    with patch("tkinter.messagebox.showerror") as mock_showerror:
        register.recruiter_check(root)
        mock_showerror.assert_called_with(
            "Error", "A database error occurred: Database error"
        )


def test_recruiter_submit_success(
    mock_db_connection, root, mock_register_widgets
):
    register.company.get.return_value = "Test Corp"
    register.loc.get.return_value = "Test City"
    with (
        patch("app.modules.register.logi") as mock_logi,
        patch("tkinter.messagebox.showinfo") as mock_showinfo,
    ):
        register.recruiter_submit(root)
        assert mock_db_connection.execute.call_count == 2
        mock_showinfo.assert_called_with("SUCCESS!", "Registration Successful")
        mock_logi.assert_called_once_with(root)


@patch("app.modules.register.logi")
def test_recruiter_submit_db_error(
    mock_logi, mock_db_connection, root, mock_register_widgets
):
    register.company.get.return_value = "Test Corp"
    register.loc.get.return_value = "Test City"
    mock_db_connection.execute.side_effect = Exception("DB connection failed")
    register.recruiter_submit(root)
    mock_logi.assert_not_called()


def test_client_check_success(mock_db_connection, root, mock_register_widgets):
    register.name.get.return_value = "Test Client"
    register.email.get.return_value = "new@client.com"
    register.pwd.get.return_value = "password123"
    register.cpwd.get.return_value = "password123"
    mock_db_connection.fetchall.return_value = []
    with patch("app.modules.register.client_complete") as mock_client_complete:
        register.client_check(root)
        mock_client_complete.assert_called_once_with(root)


def test_client_check_password_mismatch(root, mock_register_widgets):
    register.pwd.get.return_value = "password123"
    register.cpwd.get.return_value = "wrongpassword"
    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        register.client_check(root)
        mock_showinfo.assert_called_with("PASSWORDS DO NOT MATCH")


def test_client_submit_success(
    mock_db_connection, root, mock_register_widgets
):
    register.age.get.return_value = "30"
    register.loc.get.return_value = "Test Ville"
    register.workxp.get.return_value = "5"
    register.qualification.get.return_value = "PhD"
    register.skills.get.return_value = "Testing, Mocking"
    with (
        patch("app.modules.register.logi") as mock_logi,
        patch("tkinter.messagebox.showinfo") as mock_showinfo,
    ):
        register.client_submit(root)
        assert mock_db_connection.execute.call_count == 2
        mock_showinfo.assert_called_with("SUCCESS!", "Registration Successful")
        mock_logi.assert_called_once_with(root)


def test_client_submit_missing_fields(root, mock_register_widgets):
    register.loc.get.return_value = ""
    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        register.client_submit(root)
        mock_showinfo.assert_called_with("ALL FIELDS ARE MUST BE FILLED")


@patch("app.modules.register.client_regis")
@patch("app.modules.register.recruit_reg")
@patch("app.modules.register.logi")
@patch("app.modules.register.PhotoImage")
@patch("app.modules.register.Button")
@patch("app.modules.register.Label")
@patch("app.modules.register.Frame")
def test_mai_ui(
    mock_frame,
    mock_label,
    mock_button,
    mock_photo,
    mock_logi,
    mock_recruit,
    mock_client,
    root,
):
    register.mai(root)
    assert mock_button.call_count == 3
    assert "command" in mock_button.call_args_list[0].kwargs
    assert "command" in mock_button.call_args_list[1].kwargs
    assert "command" in mock_button.call_args_list[2].kwargs


@patch("app.modules.register.recruiter_check")
@patch("app.modules.register.mai")
@patch("app.modules.register.PhotoImage")
@patch("app.modules.register.Button")
@patch("app.modules.register.Entry")
@patch("app.modules.register.Label")
@patch("app.modules.register.Frame")
def test_recruit_reg_ui(
    mock_frame,
    mock_label,
    mock_entry,
    mock_button,
    mock_photo,
    mock_mai,
    mock_check,
    root,
):
    with patch("app.modules.register.r1", create=True) as mock_r1:
        mock_r1.destroy = MagicMock()
        register.recruit_reg(root)
        mock_r1.destroy.assert_called_once()

    assert mock_label.call_count >= 4
    assert mock_entry.call_count >= 4
    assert mock_button.call_count == 2


@patch("app.modules.register.recruiter_submit")
@patch("app.modules.register.PhotoImage")
@patch("app.modules.register.Button")
@patch("app.modules.register.Entry")
@patch("app.modules.register.ttk")
@patch("app.modules.register.Label")
@patch("app.modules.register.Frame")
def test_recruit_complete_ui(
    mock_frame,
    mock_label,
    mock_ttk,
    mock_entry,
    mock_button,
    mock_photo,
    mock_submit,
    root,
):
    register.recruit_complete(root)
    assert mock_label.call_count >= 3
    assert mock_entry.call_count >= 2
    assert mock_ttk.Radiobutton.call_count == 2

    reg_btn_call = next(
        c for c in mock_button.call_args_list if c.kwargs.get("bd") == 0
    )
    command = reg_btn_call.kwargs.get("command")
    assert callable(command)
    command()
    mock_submit.assert_called_once_with(root)
