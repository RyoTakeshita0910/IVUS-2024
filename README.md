# IVUS-2024


## 環境設定
- anacondaの仮想環境作成
- pythonのversion >= 3.9
```bash
conda create -n IVUS-2024 python=3.9
```

- ライブラリのインストール
- **※足りないライブラリはその都度インストールしてください**
```bash
pip install -r requirements.txt
```

## 前処理

## 推論(Inference)
上から順に実行してください
<br>

### 1. 血管壁の領域抽出(Segmentation vessel wall)
#### 画像生成
- IVUS画像をU-Net++に入力し、Lumen, Media, Wireの領域を予測(IVUS-2024-DL)
- 深層学習モデルで生成したLumen, Media, Wireに大津の二値化とラベル削除を適用し、それぞれのマスク画像と、**血管壁領域のIVUS画像を生成**(LMW_to_IBIVUS_input.py)

#### 結果解析
- Lumen, Media, WireのJaccard係数とHausdorff距離を計算(eval_pred_LMW.py)

### 2. プラーク成分の領域分割(Segmentation Plaque)
#### 画像生成 1
- **血管壁領域のIVUS画像**を深層学習モデルに入力し、背景と各プラーク成分の領域を予測(IVUS-2024-DL)
- 深層学習モデルで生成した背景と各プラーク成分の領域からIB-IVUS画像を生成(make_IBIVUS.py)

#### 画像生成 2
- Lumen, Media, Wireの正解のマスク画像から、**正解の血管壁領域のIVUS画像を生成**(LMW_to_IBIVUS_input.py)
- **正解の血管壁領域のIVUS画像**を深層学習モデルに入力し、背景と各プラーク成分の領域を予測(IVUS-2024-DL)
- 正解の血管壁領域から生成した背景と各プラーク成分の領域からIB-IVUS画像(血管壁領域は正解画像を使用)を生成(make_IBIVUS.py)

#### 結果解析
- **正解のIB-IVUS画像**と**正解の血管壁領域から生成したIB-IVUS画像**を用いて、パッチ画像を作成し、全パッチ画像をクラス分け(make_patch_IBIVUS.py)
- 正解クラスと予測クラスの混同行列から各プラーク成分の一致率を算出し、手法のプラーク分類精度を評価(eval_patch_IBIVUS.py)

### 3. 血管の状態判別(Vessel discirimination)
#### 結果解析
- 正解と予測のIB-IVUS画像における脂質プラークの割合を算出(calc_lipid_rate_IBIVUS.py)
- 脂質プラークの割合から血管の状態を判別し、正解と予測の感度・特異度を算出(eval_lipid_rate_IBIVUS.py)
- 正解と予測の脂質プラークの割合からROC曲線の描画とAUCを算出(make_roc.py)