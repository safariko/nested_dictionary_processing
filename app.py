import json
import argparse
from os import path

full_path = path.realpath(__file__)
pathname = path.dirname(full_path)


def create_temp_dict_dep(dependencies_comma_split):
    """The function creates the structure of the final dictionary where the data from orders is filled"""
    temp_dict_dep = {}

    for i in dependencies_comma_split:
        temp_dict_dep.setdefault(i[0], [])
        temp_dict_dep[i[0]].append(i[1])

    first_dim_keys = []

    for e in temp_dict_dep.keys():
        first_dim_keys.append(e)

    remove_temp_dict_dep_list = []

    for first_dim, second_dim in temp_dict_dep.copy().items():
        for c in range(len(second_dim)):
            for d in range(len(first_dim_keys)):
                if second_dim[c] == first_dim_keys[d]:
                    unit_dict = {}
                    unit_dict[second_dim[c]] = temp_dict_dep[first_dim_keys[d]]
                    temp_dict_dep[first_dim][c] = unit_dict
                    remove_temp_dict_dep_list.append(first_dim_keys[d])

    for i in range(len(remove_temp_dict_dep_list)):
        temp_dict_dep.pop(remove_temp_dict_dep_list[i], None)

    return temp_dict_dep




def input_data(orders, dependencies):
    """This function gets data from input files"""

    #open depencies file and store the data in the object

    with open(pathname + '/' + dependencies, 'r') as dependencies_data:
        next(dependencies_data)
        dependencies_txt = dependencies_data.read()

    dependencies_n_split = dependencies_txt.split("\n")
    dependencies_n_split = list(filter(None, dependencies_n_split))
    dependencies_comma_split = []

    for i in dependencies_n_split:
        dependencies_comma_split.append(i.split(","))

    temp_dict_dep = create_temp_dict_dep(dependencies_comma_split)



    #open orders file and store the data in the object

    with open(pathname + '/' + orders, 'r') as orders_data:
        next(orders_data)
        orders_txt = orders_data.read()

    orders_n_split = orders_txt.split("\n")
    orders_n_split = list(filter(None, orders_n_split))
    orders_comma_split = []

    for i in orders_n_split:
        orders_comma_split.append(i.split(","))

    temp_dict_order = {}

    for i in orders_comma_split:
        temp_dict_order[i[0]] = i[1]

    return temp_dict_dep, temp_dict_order


def output_in_json(order_dict):
    """this function output to an external file in json"""
    try:
        json_object = json.dumps(order_dict)
        with open("output.json", "w") as outfile:
            outfile.write(json_object)
    except:
        with open("output.json", "w") as outfile:
            outfile.write("The dictionary is not serializable")



