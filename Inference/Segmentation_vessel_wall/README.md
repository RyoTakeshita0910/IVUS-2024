# 血管壁の領域抽出
## 血管壁領域のIVUS画像の生成：LMW_to_IBIVUS_input.py
深層学習で出力した画像から血管壁領域のIVUS画像を生成する
### 実行方法
```bash
python LMW_to_IBIVUS_input.py --lumen_dir ~/path/lumen --media_dir ~/path/media --wire_dir ~/path/wire --img_dir ~path/IVUS --dest_dir ~path/output
```
### 動作
1. Lumen, Media, Wireに大津の二値化とラベル削除を施し、マスク画像を生成・保存<br>
2. Lumen, Media, Wireから血管壁のマスク画像を生成<br>
3. IVUS画像に血管壁のマスク画像を適用し，血管壁のIVUS画像を生成・保存<br>

### 結果例
・Lumen, Media, Wireの二値化画像とマスク画像が保存される<br>
・血管壁領域のIVUS画像が保存される<br>
|![0001_03492907_000001](https://github.com/RyoTakeshita0910/IVUS-2024/assets/104045526/eee15330-a28e-4379-b763-0d5e475d7c73)|![0001_03492907_000001](https://github.com/RyoTakeshita0910/IVUS-2024/assets/104045526/78de4974-b3d3-4492-a486-2dca4b6491e2)|![0001_03492907_000001](https://github.com/RyoTakeshita0910/IVUS-2024/assets/104045526/21cde1f7-4a18-4969-a108-a844213d05fe)|![0001_03492907_000001](https://github.com/RyoTakeshita0910/IVUS-2024/assets/104045526/5a9bf9b6-1a79-492d-bea6-4c3a86ee42b1)|
|---|---|---|---|
|Lumen|Media|Wire|IB-IVUS_input|

<br>
============================================================================================
<br>

## 各領域の抽出精度の評価：eval_pred_LMW.py
深層学習で出力した各領域のマスク画像の抽出精度を評価する
### 実行方法
```bash
python eval_pred_LMW.py --eval_dir ~/path/prediction/mask --gt_dir ~/path/ground-truth/mask --out_csv ~/path/output/csv
```
### 動作
1. LMW_to_IBIVUS_iput.pyで生成したLumenやMediaやWireのマスク画像と正解のマスク画像を読み込む<br>
2. Jaccard係数とHausdorff距離の計算<br>
3. 計算結果をcsvで出力<br>


### 結果例
・csvに各画像のJaccard係数とHausdorff距離の計算結果が保存される
|img_name|IoU|Hausdorff_distance|
|---|---|---|
|0001_03492907_000001|0.928185999|5.656854249|
|0001_03492907_000061|0.893295109|8|
|0001_03492907_000121|0.879259348|8.94427191|
|0001_03492907_000181|0.918669999|8.602325267|
|...|...|...|
|ave|...|...|

