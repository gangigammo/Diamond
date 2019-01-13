"""
Userのふるまいのテスト
"""
from django.test import TestCase


from financial.models import User
from financial.models.objects import Users


class UserModelTest(TestCase):
    def test_main(self):
        testname = "username"
        testpass = "password"
        user = User(name=testname, password=testpass)

        if user.name != testname:
            raise AssertionError("User.nameをインスタンスに保持できていません")

        print("User.passwordの表現は %s です。平文ではありませんか？" % user.password)

        try:
            user.save()
        except Exception as ex:
            print("Userをデータベースに保存できませんでした")
            raise AssertionError(ex)
        print("userをデータベースに保存しました")
        print("Userモデルのテスト終了")


class UsersTest(TestCase):
    def test_main(self):
        if not Users.getFirst() is None:
            raise AssertionError("空のデータベースからUserを取得できてしまいました")

        testname = "username"
        testpass = "password"
        user = User(name=testname, password=testpass)
        user.save()
        print("userをデータベースに保存しました")

        gotuser = Users.getFirst()
        if gotuser is None:
            raise AssertionError("データベースからUserを取得できていません")

        if gotuser.name != testname:
            raise AssertionError("DBから取り出したUser.nameが異なります")
        if gotuser.password != user.password:
            raise AssertionError("DBから取り出したUser.passwordが異なります")

        print("Usersのテスト終了")
