#!/bin/bash

# ウィンドウタイトルを指定
WINDOW_TITLE="/bin/bash"

# 無限ループでウィンドウを前面に表示
while true; do
    # ウィンドウIDを取得
    WINDOW_ID=$(wmctrl -lx | grep "$WINDOW_TITLE" | awk '{print $1}')
    
    if [ -n "$WINDOW_ID" ]; then
        # ウィンドウを最前面に移動
        wmctrl -ia "$WINDOW_ID"
    else
        echo "ウィンドウが見つかりません: $WINDOW_TITLE"
    fi

    # 1秒待機
    sleep 1
done
