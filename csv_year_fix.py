import csv


def csv_year_circa_fix():
    data = []
    header = None
    file_name = 'train_info_modified.csv'
    file_name_fixed = 'train_info_modified_fixed.csv'
    try:
        with open(file_name) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[5][:2] == 'c.':
                    line[5] = line[5][2:]
                data.append(line)
    except Exception as e:
        print(e)

    header = data[0]
    data = data[1:]

    # for line in data:
    #     if not line[5].isdigit() and line[5] != '':
    #         print(line[5],line[0])

    try:
        with open(file_name_fixed, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for x in data:
                writer.writerow(x)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    csv_year_circa_fix()
