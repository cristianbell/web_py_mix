"""
Status: -
professionKey:
[
  "00102bb8-a36d-4e5a-a874-b8fe856d9901",
  "18fda4ca-e0c5-4110-94de-c109f9697e9f",
  "d3edc2ae-818f-4e94-82b2-8cbc6114567b",
  "32684e5c-9b64-439c-86f2-ff6f62d7d4c0",
  "e3f15fc9-e1ec-4c2c-81e3-8a40a827ce5e",
  "0ae60915-d9fb-46ff-a6f2-dec89f4427ab",
  "39f3f0ad-bf7d-418e-ab4e-bb68f2a67339",
  "fda65a8c-2f0f-48e9-8c73-ce93c3f19624",
  "7507ca69-9774-42a1-ba7e-3b824ae21af1",
  "088b18b2-aa7a-45f9-90d1-022d53891282"
]

fields: E-Mail-Adresse, Telefonnummer, Vorname, Nachname, Staus
"""

from datetime import datetime
from os import walk
import json
import csv

crt_year = datetime.today().year

_, _, filenames = next(walk('dump/journeymanBackend-prod-talent_Apr/data'))

matched = 0
total = 0
professionKeys = [
    "00102bb8-a36d-4e5a-a874-b8fe856d9901",
    "18fda4ca-e0c5-4110-94de-c109f9697e9f",
    "d3edc2ae-818f-4e94-82b2-8cbc6114567b",
    "32684e5c-9b64-439c-86f2-ff6f62d7d4c0",
    "e3f15fc9-e1ec-4c2c-81e3-8a40a827ce5e",
    "0ae60915-d9fb-46ff-a6f2-dec89f4427ab",
    "39f3f0ad-bf7d-418e-ab4e-bb68f2a67339",
    "fda65a8c-2f0f-48e9-8c73-ce93c3f19624",
    "7507ca69-9774-42a1-ba7e-3b824ae21af1",
    "088b18b2-aa7a-45f9-90d1-022d53891282"
]

with open('talents.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['email', 'phone', 'first_name', 'last_name', 'profession', 'country'])
    for file in filenames:
        with open('dump/journeymanBackend-prod-talent/data/' + file) as f:
            data = json.load(f)

            for item in data['Items']:
                total = total + 1
                if 'status' in item['profile']['M'] and 'currentStatus' in item['profile']['M']['status']['M']:
                    status = int(item['profile']['M']['status']['M']['currentStatus']['S'])

                contact = item['contact']['M']
                phone = contact['phone']['L'][0]['M']['number']['S'] if 'phone' in contact \
                                                                        and len(contact['phone']['L']) > 0 else ''

                firstName = contact['firstName']['S'] if ('firstName' in contact and 'S' in contact['firstName']) \
                    else ''
                lastName = contact['lastName']['S'] if ('lastName' in contact and 'S' in contact['lastName']) else ''

                address = item['address']['M'] if 'address' in item else ''
                country = address['country']['S'] if 'country' in address else ''

                profession = None

                if 'professionKeys' in item['profile']['M']:
                    for key in item['profile']['M']['professionKeys']['L']:
                        if key['S'] in professionKeys:
                            profession = item['profile']['M']['professions']['L'][0]['M']['profession']['S'].replace(
                                '\n', '')
                            matched = matched + 1
                            print('{}, {}, {}, {}, {}, {}'.format(
                                item['email']['S'], phone, firstName, lastName, profession, country))
                            writer.writerow(
                                [item['email']['S'], phone, firstName, lastName,
                                 profession, country])

print('{} out of total {}'.format(matched, total))
