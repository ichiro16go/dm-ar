"""
YOLOv8 OBBモデルでカード検出を訓練するスクリプト
実行前に data/processed に学習データがあることを確認してください
"""

from ultralytics import YOLO
import argparse
from pathlib import Path


def train_card_detection(data_config: str = "backend/config.yaml", device: int = 0):
    """
    YOLOv8 OBBでカード検出モデルを訓練
    
    Args:
        data_config: データセット設定ファイルのパス
        device: 使用するGPU ID（0でGPU, "cpu"でCPU）
    """
    
    print(f"🚀 YOLOv8 OBB カード検出モデルの訓練を開始します")
    print(f"📋 設定ファイル: {data_config}")
    print(f"🖥️  使用デバイス: {'GPU' if device != 'cpu' else 'CPU'}")
    
    # YOLOv8l-OBBモデルをロード
    model = YOLO("yolov8l-obb.pt")
    
    # 訓練実行
    results = model.train(
        data=data_config,
        epochs=100,
        imgsz=640,
        device=device,
        patience=20,  # Early stopping
        save=True,
        project="models",
        name="card_detector",
        plots=True,
        verbose=True,
    )
    
    print(f"✅ 訓練完了！")
    print(f"📊 結果: {results}")
    
    return model


def evaluate_model(model_path: str, data_config: str = "backend/config.yaml", device: int = 0):
    """
    訓練済みモデルを評価
    
    Args:
        model_path: モデルファイルのパス
        data_config: データセット設定ファイルのパス
        device: 使用するGPU ID
    """
    
    print(f"📊 モデルを評価中: {model_path}")
    model = YOLO(model_path)
    
    metrics = model.val(
        data=data_config,
        device=device,
    )
    
    print(f"✅ 評価完了")
    print(f"📈 評価結果: {metrics}")
    
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLOv8 OBB カード検出モデルの訓練")
    parser.add_argument(
        "--data",
        type=str,
        default="backend/config.yaml",
        help="データセット設定ファイル",
    )
    parser.add_argument(
        "--device",
        type=int,
        default=0,
        help="GPU ID（0でGPU, 'cpu'でCPU）",
    )
    parser.add_argument(
        "--eval",
        type=str,
        default=None,
        help="評価するモデルのパス（指定時は訓練をスキップ）",
    )
    
    args = parser.parse_args()
    
    if args.eval:
        evaluate_model(args.eval, args.data, args.device)
    else:
        train_card_detection(args.data, args.device)
