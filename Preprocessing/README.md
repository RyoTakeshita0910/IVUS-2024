# 前処理
## データを抜き出す(make_IVUS_pngs.py)
- 医師からもらったデータフォルダからデータを抜き出す
- 練習で渡した前処理のプログラム1~3などをまとめてできる

### 実行方法
```bash
python make_IVUS_pngs.py --src_dir ~/path/containing/DICOM/folder --dest_dir ~/path/output --csv_name output csv name
```
<br>

- "src_dir"のフォルダ配置
```bash
src_dir
├── <xxyyzz(dataset name)>
│   ├── VISIATLAS3.DCM
│   │   └── ~ 
│   │       └── xxx000(DICOMファイル)
│   │
│   │(ラベル付けされた画像)
│   ├── Frame000x.png
│   ├── Frame000y.png
│   ├── Frame000z.png
│   ├── ... 
│   │
│   └── xxxyyy.csv(データに関する情報を載せたcsv)
│
├── <wwxxyy(dataset name)>

```
<br>

### 結果例
- "dest_dir"のファルダ配置
```bash
dest_dir
├── dicom(DICOMファイルの保存場所)
│   ├── xxx000
│   ├── yyy000
│   ├── ...
│
├── gt_anno(血管壁の領域抽出のラベル)
│   ├── xxx000_00000x.png
│   ├── xxx000_00000y.png
│   ├── ...
│
├── gt_ib(プラーク成分の領域分割のラベル)
│   ├── xxx000_00000x.png
│   ├── xxx000_00000y.png
│   ├── ...
│
├── input(ラベルのあるIVUS画像)
│   ├── xxx000_00000x.png
│   ├── xxx000_00000y.png
│   ├── ...
│
├── pngs(各DICOMの全ての画像)
│   ├── xxyyzz
│   │   ├── 000001.png
│   │   ├── 000002.png
│   │   ├── ...
│   │   
│   ├── wwxxyy
│   │   ├── 000001.png
│   │   ├── 000002.png
│   │   ├── ...
│
└── (csv_name).csv (DICOMの情報をまとめたcsv)

```

## 医師のアノテーション画像からLumen,Media,Wireのマスク画像を生成する(make_gt_IVUS.py)



## 医師のアノテーション画像からIB-IVUS画像の各プラークのマスク画像を生成する(make_gt_IBIVUS.py)
