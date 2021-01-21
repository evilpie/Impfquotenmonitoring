import sys
import os
import openpyxl
import requests
import tempfile

URL = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile'
response = requests.get(URL)

with tempfile.TemporaryFile() as fp:
  fp.write(response.content)

  fp.seek(0)

  workbook = openpyxl.load_workbook(fp)
  sheet = workbook.worksheets[1]

  date = sheet.title.lstrip('Impfungen_bis_einschl_').lstrip('Gesamt_bis_einschl_')
  (day, month, year) = date.split('.')
  date = "20{}-{}-{}".format(year, month, day)

  print('Date: {}'.format(date))

  for number in range(0, 10):
    u = '' if number == 0 else '-{}'.format(number)
    path = 'Impfquotenmonitoring-{}{}.xlsx'.format(date, u)

    if not os.path.exists(path):
      break

    if open(path, mode='rb').read() == response.content:
      print('Duplicate of "{}"'.format(path))
      sys.exit(0)

  print('Creating "{}"'.format(path))
  open(path, mode='wb').write(response.content)
