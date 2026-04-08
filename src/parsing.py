def parsing(filename: str):
    drone_count = []
    check_first_line = False
    count_start_hub = 0
    count_end_hub = 0
    lst_zone = ["normal", "blocked", "restricted", "priority"]
    try:
        with open(filename, 'r') as file:
            for number_line, line in enumerate(file, start=1):
                zone = "normal"
                color = "none"
                max_drones = 1
                max_link_capacity = 1
                check_name_zone = []
                name_zone = "none"
                x = 0
                y = 0
                connexion_from = "none"
                connexion_to = "none"
                if line.strip().startswith('#'):
                    continue
                if not check_first_line:
                    if line.strip().startswith('nb_drones'):
                        check_first_line = True
                        if ":" not in line:
                            return (f"ERROR line {number_line}: format is not correct. "
                                    "Should be like this: 'nb_drones: <int>'")
                        drone_count = line.split(":")
                        try:
                            ndrones = int(drone_count[1])
                        except ValueError:
                            return f"ERROR {number_line}: must be integer."
                        if ndrones <= 0:
                            return (f"ERROR {number_line}: number of drones must be strictly "
                                    "positives.")
                    if not check_first_line:
                        return (f"ERROR line {number_line}: config file first line "
                                "must contains number of drones.")
                if (line.strip().startswith("hub")
                    or line.strip().startswith("start_hub")
                   or line.strip().startswith("end_hub")):
                    if line.strip().startswith("start_hub"):
                        if ":" not in line:
                            return (f"ERROR line {number_line}: format is not correct, "
                                    "missing ':'")
                        if count_start_hub > 0:
                            return (f"ERROR line {number_line}: it should be only one start_hub.")
                        else:
                            count_start_hub += 1
                    if line.strip().startswith("end_hub"):
                        if count_end_hub > 0:
                            return (f"ERROR line {number_line}: it should be only one end_hub.")
                        else:
                            count_end_hub += 1
                    if "[" in line and "]" not in line:
                        return f"ERROR line {number_line}: incorrect format for metadata."
                    if "]" in line and "[" not in line:
                        return f"ERROR line {number_line}: incorrect format for metadata."
                    if "[" in line and "]" in line:
                        if line.count("[") > 1 or line.count("]") > 1:
                            return f"ERROR line {number_line}: incorrect format for metadata."
                        pos1 = line.find("[")
                        pos2 = line.find("]")
                        if pos1 > pos2:
                            return f"ERROR line {number_line}: incorrect format for metadata."
                        metadata_str = line[pos1 + 1: pos2]
                        metadata_lst = metadata_str.split(" ")
                        metadata_dct = {}
                        for meta in metadata_lst:
                            if meta.count("=") != 1:
                                return f"ERROR line {number_line}: incorrect format for metadata."
                            key, value = meta.split("=")
                            metadata_dct[key] = value
                        for key, value in metadata_dct.items():
                            if key == 'zone':
                                if value not in lst_zone:
                                    return f"ERROR line {number_line}: invalid zone."
                                zone = value
                            if key == "max_drones":
                                try:
                                    n = int(metadata_dct["max_drones"])
                                    if n <= 0:
                                        return f"ERROR line {number_line}: max_drones value should be a positif integer."
                                except ValueError:
                                    return (f"ERROR line {number_line}: max_drones value should be an integer.")
                                max_drones = value
                            else:
                                max_drones = 1
                            if key == "max_link_capacity":
                                try:
                                    n = int(metadata_dct["max_link_capacity"])
                                    if n <= 0:
                                        return f"ERROR line {number_line}: max_link_capacity value should be a positif integer."
                                except ValueError:
                                    return (f"ERROR line {number_line}: max_link_capacity value should be an integer.")
                                max_link_capacity = value
                            if key == "color":
                                if not value.isalpha():
                                    return f"ERROR line {number_line}: color name should be a valid color in one word."
                                color = value
                        main_part = line[:pos1].strip()
                    else:
                        main_part = line.strip()
                    main_part_data = main_part.split(":")
                    main_part_data_lst = main_part_data[1].strip().split(" ")
                    if len(main_part_data_lst) != 3:
                        return f"ERROR line {number_line}: should only name's zone, x and y."
                    if main_part_data_lst[0] in check_name_zone:
                        return f"ERROR line {number_line}: name zone already used."
                    if not main_part_data_lst[0].isalnum():
                        return f"ERROR line {number_line}: name's zone containts invalid charaters." 
                    else:
                        name_zone = main_part_data_lst[0]
                        check_name_zone.append(name_zone)
                    try:
                        x = int(main_part_data_lst[1])
                        y = int(main_part_data_lst[2])
                    except ValueError:
                        return f"ERROR line {number_line}: coordinates should be interger."
                    print(name_zone, x, y, zone, color, max_drones)
                if line.strip().startswith("connection"):
                    if ":" not in line:
                        return (f"ERROR line {number_line}: format is not correct, "
                                    "missing ':'")
                    if "[" in line and "]" not in line:
                        return f"ERROR line {number_line}: incorrect format for metadata."
                    if "]" in line and "[" not in line:
                        return f"ERROR line {number_line}: incorrect format for metadata."
                    if "[" in line and "]" in line:
                        if line.count("[") > 1 or line.count("]") > 1:
                            return f"ERROR line {number_line}: incorrect format for metadata."
                        pos1 = line.find("[")
                        pos2 = line.find("]")
                        if pos1 > pos2:
                            return f"ERROR line {number_line}: incorrect format for metadata."
                        metadata_str = line[pos1 + 1: pos2]
                        metadata_lst = metadata_str.split(" ")
                        metadata_dct = {}
                        for meta in metadata_lst:
                            if meta.count("=") != 1:
                                return f"ERROR line {number_line}: incorrect format for metadata."
                            key, value = meta.split("=")
                            metadata_dct[key] = value
                        for key, value in metadata_dct.items():
                            if key == "max_link_capacity":
                                try:
                                    n = int(metadata_dct["max_link_capacity"])
                                    if n <= 0:
                                        return f"ERROR line {number_line}: max_link_capacity value should be a positif integer."
                                except ValueError:
                                    return (f"ERROR line {number_line}: max_link_capacity value should be an integer.")
                                max_link_capacity = value                             
                        main_part = line[:pos1].strip()
                    else:
                        max_link_capacity = 1
                        main_part = line.strip()
                    main_part_data = main_part.split(":")
                    main_part_data_lst = main_part_data[1].strip().split("-")
                    if len(main_part_data_lst) != 2:
                        return f"ERROR line {number_line}: should only connexion between two zones."
                    if (main_part_data_lst[0] not in check_name_zone 
                        or main_part_data_lst[1] not in check_name_zone):
                        return f"ERROR line {number_line}: unknown zone."
                    if (not main_part_data_lst[0].isalnum() 
                        or not main_part_data_lst[1].isalnum()):
                        return f"ERROR line {number_line}: name's zone containts invalid charaters." 
                    else:
                        connexion_from = main_part_data_lst[0]
                        connexion_to = main_part_data_lst[1]
                    print(connexion_from, connexion_to, max_link_capacity)
            if count_start_hub == 0:
                return (f"ERROR line {number_line}: should be one start_hub.")
            if count_end_hub == 0:
                return (f"ERROR line {number_line}: should be one end_hub.")
    except FileNotFoundError as e:
        return f"ERROR {e}"
    
if __name__ == '__main__':
    print(parsing("test.txt"))
