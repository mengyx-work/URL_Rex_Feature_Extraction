import re
import urllib2
import sys
from optparse import OptionParser


def feature_extraction(url):

	req = urllib2.Request(url)
	try:
		response = urllib2.urlopen(req)
	except IOError as e:
		print 'can not open the URL'
		sys.exit(0)

	html = response.read()

	regrex = {'General_Features':'(?<=<title>)(.+)(?=\s-\sYelp<\/title>)', 'Full Address':'(?<=<address>\n)(.+)(?=\n\s+<\/address>)', 'Price Range':'(?<="nowrap price-description">\n)(.+)', 'Phone Number':'(?<=itemprop="telephone">\n)(.+)', 'Open Now':'((?<=nowrap extra open">)|(?<=nowrap extra closed">))(.+)(?=<\/span>)', 'Postal Code':'(?<="postalCode">)(.{4,15})(?=<\/span>)'}
	print '\n'
	for key, value in regrex.iteritems():
		regrexFinder = re.compile(value)
		results = re.findall(regrexFinder, html)

		#extract flavor/name/region features from title 
		if key=='General_Features':
			name = re.findall(r'(.+?)(?=\s-\s?)', results[0])
			flavor = re.findall(r'(?<=\s-\s)(.+?)(?=\s-\s?)', results[0])
			region = re.findall(r'(?<=\s-\s)((.(?!-))+)', results[0])
			print ('Feature Restaurant Name found to be: {0} \nFeature Type found to be: {1}'.format(name[0], flavor[0]))
			print ('Feature Location Regions found to be: {0}'.format(region[1][0])) 
		else:
			#deal with missing features
			if not results:
				if key=='Open Now':
					print ('Feature {0} can not be found, can be closed permentantly.'.format(key))
				if key=='Price Range':
					print ('Feature {0} can not be found.'.format(key))
						
			#all the other regular features
			else: 
				if key=='Open Now':
					status = results[0][1]
					print ('Feature {0} found to be: {1}'.format(key, status)) 	

				else:
					print ('Feature {0} found to be: {1}'.format(key, results[0])) 	


if __name__ == "__main__":

	parser = OptionParser()
	parser.add_option('-f', '--filename', help='URL text file name (each line contains a URL)', dest='filename', default=None, action='store')
	parser.add_option('-l', '--url', help='URL address', dest='url', default=None, action='store')

	(opts, args) = parser.parse_args()

	if opts.filename is not None:
		for line in open(opts.filename):
			feature_extraction(line)

	if opts.url is not None:
		feature_extraction(opts.url)
