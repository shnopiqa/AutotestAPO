import requests
import pytest


class TestUserAuth:


    exclude_params = [
        ("no_cookie"),
        ("no_token")

    ]

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        print(response1.text)

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is not CSRF token header in the response"
        assert "user_id" in response1.json(), "THere is no user id in the response"

        auth_sid = response1.cookies.get("auth_sid")
        print(auth_sid)
        token = response1.headers.get("x-csrf-token")
        print(token)

        if condition == "no_cookie":
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={'x-csrf-token':token}
            )
            print(response2.text)
        else:
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={'auth_sid': auth_sid}
            )
            print(response2.text)
        assert "user_id" in response1.json(), "There is no user id in the second response"

        user_id_from_check_method = response2.json()["user_id"]

        print(user_id_from_check_method)

        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"
