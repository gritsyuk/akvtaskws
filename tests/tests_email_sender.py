import pytest
from unittest.mock import patch, MagicMock
from src.email_akv import EmailSender


@pytest.fixture
def email_sender():
    # Создаём экземпляр EmailSender для тестов
    return EmailSender(email_sender="test@example.com", password="password")


@patch('smtplib.SMTP_SSL')
def test_send_email_success(mock_smtp_ssl, email_sender):
    # Настраиваем мок для SMTP-сервера
    mock_server = MagicMock()
    mock_smtp_ssl.return_value.__enter__.return_value = mock_server

    # Данные для теста
    email_list = ["recipient@example.com"]
    email_subj = "Test Subject"
    html_table = "<html><body>Test email</body></html>"

    # Вызываем тестируемый метод
    email_sender.send_email(html_table, email_list, email_subj)

    # Проверяем, что соединение с SMTP-сервером было установлено
    mock_smtp_ssl.assert_called_with('smtp.mail.ru', 465)
    mock_server.login.assert_called_with("test@example.com", "password")
    
    # Проверяем, что письмо было отправлено
    mock_server.sendmail.assert_called_once()
    assert "recipient@example.com" in mock_server.sendmail.call_args[0][1]  # Проверка получателя
    assert email_subj in mock_server.sendmail.call_args[0][2]  # Проверка темы письма


@patch('smtplib.SMTP_SSL')
def test_send_email_failure(mock_smtp_ssl, email_sender, caplog):
    # Настраиваем мок, который выбрасывает исключение
    mock_smtp_ssl.side_effect = Exception("Failed to connect")

    # Данные для теста
    email_list = ["recipient@example.com"]
    email_subj = "Test Subject"
    html_table = "<html><body>Test email</body></html>"

    # Логируем ошибки и вызываем метод
    with caplog.at_level('ERROR'):
        email_sender.send_email(html_table, email_list, email_subj)
        # Проверяем, что ошибка залогировалась
        assert "Failed to send email" in caplog.text
