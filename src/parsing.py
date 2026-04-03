def parsing(filename: str):
    drone_count = []
    check_first_line = False
    count_start_hub = 0
    count_end_hub = 0
    lst_zone = ["normal", "blocked", "restricted", "priority"]
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip().startswith('#'):
                    continue
                if not check_first_line:
                    if line.strip().startswith('nb_drones:'):
                        check_first_line = True
                        if ":" not in line:
                            return ("ERROR: format is not correct. "
                                    "Should be like this: 'nb_drones: <int>'")
                        drone_count = line.split(":")
                        try:
                            ndrones = int(drone_count[1])
                        except ValueError:
                            return "ERROR: must be integer."
                        if ndrones <= 0:
                            return ("ERROR: number of drones must be strictly "
                                    "positives")
                    if not check_first_line:
                        return ("ERROR: config file first line "
                                "must contains number of drones")
                if (line.strip().startswith("hub:")
                    or line.strip().startswith("start_hub:")
                   or line.strip().startswith("end_hub:")):
                    if line.strip().startswith("start_hub:"):
                        if count_start_hub > 0:
                            return ("ERROR: it should be only one start_hub")
                        else:
                            count_start_hub += 1
                    if line.strip().startswith("end_hub:"):
                        if count_end_hub > 0:
                            return ("ERROR: it should be only one end_hub")
                        else:
                            count_end_hub += 1
                    zone = "normal"
                    color = "none"
                    max_drones = 1
                    if "[" in line and "]" not in line:
                        return "ERROR: incorrect format for metadata"
                    if "]" in line and "[" not in line:
                        return "ERROR: incorrect format for metadata"
                    if "[" in line and "]" in line:
                        if line.count("[") > 1 or line.count("]") > 1:
                            return "ERROR: incorrect format for metadata"
                        pos1 = line.find("[")
                        pos2 = line.find("]")
                        if pos1 > pos2:
                            return "ERROR: incorrect format for metadata"
                        metadata_str = line[pos1 + 1: pos2]
                        metadata_lst = metadata_str.split(" ")
                        metadata_dct = {}
                        for meta in metadata_lst:
                            if meta.count("=") != 1:
                                return "ERROR: incorrect format for metadata"
                            key, value = meta.split("=")
                            metadata_dct[key] = value
                        # début partie pas correcte
                        if (metadata_dct["zone"] and metadata_dct["zone"] 
                           not in lst_zone):
                            return "ERROR: invalid zone."
                        if (metadata_dct["max_drones"] and 
                           int(metadata_dct["max_drones"]) <= 0):
                            return "ERROR: invalid number of drones."
                        # fin partie pas correcte         
            if count_start_hub == 0:
                return ("ERROR: should be one start_hub.")
            if count_end_hub == 0:
                return ("ERROR: should be one end_hub.")

    except FileNotFoundError as e:
        return f"ERROR {e}"


if __name__ == '__main__':
    print(parsing("test.txt"))