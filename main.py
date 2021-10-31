import requests
from html.parser import HTMLParser
import nlp_rake
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-u', '--url', dest="url", default='https://en.wikipedia.org/wiki/Vsauce')
parser.add_option('-f', '--min-freq', dest="min_freq", default=3, type='int', help="Minimum Frequency of word to be included")
parser.add_option('-c', '--min-chars', dest="min_chars", default=5, type='int', help="Minimum Characters in word to be included")
(options, args) = parser.parse_args()

url = options.url
min_freq = options.min_freq
min_chars = options.min_chars

text = requests.get(url).content.decode('utf-8')

class MyHTMLParser(HTMLParser):
	script = False
	res = ""
	def handle_starttag(self, tag, attrs):
		if tag.lower() in ["script", "style"]:
			self.script = True
	def handle_endtag(self, tag):
		if tag.lower() in ["script", "style"]:
			self.script = False
	def handle_data(self, data):
		if str.strip(data) == "" or self.script:
			return
		self.res += ' ' + data.replace('[ edit ]', '')

parser = MyHTMLParser()
parser.feed(text)
text = parser.res

extractor = nlp_rake.Rake(max_words=2, min_freq=min_freq, min_chars=min_chars)
res = extractor.apply(text)

wc = WordCloud(background_color='white',width=800,height=600)
plt.figure(figsize=(15,7))
plt.imshow(wc.generate_from_frequencies({ k:v for k,v in res }))
plt.show();