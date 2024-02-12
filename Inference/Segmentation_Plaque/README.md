# プラーク成分の領域分割
## IB-IVUS画像の生成：make_IBIVS.py
深層学習から出力された各プラーク成分のマスク画像からIB-IVUS画像を生成する
### 実行方法
```bash
python make_IB_IVUS.py --input_dir ~/path/all/plaque/mask --lumen_dir ~/path/lumen/mask --media_dir ~/path/media/mask --wire_dir ~/path/wire/mask --dest_dir ~path/output
```
### 動作の処理
1. 各プラーク成分のマスク画像における画素値が高いプラークを優先して、全てのプラーク成分を統合
2. Lumen, Mediaマスク画像から血管壁の輪郭を抽出
3. Lumen, Media, Wireから血管壁の領域を特定し、範囲外を背景に設定
4. 血管壁の範囲内において色のないピクセルについて、周囲から色を特定
5. 1~4の結果を統合してIB-IVUS画像を生成


