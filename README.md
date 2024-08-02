使い方（一通り読んでから作るのをおすすめします）：
➀右上の「<> Code ▿」（緑色）をクリック
➁（「HTTPS」タブの）「Download ZIP」をクリック
➂ダウンロードされたZIPフォルダをすべて展開する（展開する場所は基本的にどこでもいい）
➃展開したフォルダに、「font」フォルダを作成
➄「C:\Windows\Fonts」から、日本語に対応したフォントをコピーして、➃で作ったフォルダ内にペースト。テストで使ったフォント以外を使用するときは、「main_game.py」の中の「japanese_font_path」の設定を変える。
　　（テストでは、「BIZ UDゴシック」を使用。ペーストすると「BIZ-UDGothicB.ttc」と「BIZ-UDGothicR.ttc」ができる。）
➅「main_game.py」を実行する。
　　AIの推論をする上で、「動作環境.txt」に入っているライブラリが必要。
　　コマンドプロンプトで、「pip install -r requirements.txt」を実行（requirements.txtの中身を読み取ってインストールする）
