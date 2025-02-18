#!/bin/bash

# 対象となるファイルが存在するディレクトリ（適宜変更してください）
TARGET_DIR="/media/eikinagata2/Elements/bag/uda_for_merge"
REMOVED_DIR="/media/eikinagata2/Elements/bag/data_renamed"
cd $TARGET_DIR
# ファイルを処理する
for file in ${TARGET_DIR}/*.db3; do
    # ファイル名から最後の番号部分を取得
    base_name=$(basename "$file")
    prefix="${base_name%_*}" # 最後のアンダースコア以降を除去
    number_part="${base_name##*_}" # 最後のアンダースコア以降を抽出
    number="${number_part%.*}" # 拡張子を除外
    extension="${number_part##*.}" # 拡張子を抽出

    # 番号を3桁にフォーマット
    formatted_number=$(printf "%03d" "$number")

    # 新しいファイル名を作成
    new_name="${prefix}_${formatted_number}.${extension}"

    # ファイル名を変更
    mv "$file" "${REMOVED_DIR}/${new_name}"
    echo "Renamed: $file -> ${TARGET_DIR}${new_name}"
done
