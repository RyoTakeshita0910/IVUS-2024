# プラーク成分の領域分割
## IB-IVUS画像の生成：make_IBIVS.py
深層学習から出力された各プラーク成分のマスク画像からIB-IVUS画像を生成する
### 実行方法
```bash
python make_IB_IVUS.py --input_dir ~/path/all/plaque/mask --lumen_dir ~/path/lumen/mask --media_dir ~/path/media/mask --wire_dir ~/path/wire/mask --dest_dir ~path/output
```
### 動作
1. 各プラーク成分のマスク画像における画素値が高いプラークを優先して、全てのプラーク成分を統合<br>
2. Lumen, Mediaマスク画像から血管壁の輪郭を抽出<br>
3. Lumen, Media, Wireから血管壁の領域を特定し、範囲外を背景に設定<br>
4. 血管壁の範囲内において色のないピクセルについて、周囲から色を特定<br>
5. 1~4の結果を統合してIB-IVUS画像を生成<br>

<br>
====================================================================
<br>

## IB-IVUS画像のパッチ画像の作成とクラスの割り当て：make_patch_IBIVUS.py
正解のIB-IVUS画像と深層学習によって生成したIB-IVUS画像からパッチ画像を作成し，プラーク成分の分類精度の評価に用いる
### 実行方法
```bash
python make_patch_IBIVUS.py --img_dir ~/path/IB-IVUS --dest_dir ~/path/output --csv_name output csv file name
```

### 動作
1. IB-IVUS画像からパッチ画像を作成<br>
2. 生成したパッチ画像を背景クラスまたは、各プラーク成分のクラスへ割り当てる<br>
3. 全てのパッチ画像のクラスに関する情報をCSVに保存<br><br>

#### 上記の処理を正解のIB-IVUS画像と深層学習によって生成されたIB-IVUS画像の両方に適用する -> プラーク成分の分類精度評価に使用


<br>
====================================================================
<br>

## 生成したIB-IVUS画像のプラーク成分の分類精度評価：eval_patch_IBIVUS.py
make_patch_IBIVUS.pyで生成したcsvを元に、各プラーク成分の正解クラスと予測クラスの一致率を計算
### 実行方法
```bash
python eval_patch_IBIVUS.py --eval_csv ~/path/csv file/prediction --gt_csv ~/path/csv file/ground-truth --out_csv ~/path/csv file/output
```

### 動作
1. 予測したIB-IVUS画像と正解のIB-IVUS画像に関するパッチ画像のクラス分けの情報をcsvから読込<br>
2. 予測クラスと正解クラスの混同行列を作成<br>
3. 予測クラスと正解クラスの一致率を計算し、結果をcsvに保存<br>