"""Sample Data

Creates and saves profiles for the films given in sample_data.

"""

import glob
import profiler
import os
import csv

from adapters import IMDbAdapter, RTAdapter, MetacriticAdapter


def create_sample_output(filename):
	short_filename = os.path.basename(filename)
	print 'Opening file: "%s"' % short_filename
	# Open file and extract film titles
	with open(filename, 'r') as f:
		titles = [line.strip() for line in f.readlines()]
	# Create adapters
	adapters = [
		RTAdapter(),
		IMDbAdapter(),
		MetacriticAdapter()
	]
	# Create film profiles
	profiles = []
	for title in titles:
		profile = profiler.create_profile(title, adapters)
		profiles.append(profile)
		print profile
	# Write output
	print 'Writing film profiles'
	with open('sample_data/output/' + short_filename[:-3] + 'csv', 'w') as f:
		writer = csv.writer(f)
		headers = ['Title']
		[headers.append(str(a)) for a in adapters]
		writer.writerow(headers)
		for p in profiles:
			row = []
			row.append(p.film)
			for s in p.scores:
				row.append(str(s[1]))
			writer.writerow(row)
	print 'Done'

if __name__ == '__main__':
	print 'Looking for "*.txt" files in folder "sample_data"'
	# Find sample files
	files = glob.glob('sample_data/*.txt')
	for f in files:
		create_sample_output(f)

	# a = [
	# 	'asdasd',
	# 	'asdasdafvxcv',
	# 	'vrwgeg'
	# ]

	# with open('test.txt', 'w') as f:
	# 	for s in a:
	# 		f.write(s + '\n')