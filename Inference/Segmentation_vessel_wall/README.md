# 血管壁の領域抽出
## 血管壁領域のIVUS画像の生成：LMW_to_IBIVUS_input.py
深層学習で出力した画像から血管壁領域のIVUS画像を生成する
### 実行方法
```bash
python LMW_to_IBIVUS_input.py --lumen_dir ~/path/lumen --media_dir ~/path/media --wire_dir ~/path/wire --img_dir ~path/IVUS --dest_dir ~path/output
```
### 動作の処理
1. Lumen, Media, Wireに大津の二値化とラベル削除を施し、マスク画像を生成・保存<br>
2. Lumen, Media, Wireから血管壁のマスク画像を生成<br>
3. IVUS画像に血管壁のマスク画像を適用し，血管壁のIVUS画像を生成・保存<br>

<br>
====================================================================
<br>

## 各領域の抽出精度の評価：eval_pred_LMW.py
深層学習で出力した各領域のマスク画像の抽出精度を評価する
### 実行方法
```bash
python eval_pred_LMW.py --eval_dir ~/path/prediction/mask --gt_dir ~/path/ground-truth/mask --out_csv ~/path/output/csv
```
### 動作の処理
1. LMW_to_IBIVUS_iput.pyで生成したLumenやMediaやWireのマスク画像と正解のマスク画像を読み込む<br>
2. Jaccard係数とHausdorff距離の計算<br>
3. 計算結果をcsvで出力<br>
