# Phase 1 実装ワークフロー

## やること（ステップバイステップ）

### ステップ 1️⃣: Roboflowアカウント作成 & データセット準備

```bash
# 1. Roboflow に登録
# https://roboflow.com/ へアクセス
# 🎬 YouTube で「Roboflow YOLOv8」と検索で手順が見つかります

# 2. 新しいプロジェクト作成
# - Project Name: "dm-ar-cards"
# - Object Detection
# - YOLOv8 (OBB)

# 3. 画像をアップロード
# - フォルダ: data/raw に約 100～200 枚のカード画像を配置
# - Roboflow にアップロード

# 4. アノテーション（ラベル付け）
# - 各画像でカードの範囲を OBB（回転バウンディングボックス）でマーク
# - 重要: 回転角度も正確にマーク
```

```
💡 ヒント: 最初は有名カード 5 種類×20 枚 = 100 枚程度でスタート
   慣れてから増やしていくのがおすすめ
```

### ステップ 2️⃣: データセットをエクスポート

```bash
# 1. Roboflow ダッシュボードから下記を設定
# - Format: YOLOv8 (OBB mode)
# - Classes: "card" (1 クラスのみ)
# - Auto-Orient: Yes
# - Augmentation: No (後で手動で設定)

# 2. YOLOv8 用フォーマットで download
# → ローカルに ZIP ファイルがダウンロードされる
```

### ステップ 3️⃣: ダウンロードしたデータセットを準備

```bash
# 1. ダウンロード ZIP を解凍
unzip /path/to/dm-ar-cards-dataset.zip -d ~/Downloads/

# 2. データセットを標準形式に整理
cd ~/dev/self/dm-ar
source venv/bin/activate  # 仮想環境有効化

python scripts/prepare_dataset.py \
    --source ~/Downloads/dm-ar-cards-dataset \
    --output data/processed \
    --validate

# 3. 確認メッセージ
# ✅ データセット準備完了: data/processed
# ✅ train images: 80ファイル
# ✅ val images: 10ファイル
# ✅ test images: 10ファイル
```

### ステップ 4️⃣: YOLOv8 で訓練

```bash
# 仮想環境を有効化
source venv/bin/activate

# 訓練スタート
python backend/train.py \
    --data backend/config.yaml \
    --device 0

# 🚀 訓練開始！
# 進捗が表示されます
# └─ Epoch 1/100
# │  ├─ Images: 80/80 ✅
# │  ├─ Loss: 0.654
# │  └─ mAP: 0.42
# └─ Epoch 2/100
#    ...
```

```
⏱️ 訓練時間の目安:
- GPU あり: 1～2 時間
- GPU なし (CPU): 8～12 時間
- WSL GPU: CUDA がセットアップできれば高速

💡 NVIDIA GPU を持ってれば、下記でセットアップ:
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### ステップ 5️⃣: 訓練結果の確認

```bash
# 訓練が完了したら
# models/card_detector/ に最適なモデルが保存される

ls -la models/card_detector/weights/
# ├── best.pt         ← テストデータで最も良い結果
# ├── last.pt         ← 最後のエポック
# └── ...

# 📊 訓練結果の可視化（内部ディレクトリに保存）
# models/card_detector/results/
# ├── results.csv     ← 全エポックの数値
# ├── confusion_matrix.png
# ├── F1_curve.png
# ├── PR_curve.png
# └── ...
```

### ステップ 6️⃣: 推論テスト

```bash
# テスト画像で推論を試す
source venv/bin/activate

python backend/inference.py \
    --model models/card_detector/weights/best.pt \
    --image path/to/test_card.jpg \
    --output detected_card.jpg

# 出力: 
# ✅ 検出結果を保存: detected_card.jpg
# 📊 検出されたカード: 3個

# detected_card.jpg を開いて確認
# (カード周りに緑の枠が付いていれば成功！)
```

---

## トラブルシューティング

### Q: "No module named 'ultralytics'"
```bash
# A: 仮想環境が有効でない
source venv/bin/activate
pip install ultralytics
```

### Q: "CUDA out of memory"
```bash
# A: GPU メモリ不足
# 対策: backend/config.yaml の batch サイズを減らす
batch: 4  # (デフォルト 16 から減らす)
```

### Q: "訓練が遅い"
```bash
# A: 複数の原因が考えられます
# 1. CPU だけで動いている
#    → GPU の CUDA 設定: pip install torch --index-url ...

# 2. バッチサイズが大きすぎる
#    → backend/config.yaml の batch を減らす

# 3. データセットが大きすぎる
#    → imgsz: 640 を 416 に減らす
```

### Q: "精度が 50% 以下"
```bash
# A: よくあります！原因の確認:
# 1. データセットが小さい？
#    → 各クラス 100+ 枚を目指す

# 2. アノテーションが雑？
#    → Roboflow で厳密にラベル付けを再確認

# 3. エポック数が少ない？
#    → 100→200 に増やす
#    → ただし過学習に注意

# 4. 多様性が足りない？
#    → 異なる角度・照明でデータ拡張
```

---

## チェックリスト

- [ ] 仮想環境が有効 (`(venv)` がターミナルに表示)
- [ ] `pip list` で ultralytics が表示される
- [ ] Roboflow にプロジェクト作成完了
- [ ] 画像をアップロード＆アノテーション完了
- [ ] `prepare_dataset.py` で `data/processed` 作成完了
- [ ] `data/processed/data.yaml` が存在
- [ ] `backend/train.py` で訓練開始できる
- [ ] 訓練完了後 `models/card_detector/weights/best.pt` が存在
- [ ] `backend/inference.py` でテスト推論成功

---

## 次のフェーズへ

Phase 1 が完了（精度が 80% 以上）したら、Phase 2 へ進みます：
- Phase 2: Flutter と FastAPI の連携
- API 用サーバーの構築
- リアルタイム推論テスト
