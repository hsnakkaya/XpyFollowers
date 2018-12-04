import csv
import pandas


def edges_process(id_var):  # Iterate through all files and find edges, id_var = id number to iterate up to

    # open new csv file

    with open('output/edges.csv', mode='w', encoding='utf-8', newline='') as file:

        # create and write the headers needed for Gephi

        fieldnames = ['Source', 'Target', 'Weight']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()

        csv_writer = csv.writer(file)

        # iterate through all files and find common followers

        for x in range(id_var):

            with open('follower_ids/' + str(x+1) + '.csv', 'r') as f:
                a = set([row[0] for row in csv.reader(f)])
                f.close()

            for y in range(id_var-1):

                if y+2 <= x+1:
                    continue
                with open('follower_ids/' + str(y+2) + '.csv', 'r') as f:
                    b = set([row[0] for row in csv.reader(f)])
                    f.close()

                # Write data to the file

                source = x+1
                target = y+2
                weight = len(a.intersection(b))
                row_to_write = [source, target, weight]
                csv_writer.writerow(row_to_write)

        file.close()


def nodes_process(id_var):  # id_var = id number to iterate up to

    excel_list = pandas.read_excel('list.xlsx', sheet_name='Sheet1')

    with open('output/nodes.csv', mode='w', encoding='utf-8', newline='') as file:

        fieldnames = ['Id', 'Label', 'Weight', 'Category', 'Subcategory', 'Twitter_handle', 'Verified']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()

        csv_writer = csv.writer(file)

        for x in range(id_var):

            with open('follower_ids/' + str(x+1) + '.csv', 'r') as f:
                a = set([row[0] for row in csv.reader(f)])

                label = excel_list.loc[x, 'name']
                weight = len(a)
                category = excel_list.loc[x, 'category']
                subcategory = excel_list.loc[x, 'subcategory']
                handle = '@' + excel_list.loc[x, 'twitter_handle']
                verified = excel_list.loc[x, 'verified']

                row_to_write = [x+1, label, weight, category, subcategory, handle, verified]

                csv_writer.writerow(row_to_write)
                f.close()
        file.close()


edges_process(69)
nodes_process(69)

