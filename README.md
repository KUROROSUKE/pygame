## 使い方（一通り読んでから作るのをおすすめします）：  
  
**➀右上の「<> Code ▿」（緑色）をクリック**  
**➁**（「HTTPS」タブの）**「Download ZIP」をクリック**  
**➂ダウンロードされたZIPフォルダをすべて展開する**（展開する場所は基本的にどこでもいい）  
**➃展開したフォルダに、「font」フォルダを作成**  
**➄「C:\Windows\Fonts」から、日本語に対応したフォントをコピーして、➃で作ったフォルダ内にペースト**。  
　　テストで使ったフォント以外を使用するときは、「main_game.py」の中の「japanese_font_path」の設定を変える。  
　　（テストでは、「BIZ UDゴシック」を使用。ペーストすると「BIZ-UDGothicB.ttc」と「BIZ-UDGothicR.ttc」ができる。）  
**➅「main_game.py」を実行する。**  
　　**AIの推論をする上で、「動作環境.txt」に入っているライブラリが必要。**  
　　コマンドプロンプトで、「pip install -r requirements.txt」を実行（requirements.txtの中身を読み取ってインストールする）  
元ネタ：https://kurorosuke.github.io/atom_game/new_game/game.html  
↑これとの違い：tensorflowによってAIの推論を用いた。  
  
  

拡張する方法：  
➀新たな分子を作れるようにする（カードは8枚なので、原子の数が8以下の物）
  compound/standard.jsonの"material"に
          ...},　　←「,」から書き始める  
          {  
              "name": "分子の名前",　　←""はいる。  
              "formula": "分子の化学式",　　←これも""がいる  
              "point": ポイント数,　　←""はいらない。数字で入力  
              "components": {  
                  "必要な原子➀": 原子➀の数,　　←原子の種類だけ必要。最後の原子には「,」はいらない  
                  "必要な原子➁": 原子➁の数  
              }  
          }  
    を追加する  
➁フォントを変える  
　　「font」ディレクトリに日本語対応のフォントを入れる  
  　main_game.pyの「japanese_font_path」にそのフォントの相対パスを入れる（「font/フォントの名前」）  
