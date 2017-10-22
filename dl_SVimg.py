# coding:utf-8
''' ASCII のエラーは上のやつを加えると治る,httpsにするとエラーが出る '''
''' 　　　　　参考　　　　　　　　　　　　　　　　　　　　　　　　　'''
''' https://qiita.com/donksite/items/21852b2baa94c94ffcbe '''
''' やること：画像のファイル名を変える、パノラマIDを入力に加えてファイル名から座標がわかるようにする、cssを読み込めるようにする '''

import requests
import os
import sys
import csv

# 画像をダウンロードする
def download_image(url, timeout = 10):
    response = requests.get(url, allow_redirects=False, timeout=timeout)

    if response.status_code != 200:
        e = Exception("HTTP status: " + response.status_code)
        raise e

    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        e = Exception("Content-Type: " + content_type)
        raise e

    return response.content

# 画像のファイル名を決める
def make_filename(base_dir, panoID, url, direction):
    #ext = os.path.splitext(url)[1] # 拡張子を取得
    ext = ".jpg"
    filename = str(panoID) + "," + str(direction) + ext        # 番号に拡張子をつけてファイル名にする
    print(filename)

    fullpath = os.path.join(base_dir, filename)

    return fullpath

# 画像を保存する
def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)

# メイン
if __name__ == "__main__":
    basic_URL = "http://maps.googleapis.com/maps/api/streetview?size=400x400&pano="
    basic_settings = "&fov=90&heading=365&pitch=10&key="
    APIkey = "AIzaSyC9pE8zT_G8gORaEZYykCUve5k4ozJmQFI"
    urls_txt = "input.txt"
    images_dir = "SVimages"
    idx = 0
    count = 0

    with open('SVinfo1.csv','r') as f1:
        datareader = csv.reader(f1)
        ''' 一列目がpanoID、二列目が道路の向き '''
        for row in datareader:
            if count > 100 :
                break
            ''' 道路の向き±90°で二枚の画像を取得する '''
            dirc1 = float(row[1]) + 90
            dirc2 = float(row[1]) - 90
            url1 = basic_URL + row[0] + "&fov=90&heading=" + str(dirc1) + "&pitch=10&key=" + APIkey
            url2 = basic_URL + row[0] + "&fov=90&heading=" + str(dirc2) + "&pitch=10&key=" + APIkey

            filename1 = make_filename(images_dir, row[0], url1, dirc1)
            filename2 = make_filename(images_dir, row[0], url2, dirc2)

            print( "%s" % (url1))
            try:
                image = download_image(url1)
                save_image(filename1, image)
                image = download_image(url2)
                save_image(filename2, image)
                idx += 1
            except KeyboardInterrupt:
                break
            except Exception as err:
                print ("%s" % (err))

            count += 1


'''
    with open(urls_txt, "r") as fin:
        for line in fin:
            url = line.strip()
            filename = make_filename(images_dir, idx, url, 0)

            print( "%s" % (url))
            try:
                image = download_image(url)
                save_image(filename, image)
                idx += 1
            except KeyboardInterrupt:
                break
            except Exception as err:
                print ("%s" % (err))
'''
