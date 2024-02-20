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
#### 画像生成
- **血管壁領域のIVUS画像**をU-Net++に入力し、背景と各プラーク成分の領域を予測(IVUS-2024-DL)
- 深層学習モデルで生成した背景と各プラーク成分の領域からIB-IVUS画像を生成(make_IBIVUS.py)

#### 結果解析
- 正解と予測のIB-IVUS画像からパッチ画像を作成し、全パッチ画像をクラス分け(make_patch_IBIVUS.py)
- 正解クラスと予測クラスの混同行列から各プラーク成分の一致率を算出し、手法のプラーク分類精度を評価(eval_patch_IBIVUS.py)

### 3. 血管の状態判別(Vessel discirimination)
#### 結果解析
- 