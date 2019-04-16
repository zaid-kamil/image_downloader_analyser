import os

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import pandas as pd
import requests
import shutil
from classify import makeprediction
from io import open as iopen
from urllib.parse import urlsplit
from google_images_download import google_images_download
from datetime import datetime
import time
app = Flask(__name__)
app.secret_key = "major blazer"

@app.route('/images')
def show_images():
    df = pd.read_csv("images.csv")
    src = df['src'].tolist()[:30]
    title = df['title'].tolist()[:30]
    data = [(s, t) for s, t in zip(src, title)]
    session['data'] = data
    return render_template('view.html', images=data)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        query = request.form.get('query')
        size = request.form.get('size','medium')
        limit = request.form.get('limit')
        # scraper execute
        if query:
            print("query",query)
            print("size",size)
            print("limit",limit)
            path = downloader(query,limit,size)
            return jsonify({'result': 'done','folder':path})
    return render_template('index.html')

def downloader(query,limit=5,size='medium',dir=str(int(datetime.timestamp(datetime.now())))):
    
    directory=os.path.join('static','downloads',dir)
    response = google_images_download.googleimagesdownload()
    arguments = {"keywords": f"{query}",
                 "limit": limit,
                 "print_urls": True,
                 "output_directory":directory,
                 "no_directory":True,
                 "size":size,
                 }
    paths = response.download(arguments)
    return dir


def getImage(data):
    print(data)
    suffix_list = ['jpg', 'jpeg', 'gif', 'png', 'tif']
    ext = data[0].split('?')[0]
    print('norm', ext)
    ext = ext.split('/')[-1].split('.')[-1]
    print('clean', ext)
    name = data[1].replace(" ", "_") + '.' + ext
    imagepath = os.path.join('download', name)
    if os.path.exists(imagepath):
        return imagepath
    if ext in suffix_list:
        response = requests.get(data[0], headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        })
        if response.status_code == 200:
            with iopen(imagepath, 'wb') as out_file:
                out_file.write(response.content)
            del response
            return imagepath
        else:
            print(response.text)
            print('no response')
            return None
    else:
        print('wrong extension')
        return None


@app.route('/classify', methods=['GET', 'POST'])
def classify_image():
    if request.method=='GET':
        dir = request.args.get('p')
        directory=os.path.join('static','downloads',dir)
        results = []
        for image in os.listdir(directory):
            fullimage=os.path.join(directory,image)
            print("image",fullimage) 
            if image and os.path.exists(fullimage):
                out = makeprediction(fullimage)
                results.append([
                    fullimage,
                    out,
                ])
        return render_template('classify.html', results=results)
    else:
        return redirect('/')
    

@app.route('/savedimages')
def saved_images():
    images_dir=os.path.join('static','downloads')
    images=[(item,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(item)))) for item in os.listdir(images_dir)]
    return render_template('view.html', data=images)


if __name__ == '__main__':
    app.run(debug=True)