def convert(orders, dependencies):
    """This function puts data into final dictionary in json"""

    temp_dict_dep, temp_dict_order = input_data(orders, dependencies)

    #final dictionary
    order_dict = {}
    order_dict.setdefault("orders", [])

    final_dict_keys = []

    for a in temp_dict_dep.keys():
        final_dict_keys.append(a)


    for i in range(len(temp_dict_dep)):

        #similar to creating a deep copy used for iteration
        temp_dict_dep_copy, _ = input_data(orders, dependencies)

        unit_dict = {}
        unit_dict["id"] = final_dict_keys[i]
        unit_dict["name"] = temp_dict_order[final_dict_keys[i]]
        unit_dict["dependencies"] = temp_dict_dep_copy[final_dict_keys[i]]

        #unpacking dictionary for nested dependencies key on 1st level of depth
        remove_sub_list = []
        for n in range(len(unit_dict["dependencies"])):
            if isinstance((unit_dict["dependencies"][n]), str):
                remove_subunit_value = unit_dict["dependencies"][n]
                subunit_dict = {}
                subunit_dict["id"] = unit_dict["dependencies"][n]
                subunit_dict["name"] = temp_dict_order[(subunit_dict["id"])]
                subunit_dict.setdefault("dependencies", [])
                unit_dict["dependencies"].append(subunit_dict)
                remove_sub_list.append(remove_subunit_value)

            if isinstance(unit_dict["dependencies"][n], dict):
                remove_subunit_value = unit_dict["dependencies"][n]
                subunit_dict = {}
                for key, value in unit_dict["dependencies"][n].items():
                    subunit_dict["id"] = key
                    subunit_dict["name"] = temp_dict_order[key]
                    subunit_dict.setdefault("dependencies", [])
                    subunit_dict["dependencies"] = value
                    unit_dict["dependencies"].append(subunit_dict)
                    remove_sub_list.append(remove_subunit_value)



                    # unpacking dictionary for nested dependencies key on 2nd level of depth
                    remove_sub_subunit_list = []
                    for l in range(len(subunit_dict["dependencies"])):

                        if isinstance((subunit_dict["dependencies"][l]), str):
                            remove_sub_subunit_value = subunit_dict["dependencies"][l]
                            sub_subunit_dict = {}
                            sub_subunit_dict["id"] = subunit_dict["dependencies"][l]
                            sub_subunit_dict["name"] = temp_dict_order[sub_subunit_dict["id"]]
                            sub_subunit_dict.setdefault("dependencies", [])
                            subunit_dict["dependencies"].append(sub_subunit_dict)
                            remove_sub_subunit_list.append(remove_sub_subunit_value)

                        if isinstance(subunit_dict["dependencies"][l], dict):
                            remove_sub_subunit_value = subunit_dict["dependencies"][l]
                            sub_subunit_dict = {}
                            for key, value in subunit_dict["dependencies"][l].items():
                                sub_subunit_dict["id"] = key
                                sub_subunit_dict["name"] = temp_dict_order[key]
                                sub_subunit_dict.setdefault("dependencies", [])
                                sub_subunit_dict["dependencies"] = value
                                subunit_dict["dependencies"].append(sub_subunit_dict)
                                remove_sub_subunit_list.append(remove_sub_subunit_value)


                            # unpacking dictionary for nested dependencies key on 3nd level of depth
                            remove_sub_sub_subunit_list = []
                            for k in range(len(sub_subunit_dict["dependencies"])):

                                if isinstance((sub_subunit_dict["dependencies"][k]), str):
                                    remove_sub_sub_subunit_value = sub_subunit_dict["dependencies"][k]
                                    sub_sub_subunit_dict = {}
                                    sub_sub_subunit_dict["id"] = sub_subunit_dict["dependencies"][k]
                                    sub_sub_subunit_dict["name"] = temp_dict_order[sub_sub_subunit_dict["id"]]
                                    sub_sub_subunit_dict.setdefault("dependencies", [])
                                    sub_subunit_dict["dependencies"].append(sub_sub_subunit_dict)
                                    remove_sub_sub_subunit_list.append(remove_sub_sub_subunit_value)

                                if isinstance(sub_subunit_dict["dependencies"][k], dict):
                                    remove_sub_sub_subunit_value = sub_subunit_dict["dependencies"][k]
                                    sub_sub_subunit_dict = {}
                                    for key, value in sub_subunit_dict["dependencies"][k].items():
                                        sub_sub_subunit_dict["id"] = key
                                        sub_sub_subunit_dict["name"] = temp_dict_order[key]
                                        sub_sub_subunit_dict.setdefault("dependencies", [])
                                        sub_sub_subunit_dict["dependencies"] = value
                                        sub_subunit_dict["dependencies"].append(sub_sub_subunit_dict)
                                        remove_sub_sub_subunit_list.append(remove_sub_sub_subunit_value)


                            #remove extra elements created during unpacking
                            for e in range(len(remove_sub_sub_subunit_list)):
                                sub_subunit_dict["dependencies"].remove(remove_sub_sub_subunit_list[e])


                    #remove extra elements created during unpacking
                    for e in range(len(remove_sub_subunit_list)):
                        subunit_dict["dependencies"].remove(remove_sub_subunit_list[e])

        # remove extra elements created during unpacking
        for e in range(len(remove_sub_list)):
            unit_dict["dependencies"].remove(remove_sub_list[e])

        order_dict["orders"].append(unit_dict)

    output_in_json(order_dict)




def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', dest='orders', required=True, action='store', help='Specify the name of orders file')
    parser.add_argument('-d', dest='dependencies', required=True, action='store', help='Specify the name of dependencies file')

    args = parser.parse_args()

    return convert(args.orders, args.dependencies)


if __name__ == "__main__":

    main()
