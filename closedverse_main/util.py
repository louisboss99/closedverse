from lxml import html
import urllib.request, urllib.error
import json
import time
from datetime import datetime
from math import floor
import cloudinary
import cloudinary.uploader
import cloudinary.api
import imghdr
import base64
from closedverse import settings

def HumanTime(date, full=False):
	now = time.time()
	if ((now - date) >= 345600) or full:
		return datetime.fromtimestamp(date).strftime('%m/%d/%Y %l:%M %p')
	interval = (now - date)
	if interval <= 59:
		return 'Less than a minute ago'
	intvals = [86400, 3600, 60, ]
	for i in intvals:
		if interval < i:
			continue
		nounits = floor(interval / i)
		text = {86400: 'day', 3600: 'hour', 60: 'minute', }.get(i)
		if nounits > 1:
			text += 's'
		return str(nounits) + ' ' + text + ' ago';


def get_mii(nnid):
	try:
		page = urllib.request.urlopen('https://miiverse.nintendo.net/users/{0}/favorites'.format(nnid)).read()
	except urllib.error.HTTPError:
		return False
	ftree = html.fromstring(page)
	miihash = ftree.xpath('//*[@id="sidebar-profile-body"]/div/a/img/@src')[0].split('.net/')[1].split('_n')[0]
	screenname = ftree.xpath('//*[@id="sidebar-profile-body"]/a/text()')[0]
	
	return [miihash, screenname, nnid]

def recaptcha_verify(request, key):
	if not request.POST.get('g-recaptcha-response'):
		return False
	re_request = urllib.request.urlopen('https://www.google.com/recaptcha/api/siteverify?secret={0}&response={1}&remoteip={2}'.format(key, request.POST['g-recaptcha-response'], request.META['REMOTE_ADDR']))
	jsond = json.loads(re_request.read().decode())
	if not jsond['success']:
		return False
	return True



def image_upload(img):
	if img == 'iVBORw0KGgoAAAANSUhEUgAAAUAAAAB4CAYAAACDziveAAADi0lEQVR4Xu3UAQ0AMAwCwc2/aJbMxl8dcDTcbTuOAAECQYFrAIOti0yAwBcwgB6BAIGsgAHMVi84AQIG0A8QIJAVMIDZ6gUnQMAA+gECBLICBjBbveAECBhAP0CAQFbAAGarF5wAAQPoBwgQyAoYwGz1ghMgYAD9AAECWQEDmK1ecAIEDKAfIEAgK2AAs9ULToCAAfQDBAhkBQxgtnrBCRAwgH6AAIGsgAHMVi84AQIG0A8QIJAVMIDZ6gUnQMAA+gECBLICBjBbveAECBhAP0CAQFbAAGarF5wAAQPoBwgQyAoYwGz1ghMgYAD9AAECWQEDmK1ecAIEDKAfIEAgK2AAs9ULToCAAfQDBAhkBQxgtnrBCRAwgH6AAIGsgAHMVi84AQIG0A8QIJAVMIDZ6gUnQMAA+gECBLICBjBbveAECBhAP0CAQFbAAGarF5wAAQPoBwgQyAoYwGz1ghMgYAD9AAECWQEDmK1ecAIEDKAfIEAgK2AAs9ULToCAAfQDBAhkBQxgtnrBCRAwgH6AAIGsgAHMVi84AQIG0A8QIJAVMIDZ6gUnQMAA+gECBLICBjBbveAECBhAP0CAQFbAAGarF5wAAQPoBwgQyAoYwGz1ghMgYAD9AAECWQEDmK1ecAIEDKAfIEAgK2AAs9ULToCAAfQDBAhkBQxgtnrBCRAwgH6AAIGsgAHMVi84AQIG0A8QIJAVMIDZ6gUnQMAA+gECBLICBjBbveAECBhAP0CAQFbAAGarF5wAAQPoBwgQyAoYwGz1ghMgYAD9AAECWQEDmK1ecAIEDKAfIEAgK2AAs9ULToCAAfQDBAhkBQxgtnrBCRAwgH6AAIGsgAHMVi84AQIG0A8QIJAVMIDZ6gUnQMAA+gECBLICBjBbveAECBhAP0CAQFbAAGarF5wAAQPoBwgQyAoYwGz1ghMgYAD9AAECWQEDmK1ecAIEDKAfIEAgK2AAs9ULToCAAfQDBAhkBQxgtnrBCRAwgH6AAIGsgAHMVi84AQIG0A8QIJAVMIDZ6gUnQMAA+gECBLICBjBbveAECBhAP0CAQFbAAGarF5wAAQPoBwgQyAoYwGz1ghMgYAD9AAECWQEDmK1ecAIEDKAfIEAgK2AAs9ULToCAAfQDBAhkBQxgtnrBCRAwgH6AAIGsgAHMVi84AQIG0A8QIJAVMIDZ6gUnQMAA+gECBLICBjBbveAECDyPXt6oD5NyewAAAABJRU5ErkJggg==':
		return 1
	try:
		decodedimg = base64.b64decode(img)
	except binascii.Error:
		return 1
	what = imghdr.what('', decodedimg)
	if not what:
		return 1
	cloudinary.config( 
		cloud_name = settings.cloudinary_name, 
		api_key = settings.cloudinary_key, 
		api_secret = settings.cloudinary_secret
	)
	up = cloudinary.uploader.upload('data:image/'+ what +';base64,' + img)
	return up.get('secure_url')
