from django.core.mail import send_mail


class Util:
    @staticmethod
    def send_mail(address, confirmation_code):
        """Метод отправки email сообщений."""

        send_mail(
            "YAmdb confirmation code",
            confirmation_code,
            "yamdb@yandex.ru",
            [address]
        )
