"""
Userのふるまいのテスト
"""
from django.test import TestCase


from financial.models import User


class UserModelTest(TestCase):
    def test_main(self):
        testname = "username"
        testpass = "password"
        user = User.new(name=testname, password=testpass)

        if user.name != testname:
            raise AssertionError("User.nameをインスタンスに保持できていません")

        print("User.passwordの表現は %s です。平文かどうか確認してください" % user.password)

        try:
            user.save()
        except Exception as ex:
            print("Userをデータベースに保存できませんでした")
            raise AssertionError(ex)
        print("OK: Userモデルの基本テスト")


class UsersTest(TestCase):
    def test_main(self):
        if not User.objects.first() is None:
            raise AssertionError("空のデータベースからUserを取得できてしまいました")

        testname = "username"
        testpass = "password"
        user = User.new(name=testname, password=testpass)
        user.save()

        gotuser = User.objects.first()
        if gotuser is None:
            raise AssertionError("データベースからUserを取得できていません")

        if gotuser.name != testname:
            raise AssertionError("DBから取り出したUser.nameが異なります")
        if gotuser.password != user.password:
            raise AssertionError("DBから取り出したUser.passwordが異なります")

        print("OK: Userデータベースの基本テスト")
