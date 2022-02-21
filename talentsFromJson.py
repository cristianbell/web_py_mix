"""
Status: pre-nominees, nominees, Journeyman & Graduates

profile.status.currentStatus: ["25", "30", "40", "50"]}

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

with open('talents.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['email', 'phone', 'first_name', 'last_name', 'education', 'city', 'region', 'country',
                     'postal_code', 'dob', 'year_of_birth', 'gender', 'age'])
    for file in filenames:
        with open(src_folder + '/' + file) as f:
            data = json.load(f)

            for item in data['Items']:
                total = total + 1
                if 'status' in item['profile']['M'] and 'currentStatus' in item['profile']['M']['status']['M']:
                    status = int(item['profile']['M']['status']['M']['currentStatus']['S'])
                    if status in (25, 30, 40, 50):
                        idx = idx + 1
                        contact = item['contact']['M']
                        phone = contact['phone']['L'][0]['M']['number']['S'] if 'phone' in contact \
                                                                                and len(contact['phone']['L']) > 0 else ''
                        dob = contact['dateOfBirth']['S'] if 'dateOfBirth' in contact else ''
                        yob = dob[:4] if dob != '' else ''
                        age = crt_year - int(yob) if yob != '' else ''
                        gender = contact['gender']['S'] if 'gender' in contact else ''

                        address = item['address']['M'] if 'address' in item else ''
                        city = address['city']['S'].replace(', \n', '; ') if 'city' in address else ''
                        region = address['state']['S'] if 'state' in address else ''
                        country = address['country']['S'] if 'country' in address else ''
                        postal_code = address['zip']['S'] if 'zip' in address else ''

                        education = item['profile']['M']['professions']['L'][0]['M']['profession']['S'].replace('\n', '')

                        print('{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(
                            item['email']['S'], phone, contact['firstName']['S'],
                            contact['lastName']['S'], education,
                            city, region, country, postal_code, dob, yob, gender, age))

                        writer.writerow([item['email']['S'], phone, contact['firstName']['S'], contact['lastName']['S'],
                                         education, city, region, country, postal_code, dob, yob, gender, age])

print('{} out of total {}'.format(idx, total))
