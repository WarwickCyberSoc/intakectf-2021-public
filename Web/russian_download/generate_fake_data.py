from faker import Faker
import csv
import os

Faker.seed(0)
fake = Faker()

flag = "WMG{d0wnl04d_l1m175_4r3_n0_ch4ll3n63_f0r_y0u}"

number_of_rows = 1000000
where_to_roughly_put_flag_in_bytes = (64 * 1024 * 1024) + 2431
flag_inserted = False

with open("data.csv", "w", newline="") as csv_file:
    field_names = ["username", "name", "sex", "address", "mail", "birthdate"]
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    for i in range(number_of_rows):
        profile = fake.simple_profile()

        if (
            not flag_inserted
            and os.path.getsize("data.csv") > where_to_roughly_put_flag_in_bytes
        ):
            profile["username"] = flag
            flag_inserted = True

        profile["address"] = profile["address"].replace("\n", "\\n")
        writer.writerow(profile)
