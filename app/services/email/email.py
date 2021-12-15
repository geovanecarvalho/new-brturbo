from dynaconf import settings
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content


def enviar_email(email, subject, body):

    sg = sendgrid.SendGridAPIClient(settings.SEND_GRID_CLIENT_KEY)
    from_email = Email(settings.EMAIL_SEND_GRID)
    to_email = To(email)
    subject = subject
    content = Content("text/html", body)
    mail = Mail(from_email, to_email, subject, content)

    mail_json = mail.get()

    response = sg.client.mail.send.post(request_body=mail_json)
    return response


def email_token(token):
    html = f"""
<html>
<body style="margin: 0; padding: 0;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
        <tr>
            <td align="center" bgcolor="#001d36" style="padding: 40px 0 30px 0;">
                <img src="https://www.brturboarena.com/wp-content/uploads/2021/06/BrTurbo-logo-horizontal-1024x722.png"
                    alt="Criando Mágica de E-mail" width="300" height="230" style="display: block;" />

                <h2 style="color: #3ab54b;">TOKEN DE ACESSO</h2>
                <h2 style="color: #fdba12">{token}</h2>
            </td>
        </tr>

        <tr>
            <td align="center" bgcolor="#fdba12" style="padding: 5px 0 5px 0;">
                <h1 style="color: #3ab54b"><b></b></h1>

            </td>

        </tr>
    </table>
</body>
</html>
    """
    return html


def email_new_password(url):
    html = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Redefinir Senha</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
       
    </head>

    <body style="margin: 0; padding: 0;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
            <tr>
                <td align="center" bgcolor="#001d36" style="padding: 40px 0 30px 0;">
                    <img src="https://www.brturboarena.com/wp-content/uploads/2021/06/BrTurbo-logo-horizontal-1024x722.png"
                        alt="Criando Mágica de E-mail" width="300" height="230" style="display: block;" />

                    <h2 style="color: #3ab54b;">REDEFINIÇÂO DE SENHA</h2>
                    <a href="#" style="background-color: #3ab54b;
                padding: 10px;
                text-decoration: none;
                border-radius: 2%;
                color: #000;
                font-weight: bolder;>click aqui para confirmar</a>
                </td>
            </tr>
            <tr>
                <td align="center" bgcolor="#fdba12" style="padding: 5px 0 5px 0;">
                    <h1 style="color: #3ab54b"><b></b></h1>

                </td>
            </tr>
        </table>
    </body>
</html>
    """.format(
        url
    )
    return html
