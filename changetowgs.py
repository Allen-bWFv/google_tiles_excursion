#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# by zhoujm00000 2018年11月15日09:49
import math
import thread
import os
import sys
import gcl_wgs
from PIL import Image
import globalmaptiles
gm = globalmaptiles.GlobalMercator()
reload(sys)
sys.setdefaultencoding('utf-8')


# 根据文件夹内的图片确定处理范围
def getxx(fielname):
	dirs = os.listdir(fielname)
	namelist = []
	for i in dirs:
		split = i.split('_')
		namelist.append(int(split[0]))
	return min(namelist), max(namelist)


# 根据文件夹内的图片确定处理范围
def getyy(fielname):
	dirs = os.listdir(fielname)
	namelist = []
	for i in dirs:
		y = os.path.splitext(i)[0]
		hy = y.split('_')[1]
		namelist.append(int(hy))
	return min(namelist), max(namelist)


def towgs(x1, x2, y1, y2, z,lock):
	zoom = z
	for j in range(x1, x2 + 1):
		for i in range(y1, y2 + 1):
			# bounds(minLat, minLon, maxLat, maxLon)
			ii = (2 ** zoom - 1) - i
			bounds = gm.TileLatLonBounds(j, ii, z)
			lon, lat = gcl_wgs.wgs84togcj02(bounds[1], bounds[0])
			tx, ty = gm.LatLontoTile(lat, lon, zoom)
			bounds2 = gm.TileLatLonBounds(tx, ty, zoom)
			px1, py1 = gm.LatLontoPixels(lat, lon, zoom)
			px2, py2 = gm.LatLontoPixels(bounds2[0], bounds2[1], zoom)
			box = (int(abs(px2 - px1)), tileSize - int(abs(py2 - py1)), int(abs(px2 - px1) + tileSize),
			       2 * tileSize - int(abs(py2 - py1)))
			ty = (2 ** zoom - 1) - ty
			img0 = imgfiles + str(zoom) + "/" + str(tx) + "_" + str(ty) + ".png"
			img1 = imgfiles + str(zoom) + "/" + str(tx) + "_" + str(ty - 1) + ".png"
			img2 = imgfiles + str(zoom) + "/" + str(tx + 1) + "_" + str(ty - 1) + ".png"
			img3 = imgfiles + str(zoom) + "/" + str(tx + 1) + "_" + str(ty) + ".png"

			if (os.path.exists(img0) and os.path.exists(img1) and os.path.exists(img2) and os.path.exists(img3)):
				outfile = output_location + str(zoom) + '/' + str(j) + '_'

				# if not os.path.exists(outfile):
				# 	os.mkdir(outfile)

				if (isTile):
					jgname = outfile + str(ii) + ".jpeg"
				else:
					# google编号
					jgname = outfile + str(i) + ".jpeg"
				target = Image.new('RGB', (tileSize * 2, tileSize * 2))
				target.paste(Image.open(img0), (0 * tileSize, 1 * tileSize))
				target.paste(Image.open(img1), (0 * tileSize, 0 * tileSize))
				target.paste(Image.open(img2), (1 * tileSize, 0 * tileSize))
				target.paste(Image.open(img3), (1 * tileSize, 1 * tileSize))
				newimg = target.crop(box)
				newimg.save(jgname, quality=quality_value)
				# print tx, ty
	print 'end' ,x1, x2
	lock.release()


# 原始文件位置
imgfiles =r"D:/work/project/tea_weather/tiles/google_tiles/"
# 结果文件位置
output_location = r"D:/work/project/tea_weather/tiles/google_tiles_fix/"
# 拼合级别
z = 7
# 瓦片大小
tileSize = 256
# 保存质量
quality_value = 70
# 是否修改为Tile编号
isTile = False

if __name__ == "__main__":
	# 根据文件夹内图片进行修改图片范围设置
	x1, x2 = getxx(imgfiles + str(z))
	y1, y2 = getyy(imgfiles + str(z))
	if not os.path.exists(output_location + str(z) +"/"):
		os.mkdir(output_location + str(z) +"/")
	print x1, x2, y1, y2, z

	# 多线程处理
	threadN = 10
	b = int(math.ceil((x2 - x1 + 1.0) / threadN))
	locks = []
	for i in range(0, threadN):
		start =int( x1 + b * i)
		if start >x2:break
		end = start + b-1
		if start + b > x2 :end = x2
		lock = thread.allocate_lock()
		lock.acquire()
		locks.append(lock)
		thread.start_new_thread(towgs, (start, end, y1, y2, z,lock))
		print start, end, y1, y2, z

	for lock in locks :
		while lock.locked() :
			pass
