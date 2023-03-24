import smtplib

def send_email(from_addr, to_addr, subject, text, encode='utf-8'):
    """
    Отправка электронного письма (email)
    """

    # оставшиеся настройки
    passwd = "*****************"
    server = "smtp.mail.ru"
    port = 587
    charset = f'Content-Type: text/plain; charset={encode}'
    mime = 'MIME-Version: 1.0'
    # формируем тело письма
    body = "\r\n".join((f"From: {from_addr}", f"To: {to_addr}",
           f"Subject: {subject}", mime, charset, "", text))

    try:
        # подключаемся к почтовому сервису
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.ehlo()
        # логинимся на почтовом сервере
        smtp.login(from_addr, passwd)
        # пробуем послать письмо
        smtp.sendmail(from_addr, to_addr, body.encode(encode))
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err
    finally:
        smtp.quit()

if __name__ == "__main__":
    from_addr = "mail"
    to_addr = "mail"
    subject = "Тестовое письмо от Python."
    text = "Отправкой почты управляет Python!"
    send_email(from_addr, to_addr, subject, text)