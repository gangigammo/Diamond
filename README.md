# Diamond
<img width="1419" alt="スクリーンショット 2020-07-13 1 20 44" src="https://user-images.githubusercontent.com/42495978/87251503-2c4c4580-c4a7-11ea-806b-9d7d1d0f5f26.png">
収支計算アプリ「金剛会計」をDjangoを用いて作成  
python3.7以上推奨(python3.6では収支編集機能などが動作せず)  
必要なパッケージはrequirements.txtに記述  

# 各ブランチの説明
| ブランチ名 | 役割 |
|:-----------|:------------:|
| master | 各人が開発した機能を統合したもの |
| deploy | nginxサーバーにデプロイするためにDebug機能をオフにして各種設定ファイルを置いたもの |
| deploy-GPT | deployブランチにお遊び機能を加えたもの |
| それ以外 | 各人の開発用ブランチ |

# 機能説明
ユーザーはアカウントを登録し、収支を記録できる。収支は金額、内容、カテゴリー、日付を要素に持つ。ユーザーは収支を円グラフ、折れ線グラフで視覚化できる。
そんな家計簿みたいなアプリケーション。

# 動かし方

pipでrequirements.txtのパッケージを取得

```
pip install -r requirements.txt
```
以下のコマンドで8000番ポートを使って開発用サーバーを起動

```
python manage.py runserver 8000
```

以下のコマンドでデータベースの作成  
modelを変更した際はmigrationsディレクトリの __\_\_init\_\_.py以外__
のファイルを削除してから行う

```
python manage.py makemigrations
python manage.py migrate
```
