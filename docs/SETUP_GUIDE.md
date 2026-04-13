# 環境セットアップガイド

## Python 仮想環境（venv）について

### 何をするのか？
仮想環境は、プロジェクトごとに独立した**Pythonと依存ライブラリの隔離されたスペース**を作ります。

- ❌ せず：全体のPythonを使う → 異なるプロジェクトで依存バージョンが衝突することがある
- ✅ 仮想環境を使用：プロジェクトA用と プロジェクトB用を完全に分離

### よく使うコマンド

```bash
# 1. 仮想環境の作成（初回のみ）
python3 -m venv venv

# 2. 仮想環境を有効化（毎回このプロジェクトで作業するときに実行）
source venv/bin/activate  # Linux/WSL
# または
venv\Scripts\activate  # Windows

# 3. パッケージをインストール
pip install -r requirements.txt

# 4. インストール済みパッケージを確認
pip list

# 5. 仮想環境を終了
deactivate
```

### 確認方法
```bash
# 仮想環境が有効になっているか確認
# ターミナルの行頭に (venv) と表示されていればOK

(venv) ichiro16go@laptop:~/dev/self/dm-ar$ 
                ↑
            ここに表示
```

---

## requirements.txt について

### 何？
プロジェクトに必要な**全Pythonパッケージのリスト**です。

```
ultralytics>=8.0.0    # YOLOv8本体
torch>=1.8.0          # 深層学習フレームワーク
opencv-python>=4.8.0  # 画像処理
fastapi>=0.104.0      # API用フレームワーク
...
```

### なぜ必要？
- 他の人がこのプロジェクトを実行する時 `pip install -r requirements.txt` で同じ環境が再現できる
- チームメンバーが全員同じバージョンで開発できる

### 新しいパッケージを追加する場合

```bash
# 1. インストール
pip install 新しいパッケージ名

# 2. requirements.txtに追加記録
pip freeze > requirements.txt

# 3. 確認 & コミット
cat requirements.txt
git add requirements.txt && git commit -m "Add new package"
```

---

## トラブルシューティング

### ケース1: "pip: command not found"
仮想環境が有効になっていません。
```bash
source venv/bin/activate  # まず有効化
pip install -r requirements.txt
```

### ケース2: "ModuleNotFoundError"
パッケージがインストールされていません。
```bash
pip install 足りないパッケージ名
# または
pip install -r requirements.txt
```

### ケース3: Windows/WSL間で混乱している
Windows側の Python を使う代わりに、**WSL側の Python** で統一してください。
```bash
which python3  # WSL内の Python の場所を確認
/usr/bin/python3  # ← これなら OK
```

---

## 次のステップ

仮想環境が有効な状態で進めてください：

```bash
# 1. 仮想環境の有効化
source venv/bin/activate

# 2. YOLOv8の訓練準備（データセット必要）
python backend/train.py --data backend/config.yaml

# 3. 推論テスト
python backend/inference.py --image path/to/image.jpg
```
