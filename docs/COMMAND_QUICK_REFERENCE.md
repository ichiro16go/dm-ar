# コマンドクイックリファレンス

## 毎回使うコマンド

```bash
# 🚀 プロジェクト開始時
cd ~/dev/self/dm-ar
source venv/bin/activate  # (venv) が表示されたら有効

# 📦 新しいパッケージをインストール
pip install パッケージ名
pip freeze | grep パッケージ名  # 確認

# 🧠 YOLOv8 訓練
python backend/train.py --data backend/config.yaml

# 🎯 推論テスト
python backend/inference.py --image ~/path/to/image.jpg

# 🛑 仮想環境を終了
deactivate
```

---

## 開発フロー

### 初回セットアップ（1回のみ）
```bash
cd ~/dev/self/dm-ar
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 日々の開発（毎回）
```bash
cd ~/dev/self/dm-ar
source venv/bin/activate
# ここで開発...
```

---

## Phase 1 ステップバイステップ

### Stage 1: データセット準備
```bash
# Roboflow から ZIP をダウンロード後
python scripts/prepare_dataset.py \
  --source ~/Downloads/dataset \
  --output data/processed \
  --validate
```

### Stage 2: 訓練実行
```bash
source venv/bin/activate
python backend/train.py --data backend/config.yaml
```

### Stage 3: 結果確認
```bash
ls -la models/card_detector/weights/best.pt
python backend/inference.py \
  --model models/card_detector/weights/best.pt \
  --image data/raw/test_card.jpg
```

---

## デバッグコマンド

```bash
# 仮想環境の状態確認
which python
python --version

# インストール済みパッケージ一覧
pip list

# 特定パッケージの情報
pip show ultralytics

# requirements.txt を更新（パッケージを追加した後）
pip freeze > requirements.txt

# 仮想環境を削除（リセット）
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ファイル/ディレクトリ構成

```
dm-ar/
├── backend/
│   ├── train.py           ← 訓練スクリプト
│   ├── inference.py       ← 推論スクリプト
│   └── config.yaml        ← YOLOv8設定
├── data/
│   ├── raw/               ← 元画像（Roboflow前）
│   ├── annotations/       ← アノテーション（Roboflow前）
│   └── processed/         ← YOLOv8用データセット（訓練用）
├── models/
│   └── card_detector/     ← 訓練済みモデル（訓練後に生成）
│       └── weights/
│           ├── best.pt    ← ← 最も重要！（これを推論で使う）
│           └── last.pt
├── scripts/
│   └── prepare_dataset.py ← データセット準備スクリプト
├── docs/
│   ├── SETUP_GUIDE.md                    ← この直下3つが学ぶべきドキュメント
│   ├── MACHINE_LEARNING_BASICS.md
│   ├── PHASE1_WORKFLOW.md
│   └── COMMAND_QUICK_REFERENCE.md        ← このファイル
├── requirements.txt
├── README.md
└── venv/                  ← 仮想環境（自動生成）
    ├── bin/
    │   ├── activate       ← このを実行してON/OFF
    │   ├── python
    │   └── pip
    ├── lib/
    └── ...
```

---

## 環境確認コマンド

```bash
# WSL 上のPythonか確認
which python3
# 出力: /usr/bin/python3 ← OK

# 仮想環境が有効か確認
(venv) $ echo $VIRTUAL_ENV
# 出力: /home/ichiro16go/dev/self/dm-ar/venv

# YOLOv8 がインストール済みか確認
python -c "import ultralytics; print(ultralytics.__version__)"
# 出力: 8.4.37 ← OK

# PyTorch（GPU対応）が有効か確認
python -c "import torch; print('CUDA:',torch.cuda.is_available())"
# 出力: CUDA: False  (WSLでCUDA未セットアップなら False でOK)
```

---

## よくあるエラーと対策

| エラー | 原因 | 対策 |
|--------|------|------|
| `ModuleNotFoundError: No module named 'ultralytics'` | 仮想環境未有効 | `source venv/bin/activate` |
| `bash: python: command not found` | python3 を python で実行 | `python3` コマンド使用 |
| `pip: Permission denied` | WSL/Windows混在 | `which pip` で確認 |
| `CUDA out of memory` | GPU メモリ不足 | batch サイズ減らす |
| `ImportError: libGL.so.1` | Linux グラフィックス依存 | `sudo apt install libgl1` |

---

## 参考：実行例

### 1️⃣ 初回セットアップ
```bash
$ cd ~/dev/self/dm-ar
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
Successfully installed pip-26.0.1
(venv) $ pip install -r requirements.txt
Collecting ultralytics>=8.0.0...
[トレンディングが数分間続く]
Successfully installed ultralytics-8.4.37 torch-2.1.1 ...
```

### 2️⃣ データセット準備
```bash
(venv) $ python scripts/prepare_dataset.py \
    --source ~/Downloads/dataset \
    --output data/processed \
    --validate
✅ train 画像をコピー: 80個
✅ val 画像をコピー: 10個
✅ test 画像をコピー: 10個
✅ data.yaml が存在します
✅ データセットは有効です
```

### 3️⃣ 訓練実行
```bash
(venv) $ python backend/train.py --data backend/config.yaml
🚀 YOLOv8 OBB カード検出モデルの訓練を開始します
📋 設定ファイル: backend/config.yaml
🖥️  使用デバイス: GPU
Epoch 1/100: ... Loss: 2.341 | mAP@0.5: 0.32
Epoch 2/100: ... Loss: 1.923 | mAP@0.5: 0.45
...
```

### 4️⃣ 推論テスト
```bash
(venv) $ python backend/inference.py \
    --model models/card_detector/weights/best.pt \
    --image test_card.jpg
✅ 検出結果を保存: detected_test_card.jpg
📊 検出されたカード: 3個
```

---

## 次のステップ

✅ **セットアップ完了**
- [ ] Phase 1: カード認識 (現在ここ)
- [ ] Phase 2: API 連携
- [ ] Phase 3: AR 投影
- [ ] Phase 4: アニメーション
- [ ] Phase 5: YouTube 配信対応
