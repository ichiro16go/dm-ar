#!/usr/bin/env python3
"""
セットアップ確認スクリプト
実行: python scripts/check_environment.py
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Python バージョン確認"""
    print("🐍 Python バージョン:")
    version = sys.version.split()[0]
    print(f"   {version}")
    if sys.version_info >= (3, 8):
        print("   ✅ OK")
        return True
    else:
        print("   ❌ 3.8 以上が必要です")
        return False


def check_package(package_name, import_name=None):
    """パッケージがインストール済みか確認"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"   ✅ {package_name}")
        return True
    except ImportError:
        print(f"   ❌ {package_name} (未インストール)")
        return False


def check_required_packages():
    """必須パッケージ確認"""
    print("\n📦 必須パッケージ:")
    packages = [
        ("ultralytics", "ultralytics"),
        ("torch", "torch"),
        ("opencv", "cv2"),
        ("numpy", "numpy"),
        ("fastapi", "fastapi"),
        ("pandas", "pandas"),
    ]
    
    results = []
    for package_name, import_name in packages:
        results.append(check_package(package_name, import_name))
    
    return all(results)


def check_venv():
    """仮想環境が有効か確認"""
    print("\n🔧 仮想環境:")
    if hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    ):
        print(f"   ✅ 有効")
        print(f"   パス: {sys.prefix}")
        return True
    else:
        print("   ❌ 仮想環境が有効でない")
        print("   実行: source venv/bin/activate")
        return False


def check_cuda():
    """CUDA（GPU）サポート確認"""
    print("\n🖥️  GPU サポート:")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"   ✅ CUDA 有効")
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print("   ⚠️  CUDA なし（CPU のみで動作）")
            return False
    except ImportError:
        print("   ❌ PyTorch が見つかりません")
        return False


def check_file_structure():
    """ファイル構造確認"""
    print("\n📁 ファイル構造:")
    required_dirs = [
        "backend",
        "data",
        "models",
        "scripts",
        "docs",
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        path = Path(dir_name)
        if path.exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ (見つかりません)")
            all_exist = False
    
    # ファイルチェック
    required_files = [
        "backend/train.py",
        "backend/inference.py",
        "backend/config.yaml",
        "requirements.txt",
        "README.md",
    ]
    
    for file_name in required_files:
        path = Path(file_name)
        if path.exists():
            print(f"   ✅ {file_name}")
        else:
            print(f"   ❌ {file_name} (見つかりません)")
            all_exist = False
    
    return all_exist


def main():
    print("=" * 50)
    print("🔍 dm-ar 環境確認スクリプト")
    print("=" * 50)
    
    checks = [
        ("Python バージョン", check_python_version),
        ("仮想環境", check_venv),
        ("必須パッケージ", check_required_packages),
        ("GPU サポート", check_cuda),
        ("ファイル構造", check_file_structure),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"⚠️  {check_name} 確認エラー: {e}")
            results.append(False)
    
    # 最終結果
    print("\n" + "=" * 50)
    
    # 重要なチェック（GPU 以外）
    # results = [python, venv, packages, cuda, file_structure]
    critical_results = [results[0], results[1], results[2], results[4]]
    
    if all(critical_results):
        print("✅ 環境セットアップ完了！")
        print("\n📝 注意:")
        print("- GPU (CUDA) は設定されていません")
        print("  → CPUで訓練実行可能（時間は長くなります）")
        print("  → GPU が必要な場合: pytorch公式サイトで cuda-enabled torch をインストール")
        print("\n🚀 次のステップ:")
        print("1. Roboflow でカード画像をアップロード")
        print("   → https://roboflow.com/")
        print("2. YOLOv8 (OBB) 形式でエクスポート")
        print("3. python scripts/prepare_dataset.py でデータセット準備")
        print("4. python backend/train.py で訓練開始")
        print("\n📚 ドキュメント:")
        print("- docs/SETUP_GUIDE.md           ← 仮想環境の使い方")
        print("- docs/MACHINE_LEARNING_BASICS.md ← 機械学習の基本")
        print("- docs/PHASE1_WORKFLOW.md       ← Phase 1 の進め方")
        print("- docs/COMMAND_QUICK_REFERENCE.md ← よく使うコマンド")
        return 0
    else:
        print("❌ セットアップに問題があります")
        print("\n実行コマンド:")
        print("$ source venv/bin/activate")
        print("$ pip install -r requirements.txt")
        print("$ python scripts/check_environment.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
