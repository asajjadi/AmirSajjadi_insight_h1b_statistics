import csv
import sys


class ItemAggregator:

    @classmethod
    def get_n_item(cls, path, search_item):
        """

        :param path: the input file path
        :param search_item: the item we are interested in
        :return: a list of tuples
        """
        all_items_dic = dict()
        with open(path, newline='') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=';')
            row_num = 0
            item_index = -1
            for row in file_reader:
                if row_num == 0:
                    for i in range(len(row)):
                        if row[i].lower().find(search_item.lower()) != -1:
                            item_index = i
                else:
                    val = all_items_dic.get(row[item_index])
                    if val is None:
                        all_items_dic[row[item_index]] = 1
                    else:
                        all_items_dic[row[item_index]] = val + 1

                row_num += 1

            row_num -= 1
            return sorted(all_items_dic.items(), key=lambda kv: kv[1], reverse=True)

    @classmethod
    def save_n_frequent_item(cls, items_dic, file_name, n, search_item):
        """

        :param items_dic: the list of tuuples
        :param file_name: the saving path
        :param n: n top, for 10 top
        :param search_item: the item we are interested in
        """
        index = 0
        rown_um = sum([val[1] for val in items_dic])
        with open(file_name, "w") as csv_file:
            csv_file.write("TOP_" + search_item + ";NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
            for item in items_dic:
                csv_file.write("{};{};{}%".format(item[0], item[1], round(100 * item[1] / rown_um, 1)))
                csv_file.write('\n')
                index += 1
                if index > n:
                    break


if __name__ == '__main__':
    if len(sys.argv) is not 4:
        print(len(sys.argv))
        print(sys.argv[0] + ": invalid or missing option")
        exit(-1)

    code, input_path, output_path1, output_path2 = sys.argv

    res = ItemAggregator.get_n_item(input_path, "JOB_TITLE")
    ItemAggregator.save_n_frequent_item(res, output_path1, 10, "OCCUPATIONS")

    res = ItemAggregator.get_n_item(input_path, "EMPLOYER_STATE")
    ItemAggregator.save_n_frequent_item(res, output_path2, 10, "STATES")
