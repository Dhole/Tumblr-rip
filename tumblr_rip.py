#!/usr/bin/env python3

""" Tumbrl downloader
This program will download all the images from a Tumblr blog """

__author__ = "Dhole"
__license__ = "BSD"
__version__ = "0.1"
__email__ = "bankukur@gmail.com"
__status__ = "Beta"


from urllib.request import urlopen, urlretrieve
import os, sys, re


def check_url(url):
  #Test if url is ok
  url_parsed = re.findall(".tumblr.com", url)
  if len(url_parsed) < 1:
    #print("Malformed url")
    return ""
  else:
    return url_parsed[0]

def get_images_page(html_code):

  images =re.findall("src=\"(?:.[^\"]*)_(?:[0-9]*).(?:jpg|png|gif)\"", html_code)

  forbidden = ["avatar"]

  images = list(set(images))
  #for im in images:
  #  print(im)
  images_http = []
  for im in images:
    for word in forbidden:
      if word not in im:
        images_http.append(im[5:-1])

  print("Number of images:", len(images_http))
  #print("---")
  #for im in images_http:
  #  print(im)
  return images_http

def check_end(html1, html2, num):
  h1 = html1
  h2 = html2
  for n in range(-2,1):
    h1 = h1.replace(str(num+n),"")
    h2 = h2.replace(str(num+n),"")

  return (h1 == h2)

def download_images(images, path):
  for im in images:
    print(im)
    im_big = im.replace("250", "1280")
    im_big = im_big.replace("500", "1280")
    filename = re.findall("([^/]*).(?:jpg|gif|png)",im)[0]
    filename = os.path.join(path,filename)
    filename_big = re.findall("([^/]*).(?:jpg|gif|png)",im_big)[0]
    filename_big = os.path.join(path,filename_big)
    try:
      urlretrieve(im_big, filename_big)
    except:
      try:
        urlretrieve(im, filename)
      except:
        print("Failed to download "+im)

def main():

  #Check input arguments
  if len(sys.argv) < 2:
    print("usage: ./tumblr_rip.py url [starting page]")
    sys.exit(1)

  url = sys.argv[1]

  if len(sys.argv) == 3:
    pagenum = int(sys.argv[2])
  else:
    pagenum = 1

  if (check_url(url) == ""):
    print("Error: Malformed url")
    sys.exit(1)

  if (url[-1] != "/"):
    url += "/"

  blog_name = url.replace("http://", "")
  blog_name = re.findall("(?:.[^\.]*)", blog_name)[0]
  current_path = os.getcwd()
  path = os.path.join(current_path, blog_name)
  #Create blog directory
  if not os.path.isdir(path):
    os.mkdir(path)

  html_code_old = ""
  while(True):
    #fetch html from url
    print("\nFetching images from page "+str(pagenum)+"\n")
    f = urlopen(url+"page/"+str(pagenum))
    html_code = f.read()
    html_code = str(html_code)
    if(check_end(html_code, html_code_old, pagenum)):
      break

    images = get_images_page(html_code)
    download_images(images, path)

    html_code_old = html_code
    pagenum += 1


  print("Done downloading all images from " + url)


if __name__ == '__main__':
  main()
