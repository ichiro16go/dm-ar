"""
YOLOv8 OBBモデルでカード検出を推論するスクリプト
"""

from ultralytics import YOLO
from pathlib import Path
import cv2
import argparse
from typing import List, Dict, Tuple
import json


class CardDetector:
    """YOLOv8 OBBを使用したカード検出器"""
    
    def __init__(self, model_path: str, device: int = 0):
        """
        Args:
            model_path: 学習済みモデルのパス
            device: 使用するGPU ID（0でGPU, 'cpu'でCPU）
        """
        self.model = YOLO(model_path)
        self.device = device
    
    def detect(
        self,
        image_path: str,
        conf_threshold: float = 0.5,
        iou_threshold: float = 0.5,
    ) -> Dict:
        """
        画像内のカードを検出
        
        Args:
            image_path: 入力画像のパス
            conf_threshold: 信頼度の閾値
            iou_threshold: IoU閾値
            
        Returns:
            検出結果の辞書
                - cards: 検出されたカード情報のリスト
                  - id: カードID
                  - bbox: バウンディングボックス [x1, y1, x2, y2]
                  - angle: 回転角（度）
                  - conf: 信頼度
                  - is_tapped: タップ状態（90度付近なら True）
                - image_size: [width, height]
        """
        
        # 推論実行
        results = self.model(
            image_path,
            device=self.device,
            conf=conf_threshold,
            iou=iou_threshold,
        )
        
        # 結果を辞書形式に変換
        detections = []
        result = results[0]  # 最初の画像の結果
        
        for i, box in enumerate(result.boxes):
            # OBBモデルの場合、回転角を含むbboxを取得
            xywh = box.xywh.cpu().numpy()[0]  # [x_center, y_center, width, height]
            angle = box.conf.cpu().numpy()[0]  # 回転角（OBB固有）
            conf = float(box.conf.cpu().numpy()[0])
            
            # 絶対座標のバウンディングボックスに変換
            x_center, y_center, width, height = xywh
            x1 = int(x_center - width / 2)
            y1 = int(y_center - height / 2)
            x2 = int(x_center + width / 2)
            y2 = int(y_center + height / 2)
            
            # タップ状態判定（±45度の範囲でタップ状態）
            is_tapped = (45 <= angle <= 135) or (225 <= angle <= 315)
            
            detection = {
                "id": i,
                "bbox": [x1, y1, x2, y2],
                "angle": float(angle),
                "conf": conf,
                "is_tapped": is_tapped,
            }
            detections.append(detection)
        
        return {
            "cards": detections,
            "image_size": list(result.orig_shape[:2][::-1]),  # [width, height]
        }
    
    def detect_and_save(
        self,
        image_path: str,
        output_path: str = None,
        conf_threshold: float = 0.5,
        iou_threshold: float = 0.5,
    ):
        """
        画像内のカードを検出し、結果を保存
        
        Args:
            image_path: 入力画像のパス
            output_path: 出力画像のパス（省略時は元画像のディレクトリに保存）
            conf_threshold: 信頼度の閾値
            iou_threshold: IoU閾値
        """
        
        # 検出実行
        detections = self.detect(image_path, conf_threshold, iou_threshold)
        
        # 画像を読み込み
        image = cv2.imread(image_path)
        h, w = image.shape[:2]
        
        # 検出結果を描画
        for card in detections["cards"]:
            x1, y1, x2, y2 = card["bbox"]
            angle = card["angle"]
            conf = card["conf"]
            is_tapped = card["is_tapped"]
            
            # バウンディングボックスを描画
            color = (0, 255, 0) if not is_tapped else (0, 0, 255)  # 緑 or 赤
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            
            # テキスト情報
            text = f"Tap: {is_tapped} | Ang: {angle:.1f}° | Conf: {conf:.2f}"
            cv2.putText(
                image,
                text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )
        
        # 出力パスの決定
        if output_path is None:
            input_path = Path(image_path)
            output_path = input_path.parent / f"detected_{input_path.name}"
        
        # 結果を保存
        cv2.imwrite(str(output_path), image)
        print(f"✅ 検出結果を保存: {output_path}")
        print(f"📊 検出されたカード: {len(detections['cards'])}個")
        
        return detections


def main():
    parser = argparse.ArgumentParser(description="YOLOv8 OBB カード検出推論")
    parser.add_argument(
        "--model",
        type=str,
        default="models/card_detector/weights/best.pt",
        help="訓練済みモデルのパス",
    )
    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="入力画像のパス",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="出力画像のパス",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.5,
        help="信頼度の閾値",
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.5,
        help="IoU閾値",
    )
    parser.add_argument(
        "--device",
        type=int,
        default=0,
        help="GPU ID",
    )
    
    args = parser.parse_args()
    
    # 検出器の初期化
    detector = CardDetector(args.model, args.device)
    
    # 推論実行
    detector.detect_and_save(
        args.image,
        args.output,
        conf_threshold=args.conf,
        iou_threshold=args.iou,
    )


if __name__ == "__main__":
    main()
