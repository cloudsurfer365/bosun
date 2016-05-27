import csv
import requests
import csvmapper
from csvmapper import CSVParser

class CSVGoogleParser(CSVParser):
	"""CSV Parser capable of parsing against a pre-defined mapper file"""
	#def __init__(self, csvFile, fmapper=None, hasHeader=False):
	def __init__(self, spreadsheet_key, fmapper=None, hasHeader=False):
		super(CSVGoogleParser, self).__init__(None, fmapper=fmapper, hasHeader=hasHeader)
		# the mapper object
		self.spreadsheet_key = spreadsheet_key

	# parses a CSV file
	def parseCSV(self):

		# google spreadsheet csv URL
		CSV_URL = "https://docs.google.com/spreadsheets/d/" + self.spreadsheet_key + "/pub?output=csv"

		# parse csv
		with requests.Session() as s:

			# download csv
			download = s.get(CSV_URL)

			# decode csv content
			decoded_content = download.content.decode('utf-8')

			# read csv content
			cr = csv.reader(decoded_content.splitlines(), delimiter=',')

			# convert csv content to csv data for csvmapper
			my_list = list(cr)
			x = []
			for row in my_list:
				x.append(row)
			self.csvData = x