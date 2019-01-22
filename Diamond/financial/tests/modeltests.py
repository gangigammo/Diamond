"""
データベース操作の複合テスト
"""
from django.test import TestCase

from financial.models import User, Balance, Category

import datetime

userDic1 = {
    "name": "Taro",
    "password": "password"
}
userDic2 = {
    "name": "KusoMan",
    "password": "unkoUNCHI"
}

incateDic1 = {
    "isIncome": True,
    "name": "work"
}
excateDic1 = {
    "isIncome": False,
    "name": "food"
}

incomeDic1 = {
    "isIncome": True,
    "description": "Nobel",
    "amount": 50000000,
    "date": datetime.date.today(),
}
expenseDic1 = {
    "isIncome": False,
    "description": "house",
    "amount": 7770000,
    "date": datetime.date.today(),
}


class DeleteTest(TestCase):
    def test_main(self):
        # サインアップ
        User.new(**userDic1).save()

        # ログイン
        user = User.objects.filter(name=userDic1["name"]).first()
        if user is None:
            raise AssertionError("ユーザーが見つかりません")
        # パスワード認証
        iscorrect = user.isCorrect(password=userDic1["password"])
        if not iscorrect:
            raise AssertionError("パスワードが認証できません")

        print("OK: ユーザーの登録・認証")
        if user.password == userDic1["password"]:
            print("WARN: パスワードが平文です!!!!!!!!!!!")

        # 収支登録
        Balance(writer=user, **incomeDic1).save()

        income = Balance.objects.filter().first()
        if income is None:
            raise AssertionError("収支を取得できません")

        if income.category:
            raise AssertionError("収入 %s のカテゴリが勝手にセットされます" % income)

        income = Balance.objects.filter(isIncome=True).first()
        if income is None:
            raise AssertionError("収入を取得できません")

        expense = Balance.objects.filter(isIncome=False).first()
        if expense:
            raise AssertionError("支出 %s を収入として取得しました" % expense)

        Balance(writer=user, **expenseDic1).save()
        expense = Balance.objects.filter(isIncome=False).first()
        if expense is None:
            raise AssertionError("支出を取得できません")

        income.delete()
        income = Balance.objects.filter(isIncome=True).first()
        if income:
            raise AssertionError("収入 %s を削除できません" % income)

        print("OK: 収支の登録・削除")

        # カテゴリ登録
        Category(writer=user, **incateDic1).save()

        incate = Category.objects.filter().first()
        if incate is None:
            raise AssertionError("カテゴリを取得できません")
        incate = Category.objects.filter(isIncome=True).first()
        if incate is None:
            raise AssertionError("収入カテゴリを取得できません")
        excate = Category.objects.filter(isIncome=False).first()
        if excate:
            raise AssertionError("収入カテゴリ %s を支出カテゴリとして取得しました", excate)

        Category(writer=user, **excateDic1).save()
        excate = Category.objects.filter(isIncome=False).first()
        if excate is None:
            raise AssertionError("支出カテゴリを取得できません")

        print("OK: カテゴリの登録")

        # カテゴリ削除機能
        Balance.objects.all().delete()
        if Balance.objects.filter().first():
            raise AssertionError("収支を全削除できません")
        Balance(writer=user, category=incate, **incomeDic1).save()
        incate.delete()
        if Category.objects.filter(isIncome=True).first():
            raise AssertionError("収入カテゴリを削除できません")
        income = Balance.objects.filter().first()
        if income is None:
            raise AssertionError("収入 %s がカテゴリ削除と連動して削除されました" % income)
        if income.category:
            raise AssertionError("収入 %s が、削除されたカテゴリに属しています", income)

        print("OK: カテゴリの削除")

        # ユーザー削除機能
        Category(writer=user, **incateDic1).save()
        user.delete()
        cate = Category.objects.filter().first()
        if cate:
            raise AssertionError("削除されたユーザーのカテゴリ %s がDB上に残っています", cate)
        bala = Balance.objects.filter().first()
        if bala:
            raise AssertionError("削除されたユーザーの収支 %s がDB上に残っています", bala)

        User.new(**userDic1).save()
        User.new(**userDic2).save()
        user1 = User.objects.filter(name=userDic1["name"]).first()
        user2 = User.objects.filter(name=userDic2["name"]).first()
        users = User.objects.all()
        if userDic1["name"] == userDic2["name"]:
            raise AssertionError("テストがおかしいです")
        if users.count() != 2:
            raise AssertionError("複数ユーザーの追加ができません")
        if user1.name != userDic1["name"] or user2.name != userDic2["name"]:
            raise AssertionError("getFirstでユーザーを正しく取得できません")

        Category(writer=user1, **excateDic1).save()
        Balance(writer=user1, **expenseDic1).save()

        Category(writer=user2, **incateDic1).save()
        Balance(writer=user2, **incomeDic1).save()

        print("  %s の削除前" % user1)
        cate = Category.objects.filter(writer=user1).first()
        bala = Balance.objects.filter(writer=user1).first()
        print("    %s has %s, %s" % (user1, cate, bala))
        cate = Category.objects.filter(writer=user2).first()
        bala = Balance.objects.filter(writer=user2).first()
        print("    %s has %s, %s" % (user2, cate, bala))

        user1.delete()

        print("  %s の削除後" % user1)
        cate = Category.objects.filter(writer=user1).first()
        bala = Balance.objects.filter(writer=user1).first()
        print("    %s has %s, %s" % (user1, cate, bala))
        cate = Category.objects.filter(writer=user2).first()
        bala = Balance.objects.filter(writer=user2).first()
        print("    %s has %s, %s" % (user2, cate, bala))
        if cate is None:
            raise AssertionError("他ユーザーの退会によってカテゴリが消えてしまいました")
        if bala is None:
            raise AssertionError("他ユーザーの退会によって収支が消えてしまいました")

        print("OK: ユーザー退会による自動削除テスト")
