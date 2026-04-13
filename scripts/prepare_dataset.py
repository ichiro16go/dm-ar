"""
YOLOv8 OBB用のデータセット準備スクリプト
Roboflowからエクスポートしたデータセットを、YOLOv8が理解できる形式に変換
"""

from pathlib import Path
import argparse
import json
from typing import List, Dict
import shutil


def create_dataset_yaml(output_dir: str, num_classes: int = 1) -> str:
    """
    YOLOv8用のdata.yamlを作成
    
    Args:
        output_dir: 出力ディレクトリ
        num_classes: クラス数
        
    Returns:
        data.yaml のパス
    """
    
    output_path = Path(output_dir) / "data.yaml"
    
    yaml_content = f"""path: {Path(output_dir).resolve()}
train: images/train
val: images/val
test: images/test

nc: {num_classes}
names: ['card']
"""
    
    with open(output_path, "w") as f:
        f.write(yaml_content)
    
    print(f"✅ data.yaml を作成: {output_path}")
    return str(output_path)


def organize_roboflow_export(
    roboflow_export_dir: str,
    output_dir: str = "data/processed",
) -> str:
    """
    Roboflowからエクスポートしたデータセットを整理
    
    Args:
        roboflow_export_dir: Roboflowエクスポートディレクトリ
        output_dir: 出力ディレクトリ
        
    Returns:
        処理後のディレクトリ
    """
    
    roboflow_path = Path(roboflow_export_dir)
    output_path = Path(output_dir)
    
    if not roboflow_path.exists():
        raise FileNotFoundError(f"Roboflow export directory not found: {roboflow_path}")
    
    # 出力ディレクトリを作成
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 画像とアノテーションを整理
    for split in ["train", "val", "test"]:
        src_image_dir = roboflow_path / split / "images"
        src_anno_dir = roboflow_path / split / "labels"
        
        dst_image_dir = output_path / "images" / split
        dst_anno_dir = output_path / "labels" / split
        
        if src_image_dir.exists():
            dst_image_dir.mkdir(parents=True, exist_ok=True)
            for image_file in src_image_dir.glob("*"):
                shutil.copy(image_file, dst_image_dir / image_file.name)
            print(f"✅ {split} 画像をコピー: {len(list(dst_image_dir.glob('*')))}個")
        
        if src_anno_dir.exists():
            dst_anno_dir.mkdir(parents=True, exist_ok=True)
            for anno_file in src_anno_dir.glob("*"):
                shutil.copy(anno_file, dst_anno_dir / anno_file.name)
            print(f"✅ {split} アノテーションをコピー: {len(list(dst_anno_dir.glob('*')))}個")
    
    # data.yamlを作成
    create_dataset_yaml(str(output_path))
    
    print(f"✅ データセット準備完了: {output_path}")
    return str(output_path)


def validate_dataset(dataset_dir: str) -> bool:
    """
    データセットの構造を検証
    
    Args:
        dataset_dir: データセットディレクトリ
        
    Returns:
        検証結果（True=OK）
    """
    
    dataset_path = Path(dataset_dir)
    required_dirs = [
        "images/train", "images/val", "images/test",
        "labels/train", "labels/val", "labels/test",
    ]
    
    all_exist = True
    for req_dir in required_dirs:
        dir_path = dataset_path / req_dir
        if not dir_path.exists():
            print(f"❌ ディレクトリが見つかりません: {dir_path}")
            all_exist = False
        else:
            file_count = len(list(dir_path.glob("*")))
            print(f"✅ {req_dir}: {file_count}ファイル")
    
    # data.yamlの確認
    if (dataset_path / "data.yaml").exists():
        print(f"✅ data.yaml が存在します")
    else:
        print(f"❌ data.yaml が見つかりません")
        all_exist = False
    
    return all_exist


def main():
    parser = argparse.ArgumentParser(
        description="Roboflowエクスポートを YOLOv8 OBB用に準備"
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Roboflowエクスポートディレクトリ",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed",
        help="出力ディレクトリ",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="準備後にデータセットを検証",
    )
    
    args = parser.parse_args()
    
    # データセット準備
    output_dir = organize_roboflow_export(args.source, args.output)
    
    # 検証
    if args.validate:
        print("\n📊 データセット検証中...")
        is_valid = validate_dataset(output_dir)
        if is_valid:
            print("✅ データセットは有効です")
        else:
            print("❌ データセットに問題があります")


if __name__ == "__main__":
    main()
