# 血管の状態判別
## 脂質プラークの割合の取得：clac_lipid_rate_IBIVUS.py
IB-IVUS画像から脂質プラーク(青と紫の領域)の割合を取得する

### 実行方法
```bash
python calc_lipid_rate_IBIVUS.py --img_dir ~/path/IB-IVUS --out_csv ~/path/output/csv
```

### 動作
1. IB-IVUS画像から黒と白以外のピクセル数を計測し、そのうち青と紫のピクセル数が含まれる割合を計算
2. 脂質プラークの割合をcsvに保存

**※**上記の処理を**正解のIB-IVUS画像と予測したIB-IVUS画像に適用する**<br>

### 結果例
- 画像のファイル名と脂質プラークの割合が保存される
- 出力したcsvには、**カラム名がない**ことに注意(以下の表は例)
<br>

|(img_name)|(lipid_rate)|
|---|---|
|0001_03492907_000001|0.015427958|
|0001_03492907_000061|0.056617647|
|0001_03492907_000121|0.076437793|
|0001_03492907_000181|0.043006018|
|0001_03492907_000241|0.152689337|
|...|...|

----
<br>

## 血管の状態に関する感度・特異度の算出：eval_lipid_rate_IBIVS.py
正解と予測の脂質プラークの割合から血管の状態判別に関する感度・特異度を算出

### 実行方法
```bash
python eval_lipid_rate_IBIVUS.py --eval_csv ~/path/prediction/lipid rate/csv --gt_csv ~/path/ground-truth/lipid rate/csv --out_csv ~/path/output/csv
```

### 動作
1. 正解と予測の脂質プラークの割合のcsvを読み込む
2. すべての断面について、脂質プラークの割合から血管の状態を判別
3. 断面ごとの正解と予測の感度・特異度を算出
4. 下記の条件に従って、症例ごとの血管状態を判別
5. 症例ごとの正解と予測の感度・特異度を算出
6. csvに結果を保存

<br>

|症例|条件|
|---|---|
|安定|1症例における「安定」な断面の枚数が過半数以上かつ，連続する「不安定」な断面が2枚以下|
|不安定|1症例における「不安定」な断面の枚数が過半数以上または，連続する「不安定」な断面が3枚以上|


### 結果例
- 1つのcsvに、全断面の血管状態、断面ごとの評価結果、症例ごとの血管状態、症例ごとの評価結果が保存される(見づらいけど許して)


|img_name|ground-truth lipid rate|ground-truth result|predisction lipid rate|prediction result|
|---|---|---|---|---|
|0001_03492907_000001|0.048770972|Good|0.015427958|Good|
|0001_03492907_000061|0.067078972|Good|0.056617647|Good|
|...|||||
|断面|不安定(正解)|安定(正解)|||
|不安定(予測)|233|51|||
|安定(予測)|125|680|||
||||||
|感度|0.6508...||||
|特異度|0.9302...||||
||||||
|症例|
|patient_name|gt result|eval result|gt_bad|pred_bad|
|...|||||

----
<br>

## ROC曲線の描画とAUCの算出：make_roc_IVUS.py
正解と予測の脂質プラークの割合から血管の状態判別に関するROC曲線の描画とAUCの算出をする

### 実行方法
```bash
python make_roc_IVUS.py --eval_csv ~/path/prediction/lipid rate/csv --gt_csv ~/path/ground-truth/lipid rate/csv --dest_dir ~/path/output
```

### 動作
1. 正解と予測の脂質プラークの割合のcsvを読み込む
2. 脂質プラークの割合の閾値を変えながら、真陽性率(感度)、偽陽性率(1-特異度)を計算
3. ROC曲線を描画し、グラフを保存
4. AUCを計算し、csvに保存

### 結果例
- ROCグラフの結果

|ROC曲線|
|---|
|<img src="https://github.com/RyoTakeshita0910/IVUS-2024/assets/104045526/22141c76-d3ed-4235-a438-41b373bebf39.png" width="350" height="350">|

<br>

- 各閾値の感度・特異度とAUCをcsvに保存

|threshold(閾値)|sensitivity(感度)|specificity(特異度)|
|---|---|---|
|0|1|1|
|0.05|1|0.954..|
|0.1|1|0.920..|
|...|||
||||
|AUC|0.906...||


# 追加解析(analysis)：正解と予測の相関関係や同等性を評価するために用いるプログラム

