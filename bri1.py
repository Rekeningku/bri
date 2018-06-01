refresh_second	= 30
username		= "retnor2908"
password 		= "Kg080808"
no_rekening		= "005301072793501"
db_url			= ""
bank_url		= "https://ib.bri.co.id/ib-bri/Login.html"
logout_url		= "https://ib.bri.co.id/ib-bri/Logout.html"
import sys
import time
import ssl
from functools import wraps
import requests
from BeautifulSoup import BeautifulSoup
from PIL import Image
from PIL import ImageEnhance
import pytesseract
from urllib import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar
ssl.wrap_socket = sslwrap(ssl.wrap_socket)


def get(link):
    urlretrieve(link,'temp.png')

def log(text):
	sys.stdout.write(text)
	sys.stdout.flush()

def captcha2text(img_path):
	im = Image.open(img_path)
	nx, ny = im.size
	#enh = ImageEnhance.Contrast(im)
	#enh.enhance(2)
	enh = ImageEnhance.Brightness(im)
	enh.enhance(5)
	enh = ImageEnhance.Sharpness(im)
	enh.enhance(1.3)
	im2 = im.resize((int(nx*5), int(ny*5)), Image.BICUBIC)
	im2.save("temp2.png")

	imgx = Image.open('temp2.png')
	imgx = imgx.convert("RGBA")
	pix = imgx.load()
	for y in xrange(imgx.size[1]):
	    for x in xrange(imgx.size[0]):
	        if pix[x, y] != (0, 0, 0, 255):
	            pix[x, y] = (255, 255, 255, 255)
	imgx.save("bw.gif", "GIF")
	original = Image.open('bw.gif')
	bg = original.resize((116, 56), Image.NEAREST)
	ext = ".tif"
	bg.save("input-NEAREST" + ext)
	image = Image.open('input-NEAREST.tif')
	text= pytesseract.image_to_string(Image.open('input-NEAREST.tif'))
	return str(filter(str.isdigit, text))

def getCaptcha(fox,element,filename):
	# now that we have the preliminary stuff out of the way time to get that image :D
	location = element.location
	size = element.size
	fox.get_screenshot_as_file('screenshot.png') # saves screenshot of entire page

	im = Image.open('screenshot.png') # uses PIL library to open image in memory

	left = int(location['x'])+1
	top = int(location['y'])
	right = left + int(size['width'])
	bottom = top + int(size['height'])


	im = im.crop((left, top, right, bottom)) # defines crop points
	im.save(filename) # saves new cropped image
	return filename
def isInteger(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

try:
	b=webdriver.PhantomJS()
except:
	log("Can't use PhantomJS as driver")
	raise
else:
	while True:
		log("\r"+time.strftime("[%d/%m/%Y")+" "+time.strftime("%H:%M:%S] ")+"Getting Transactions...   ")
		error=False
		secondtosleep=refresh_second
		b.get(bank_url)
		try:
			elCaptcha = b.find_element_by_css_selector('div#simple_img > img')
		except:
			log("error getting captcha")
		else:
			captcha_img  = getCaptcha(b,elCaptcha,'captcha_bri.png')
			captcha_text = captcha2text(captcha_img)
			#log("Captcha text: "+captcha_text[-4:]+"       ")
			if len(captcha_text)>=4 and isInteger(captcha_text[-4:]):
				try:
					iUsername=b.find_element_by_css_selector('input[name=j_plain_username]')
					iPassword=b.find_element_by_css_selector('input[name=j_plain_password]')
					iCaptcha =b.find_element_by_css_selector('input[name=j_captcha]')
					iLoginBtn=b.find_element_by_css_selector('button[type=submit]')
				except:
					log("Error getting login form input\n")
				else:
					iUsername.send_keys(username)
					iPassword.send_keys(password)
					iCaptcha.send_keys(captcha_text[-4:])
					iLoginBtn.click()
					b.get_screenshot_as_file('bri_loginpage.png')
					try:
						b.find_element_by_css_selector('label.nav-button').click()
					except:
						log("Error opening navigation\n")
					else:
						try:
							b.find_element_by_css_selector('a#myaccounts-side').click()
						except:
							error=True
							log("Error click menu rekening\n")
							b.get(logout_url)

						else:
							iframe=b.find_element_by_css_selector('iframe#iframemenu')
							b.switch_to.frame(iframe)
							try:
								linkmutasirekening=b.find_element_by_link_text('Mutasi Rekening')
							except:
								b.get(logout_url)

							else:
								linkmutasirekening.click()
								try:
									b.switch_to.default_content()
								except:
									log("error switch_to_default_content\n")
									b.get(logout_url)

								else:
									try:
										contentFrame=b.find_element_by_css_selector('iframe#content')
									except:
										log("error getting content frame\n")
										b.get(logout_url)

									else:
										try:
											b.switch_to.frame(contentFrame)
										except:
											log("error switch_to.frame(contentFrame)\n")
											b.get(logout_url)

										else:
											try:
												b.find_element_by_css_selector("select#ACCOUNT_NO > option[value='"+no_rekening+"']").click()
												b.find_element_by_css_selector("input[value='Tampilkan']").click()
											except:
												log("Error filling form\n")
												b.get(logout_url)

											else:
												try:
													trxlist = b.find_elements_by_css_selector('table#tabel-saldo tbody tr')
												except:
													log("Error getting trx list\n")
													b.get(logout_url)

												else:
													for tr in trxlist:
														tds = tr.find_elements_by_css_selector('td')
														if len(tds)==5:
															tipe='DB'

															try:
																tgl 	= tds[0].text
																uraian 	= tds[1].text.replace('\r','').replace('\n','').replace(' ',' ').replace(' ',' ')
																debet 	= tds[2].text.replace('.','').split(',')[0]
																kredit	= tds[3].text.replace('.','').split(',')[0]
																saldo 	= tds[4].text.replace('.','').split(',')[0]
																if len(debet)==0:
																	debet="0"
																if len(kredit)==0:
																	kredit="0"
																if len(saldo)==0:
																	saldo="0"
															except:
																log("Error parsing data\n")
															else:
																if len(tgl)>5:
																	nominal=debet
																	if nominal=="0":
																		tipe='CR'
																		nominal=kredit
																	data=tgl+"|"+uraian+"|"+nominal+"|"+tipe+"|"+saldo
																	log(time.strftime("[%d/%m/%Y")+" "+time.strftime("%H:%M:%S] ")+data+"\n")
													b.get(logout_url)
			else:
				secondtosleep=5
				#log("captcha_text invalid: "+captcha_text)

		if error:
			secondtosleep=600 #pause 10 menit

		ts=time.strftime("[%d/%m/%Y")+" "+time.strftime("%H:%M:%S]")
		for i in range(secondtosleep):
			cd=secondtosleep-(i+1)
			time.sleep(1)
			sys.stdout.write("\r"+ts+" Getting Transactions in "+str(cd)+"                                   ")
			sys.stdout.flush()
		sys.stdout.write("\r")
		sys.stdout.flush()


b.quit()
