import requests
import argparse

def grabSession(link):
	print(link)
	headers={"Host": "kwik.cx","Referer": "https://kwik.cx", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
	cookies={"cf_clearance":"79138993e6a9f79f94675a9cca0a6ab1dea5a93e-1604345736-0-1zf602d63fz42a4c151z87192af1-250"}
	r = requests.get(link , headers=headers)
	r = r.json()
	print(r)

def search(query):
	headers={"Host": "animepahe.com","Referer": "https://animepahe.com", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
	r = requests.get('https://animepahe.com/api?m=search&l=8&q=' + query, headers=headers)
	r = r.json()
	print(str(r["total"]) + " results found.")
	for data in r["data"]:	
		print("ID=" + str(data["id"])+", \""+data["title"]+"\""+  ", episodes : "+ str(data["episodes"]) + ", status : "+ str(data["status"]) +", year : "+ str(data["year"])) 

def genLink(dnLink):
	data={"_token": "p3qBaGVw9bB8MNFKeavhWBh8dOD4a0u7JDKWyPLV"}
	cookies={"token_QpUJAAAAAAAAGu98Hdz1l_lcSZ2rY60Ajjk9U1c":"BAYAX5_jowFfoDX2gAGBAsAAIOh0h9SaB6cp8MKHkh1LsXMAJ4jZHfLGP3UxyI9nXS8kwQBGMEQCIBiFsa24rgfR_3jIdIV-ic_lJAl3fdgptnSfHLsbhPIXAiBdgnD__Olw1Ddt52WRzhxGBms-a_6H3oYRkv9d66jv-g","kwik_session":"eyJpdiI6InJjXC9FcUZocWNPSlJYRFZoQWR2a1FnPT0iLCJ2YWx1ZSI6ImNrNnZwRkF6MjBRT3NEQ1JzTm1mcGhsbThvQVwvUWdGa2xYcDNEM1ZVS3F1Y2tNRzlWbjBXKzNSVUxPcGNRS0w3IiwibWFjIjoiZjA5NzBhYzg4ZjJmOGIyNjI0ODJhNjg4OTJiZTU1MWFjYjMyMjYyY2U5Y2QyYzY4ZGI1NzUzOGE2MTE2ODUxYyJ9"}
	headers={"Host": "kwik.cx","Referer": "https://kwik.cx","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
	for link in dnLink:
		#link=link.split("/f/")
		#link= link[0] + "/d/" + link[1]
		#print(link)
		r = requests.post(link,data = data ,headers=headers, cookies=cookies,allow_redirects=False )
		#print("Link 1:" + r.headers["Location"] + "\n")
		print(r.status_code)
		if(r.status_code==419):
			print("Page Expired! Refresh token")
		


def getKwik(id):
	once = True
	headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36","Host": "animepahe.com","Referer": "https://animepahe.com"}
	session="invalid"
	dnLink=[]
	link = 'https://animepahe.com/api?m=release&id='+ id + '&l=30&sort=episode_asc&page=1'
	r = requests.get(link, headers=headers)
	#print(r.text)
	r = r.json()
	#print(r)

	if(r["total"]==0):
		print("Invalid anime id!!!")
	else:		
		pg_num=1
		lst=r["last_page"]
		cur= r["current_page"]
		
		#if( lst >= cur):
		for i in range(cur,lst+1):
			link = 'https://animepahe.com/api?m=release&id='+ id + '&l=30&sort=episode_asc&page=' + str(i)
			r = requests.get(link, headers=headers)
			r = r.json()
			count=0
			for data in r["data"]:
				count=count+1
				if(count>2):
					break
				kwik_link = "https://animepahe.com/api?m=links&id=" + id + "&session=" + data["session"] + "&p=kwik"
				r2 = requests.get(kwik_link)
				r2 = r2.json()
				if(once):
					print(r2["data"])
					once = False
				tmp_kwik=r2["data"][1]["720"]["kwik"].split("/e/")
				dnLink.append(tmp_kwik[0]+"/f/"+tmp_kwik[1])
				#print((tmp_kwik[0]+"/d/"+tmp_kwik[1]))
				#info link
				print("Episode " + str(count) + " link fetched")

	print(dnLink)
	#genLink(dnLink)

def parseEpisode(episodes):
	episodeList=[]
	if("-" in episodes):
		for i in range (int(episodes.split("-")[0]),int(episodes.split("-")[1])+1):
			episodeList.append(i)
	elif("," in episodes):
		for i in (episodes.split(",") ):
			episodeList.append(int(i))
	else:
		episodeList.append(int(episodes))

	return episodeList
def download(id,episodes):

	episodeList=parseEpisode(episodes)	

	headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36","Host": "animepahe.com","Referer": "https://animepahe.com"}
	dnLink=[]
	link = 'https://animepahe.com/api?m=release&id='+ id + '&l=30&sort=episode_asc&page=1'
	r = requests.get(link, headers=headers)
	#print(r.text)
	r = r.json()
	#print(r)
	
	if(r["total"]==0):
		print("Invalid anime id!!!")
	else:		
		pg_num=1
		lst=r["last_page"]
		cur= r["current_page"]
		
		#if( lst >= cur):
		for i in range(cur,lst+1):
			link = 'https://animepahe.com/api?m=release&id='+ id + '&l=30&sort=episode_asc&page=' + str(i)
			r = requests.get(link, headers=headers)
			r = r.json()
			#count=0
			for data in r["data"]:
				if(data["episode"] in episodeList):
					#count=count+1
					#if(count>3):
					#	break
					kwik_link = "https://animepahe.com/api?m=links&id=" + id + "&session=" + data["session"] + "&p=kwik"
					r2 = requests.get(kwik_link)
					r2 = r2.json()
					tmp_kwik=r2["data"][0]["720"]["kwik"].split("/e/")
					dnLink.append(tmp_kwik[0]+"/d/"+tmp_kwik[1])

					#info link
					print("Episode " + str(data["episode"]) + " link fetched")

	print(dnLink)
	#genLink(dnLink)
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--search', nargs='+', type=str, help="Search for an anime title")
	parser.add_argument('-i', '--id', type=str, help="Specify the anime using id")
	parser.add_argument('-d', '--download', help="download", action="store_true")
	parser.add_argument('-e', '--episodes', nargs='+', type=str, help="episod no")
	parser.add_argument('-D', '--debug', type=str, help="download")
	parser.add_argument('-v', dest='verbose', action='store_true')
	args = parser.parse_args()
	

	if(args.id):
		if(args.download):
			if(args.episodes):
				#print(args.episodes,type(args.episodes))
				download(args.id,args.episodes[0])
		else:
			getKwik(args.id)
	if(args.search):
		srch=' '.join(args.search)
		#print(search)
		search(srch)
	if(args.debug):
		genLink(['https://kwik.cx/d/rEdOnYPzIt7R', 'https://kwik.cx/d/la74DWGvIs51', 'https://kwik.cx/d/vfLGhKrYaEuh'])
		#download()
	