from random import randint

from Accounting import models


def request_send_verify_sms(user):
    if models.User.object.filter(username=user.username).exists():
        user = models.User.object.get(username=user.username)
        verification_code = str(randint(10000, 99999))

        print(verification_code)

        """ SMS Services """

        response = {'status': 200}

        # Check sending SMS
        if response['status'] == 200:
            user.verification_code = verification_code
            user.save()
        else:
            print("Error sending SMS")
