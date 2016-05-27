import csv
import requests
import csvmapper
from csvmapper import CSVParser

class CSVGoogleParser(CSVParser):
	"""CSV Parser capable of parsing against a pre-defined mapper file"""
	#def __init__(self, csvFile, fmapper=None, hasHeader=False):
	def __init__(self, spreadsheet_key, fmapper=None, hasHeader=False):
		super(CSVGoogleParser, self).__init__(None, fmapper=fmapper, hasHeader=hasHeader)
		# the csv file
		#self.csvFile = csvFile
		# the mapper object
		self.spreadsheet_key = spreadsheet_key



	# parses a CSV file
	def parseCSV(self):

		CSV_URL = "https://docs.google.com/spreadsheets/d/" + self.spreadsheet_key + "/pub?output=csv"

		with requests.Session() as s:
			download = s.get(CSV_URL)

			decoded_content = download.content.decode('utf-8')

			cr = csv.reader(decoded_content.splitlines(), delimiter=',')
			my_list = list(cr)
			x = []
			for row in my_list:
				x.append(row)
			self.csvData = x