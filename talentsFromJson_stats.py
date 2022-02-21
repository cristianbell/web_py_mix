"""
fields: E-Mail-Adresse, Telefonnummer, Vorname, Nachname, Ausbildung (bzw. Job), Stadt, Bundesland/Region,
Land, Postleitzahl, Geburtsdatum, Geburtsjahr, Geschlecht, Alter

"""
from datetime import datetime
from os import walk
import json
import csv

crt_year = datetime.today().year
src_folder = 'dump/journeymanBackend-prod-talent/data'

_, _, filenames = next(walk(src_folder))

idx = 0
total = 0
seniority_no = 0
seniority_yes = 0
profile_complete_low = 0
profile_complete_med = 0
profile_complete_high = 0

with open('talents.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['email', 'phone', 'first_name', 'last_name', 'education', 'city', 'region', 'country',
                     'postal_code', 'dob', 'year_of_birth', 'gender', 'age'])
    for file in filenames:
        with open(src_folder + '/' + file) as f:
            data = json.load(f)

            for item in data['Items']:
                total = total + 1
                try:
                    education = item['profile']['M']['professions']['L'][0]['M']['profession']['S'].replace('\n', '')
                    profile_complete = int(item['profile']['M']['completion']['M']['percent']['N'].replace('\n', ''))
                    if education in ('Anderer Beruf / Sonstige', 'Auszubildender / ohne Ausbildung'):
                        seniority_no += 1
                    else:
                        seniority_yes += 1
                    if profile_complete < 26:
                        profile_complete_low += 1
                    elif 26 <= profile_complete < 70:
                        profile_complete_med += 1
                    else:
                        profile_complete_high += 1

                    idx += 1
                except IndexError:
                    pass
                except KeyError:
                    pass

print(f"{total}: Ausbildung no: {seniority_no/idx} / yes: {seniority_yes/idx} | {profile_complete_low/idx} / "
      f"{profile_complete_med/idx} / {profile_complete_high/idx}")
print('{} out of total {}'.format(idx, total))
