# coding=utf-8
import json
import os
import shutil
import time
import zipfile

import yaml
from PIL import Image

from ...platform import CMDProcessor


@CMDProcessor.core_register("file")
class core_module_file(object):
    def __init__(self):
        pass

    @staticmethod
    def ain(uri, mode="r"):
        if not os.path.exists(uri):
            return False
        try:
            with open(uri, mode) as f:
                fileType = uri.split(".")[-1]
                if fileType == "json":
                    f = json.load(f)
                elif fileType == "yml" or fileType == "yaml":
                    f = yaml.safe_load(f)
        except:
            print("\033[31m[load@failed] %s\033[0m" % (uri))
            return False
        return f

    @staticmethod
    def aout(uri, data, mode="w", dRename=True, msg=False):
        if not uri:
            return False

        uri = uri.replace("\\\\", "/").replace("\\", "/").replace("//", "/")

        uriDir = ""
        fileName = ""
        # 获取文件路径
        for x in uri.split("/")[:-1]:
            uriDir = uriDir + x + "/"
        # 获取文件名
        for x in uri.split("/")[-1].split(".")[:-1]:
            fileName = fileName + x + "."
        fileName = fileName[:-1]
        # 获取文件类型
        fileType = uri.split("/")[-1].split(".")[-1]
        # 检测路径中文件夹是否存在，无则创建
        if uriDir != "" and not os.path.exists(uriDir):
            os.makedirs(uriDir)
        # 检测是否有重名文件，有则将文件名改为 x_time
        if dRename and os.path.exists(uri):
            uri = uriDir + fileName + "_" + str(int(time.time())) + "." + fileType

        try:
            with open(uri, mode) as f:
                if fileType == "json":
                    data = json.dumps(data)
                elif fileType == "yml" or fileType == "yaml":
                    data = yaml.dump(data)
                f.write(data)
        except:
            print("\033[31m[save@failed] %s -> %s\033[0m" % (fileName, uri))
            return False
        if msg:
            print(
                "\033[32m[save]\033[0m \033[36m%s\033[0m -> \033[36m%s\033[0m"
                % (fileName, uri)
            )
        return True

    @staticmethod
    def mkdir(path):
        try:
            if path != "" and not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            print("\033[31m%s\033[0m" % e)

    @staticmethod
    def clearDIR(folder, nameList=[]):
        if not os.path.exists(folder):
            return
        for filename in os.listdir(folder):
            if len(nameList) > 0 and filename not in nameList:
                continue
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))

    @staticmethod
    def rm(uri, msg=False):
        uris = uri if type(uri) == list else [uri]
        r = []
        for x in uris:
            if x == "" or not os.path.exists(x):
                r.append(False)
                continue
            try:
                os.remove(x)
            except:
                print("\033[31m[remove@failed] %s\033[0m" % (x))
                r.append(False)
            if msg:
                print("\033[32m[remove]\033[0m \033[36m%s\033[0m" % (x))
            r.append(True)
        return r if len(r) > 1 else r[0]

    @staticmethod
    def unzip(ruri, furi, msg=False):
        try:
            f = zipfile.ZipFile(furi, "r")
            for name in f.namelist():
                f.extract(name, ruri)
            f.close()
        except:
            print("\033[31m[unzip@failed] %s\033[0m" % (furi))
            return False
        if msg:
            print("\033[32m[unzip]\033[0m \033[36m%s\033[0m" % (furi))
        return True

    @staticmethod
    def cov2webp(uri, plist, dlist, quality=100):
        imgs = []
        try:
            for x in plist:
                imgs.append(Image.open(x))
            imgs[0].save(
                uri,
                "webp",
                quality=quality,
                save_all=True,
                append_images=imgs[1:],
                duration=dlist,
            )
        except:
            return False
        return True

    @staticmethod
    def cov2gif(uri, plist, dlist):
        imgs = []
        try:
            for x in plist:
                imgs.append(Image.open(x))
            imgs[0].save(
                uri,
                "gif",
                save_all=True,
                append_images=imgs[1:],
                duration=dlist,
                loop=0,
            )
        except:
            return False
        return True
