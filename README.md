# デュエルマスターズ AR配信アプリ

スマホカメラでカードを認識し、AR空間にキャラクターを投影するアプリケーション。

## 開発フェーズ

- **Phase 1**: データ収集 & カード認識（YOLOv8 OBB）
- **Phase 2**: FlutterからAPI連携
- **Phase 3**: AR投影（2Dキャラ）
- **Phase 4**: タップ検出 & アニメーション
- **Phase 5**: YouTube配信対応

## プロジェクト構造

```
dm-ar/
├── backend/           # FastAPI + YOLOv8推論
├── data/              # データセット
│   ├── raw/           # 元画像
│   ├── annotations/   # アノテーションファイル
│   └── processed/     # 前処理済みデータセット
├── models/            # 学習済みモデル
├── scripts/           # ユーティリティスクリプト
└── README.md          # このファイル
```

## Phase 1 実装予定

1. **スクレイピング** - デュエルマスターズカード画像の収集
2. **アノテーション** - Roboflowでバウンディングボックスラベル付け
3. **YOLOv8 OBB学習** - 回転角を含めたカード検出モデルの訓練

## 技術スタック

| 用途 | 技術 |
|------|------|
| カード認識 | YOLOv8 OBB |
| バックエンド | Python + FastAPI |
| フロントエンド | Flutter |
| AR | ar_flutter_plugin（ARCore/ARKit） |
| アノテーション | Roboflow |
| 3Dモデル | glTF（余裕があれば） |

## セットアップ

```bash
# Python依存ライブラリのインストール
pip install -r requirements.txt

# YOLOv8 OBBで訓練
python backend/train.py

# 推論テスト
python backend/inference.py
```
# dm-ar
