class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.drone_count = 0
        self.check_name_zone = []
        self.zones = {}
        self.connections = []

    def _is_valid_zone_name(self, name: str) -> bool:
        return name != "" and " " not in name and "-" not in name

    def _extract_metadata(self, line, number_line) -> tuple[str, dict]:
        if "[" in line and "]" not in line:
            raise ValueError(f"ERROR line {number_line}: incorrect format for "
                             "metadata.")
        if "]" in line and "[" not in line:
            raise ValueError(f"ERROR line {number_line}: incorrect format for "
                             "metadata.")
        if "[" in line and "]" in line:
            if line.count("[") > 1 or line.count("]") > 1:
                raise ValueError(f"ERROR line {number_line}: incorrect format "
                                 "for metadata.")
            pos1 = line.find("[")
            pos2 = line.find("]")
            if pos1 > pos2:
                raise ValueError(f"ERROR line {number_line}: incorrect format "
                                 "for metadata.")
            metadata_str = line[pos1 + 1: pos2]
            metadata_lst = metadata_str.split()
            metadata_dct = {}
            for meta in metadata_lst:
                if meta.count("=") != 1:
                    raise ValueError(f"ERROR line {number_line}: incorrect "
                                     "format for metadata.")
                key, value = meta.split("=")
                metadata_dct[key] = value
            main_part = line[:pos1].strip()
        else:
            metadata_dct = {}
            main_part = line.strip()
        return main_part, metadata_dct

    def _get_zone_metadata(self, metadata_dct, number_line, lst_zone,
                           zone_type, color,
                           max_drones) -> tuple:
        for key, value in metadata_dct.items():
            if key == 'zone':
                if value not in lst_zone:
                    raise ValueError(f"ERROR line {number_line}: invalid "
                                     "zone.")
                zone_type = value
            elif key == "max_drones":
                try:
                    n = int(value)
                    if n <= 0:
                        raise ValueError
                except ValueError:
                    raise ValueError(f"ERROR line {number_line}: max_drones "
                                     "value should be a positif integer.")
                max_drones = n
            elif key == "color":
                if not value.isalpha():
                    raise ValueError(f"ERROR line {number_line}: color name "
                                     "should be a valid color in one word.")
                color = value
        return zone_type, color, max_drones

    def parsing(self) -> dict:
        file_has_content = False
        check_first_line = False
        lst_zone = ["normal", "blocked", "restricted", "priority"]
        seen_connexion = []
        count_start_hub = 0
        count_end_hub = 0
        try:
            with open(self.filename, 'r') as file:
                for number_line, line in enumerate(file, start=1):
                    zone_type = "normal"
                    color = "none"
                    max_drones = 1
                    max_link_capacity = 1
                    name_zone = "none"
                    x = 0
                    y = 0
                    connexion_from = "none"
                    connexion_to = "none"
                    stripped_line = line.strip()
                    if not stripped_line or stripped_line.startswith('#'):
                        continue
                    file_has_content = True
                    if not check_first_line:
                        if stripped_line.startswith('nb_drones'):
                            check_first_line = True
                            if ":" not in line:
                                raise ValueError(f"ERROR line {number_line}: "
                                                 "format is not correct. "
                                                 "Should be like this: "
                                                 "'nb_drones: <int>'")
                            parts = line.split(":")
                            if len(parts) != 2:
                                raise ValueError(f"ERROR line {number_line}: "
                                                 "format is not correct. "
                                                 "Should be like this: "
                                                 "'nb_drones: <int>'")
                            try:
                                ndrones = int(parts[1].strip())
                            except ValueError:
                                raise ValueError(f"ERROR line {number_line}: "
                                                 "must be integer.")
                            if ndrones <= 0:
                                raise ValueError(f"ERROR line {number_line}: "
                                                 "number of drones must be "
                                                 "strictly positive.")
                            self.drone_count = ndrones
                        if not check_first_line:
                            raise ValueError(f"ERROR line {number_line}: the "
                                             "first line of the config file "
                                             "must contains number of drones.")
                    if (stripped_line.startswith("hub")
                        or stripped_line.startswith("start_hub")
                       or stripped_line.startswith("end_hub")):
                        if ":" not in line:
                            raise ValueError(f"ERROR line {number_line}: "
                                             "format is not correct, "
                                             "missing ':'")
                        if stripped_line.startswith("start_hub"):
                            if count_start_hub > 0:
                                raise ValueError(f"ERROR line {number_line}: "
                                                 "it should be only one "
                                                 "start_hub.")
                            else:
                                count_start_hub += 1
                        if stripped_line.startswith("end_hub"):
                            if count_end_hub > 0:
                                raise ValueError(f"ERROR line {number_line}: "
                                                 "it should be only one "
                                                 "end_hub.")
                            else:
                                count_end_hub += 1
                        main_part, metadata_dct = self._extract_metadata(
                            line,
                            number_line
                            )
                        zone_type, color, max_drones = self._get_zone_metadata(
                            metadata_dct,
                            number_line,
                            lst_zone,
                            zone_type,
                            color,
                            max_drones
                        )
                        main_part_data = main_part.split(":")
                        main_part_data_lst = main_part_data[1].strip().split()
                        if len(main_part_data_lst) != 3:
                            raise ValueError(f"ERROR line {number_line}: zone "
                                             "must have exactly: name x y.")
                        if main_part_data_lst[0] in self.check_name_zone:
                            raise ValueError(f"ERROR line {number_line}: name "
                                             "of zone already used.")
                        name = main_part_data_lst[0]
                        if not self._is_valid_zone_name(name):
                            raise ValueError(f"ERROR line {number_line}: "
                                             "name's zone contains invalid "
                                             "characters.")
                        else:
                            name_zone = main_part_data_lst[0]
                            self.check_name_zone.append(name_zone)
                        try:
                            x = int(main_part_data_lst[1])
                            y = int(main_part_data_lst[2])
                        except ValueError:
                            raise ValueError(f"ERROR line {number_line}: "
                                             "coordinates should be interger.")
                        self.zones[name_zone] = {
                            "hub_type": main_part_data[0].strip(),
                            "x": x,
                            "y": y,
                            "zone": zone_type,
                            "color": color,
                            "max_drones": max_drones,
                        }
                    if stripped_line.startswith("connection"):
                        if ":" not in line:
                            raise ValueError(f"ERROR line {number_line}: "
                                             "format is not correct, "
                                             "missing ':'")
                        if "[" in line and "]" not in line:
                            raise ValueError(f"ERROR line {number_line}: "
                                             "incorrect format for metadata.")
                        if "]" in line and "[" not in line:
                            raise ValueError(f"ERROR line {number_line}: "
                                             "incorrect format for metadata.")
                        if "[" in line and "]" in line:
                            if line.count("[") > 1 or line.count("]") > 1:
                                raise ValueError(f"ERROR line {number_line}: "
                                                 "incorrect format for "
                                                 "metadata.")
                            pos1 = line.find("[")
                            pos2 = line.find("]")
                            if pos1 > pos2:
                                raise ValueError(f"ERROR line {number_line}: "
                                                 "incorrect format for "
                                                 "metadata.")
                            metadata_str = line[pos1 + 1: pos2]
                            metadata_lst = metadata_str.split()
                            metadata_dct = {}
                            for meta in metadata_lst:
                                if meta.count("=") != 1:
                                    raise ValueError("ERROR line "
                                                     f"{number_line}: "
                                                     "incorrect format for "
                                                     "metadata.")
                                key, value = meta.split("=")
                                metadata_dct[key] = value
                            for key, value in metadata_dct.items():
                                if key == "max_link_capacity":
                                    try:
                                        n = int(
                                            metadata_dct["max_link_capacity"]
                                            )
                                        if n <= 0:
                                            raise ValueError(
                                                "ERROR line "
                                                f"{number_line}: "
                                                "max_link_capacity "
                                                "value should be a "
                                                "positif integer."
                                                )
                                    except ValueError:
                                        raise ValueError("ERROR line "
                                                         f"{number_line}: "
                                                         "max_link_capacity "
                                                         "value should be an "
                                                         "integer.")
                                    max_link_capacity = n
                            main_part = line[:pos1].strip()
                        else:
                            main_part = stripped_line
                        main_part_data = main_part.split(":")
                        if len(main_part_data) != 2:
                            raise ValueError(f"ERROR line {number_line}: "
                                             "incorrect connection format.")
                        main_part_data_lst = (main_part_data[1].
                                              strip().split("-"))
                        if len(main_part_data_lst) != 2:
                            raise ValueError(f"ERROR line {number_line}: "
                                             "should be connexion between two "
                                             "zones.")
                        if (main_part_data_lst[0] not in self.check_name_zone
                           or main_part_data_lst[1]
                           not in self.check_name_zone):
                            raise ValueError(f"ERROR line {number_line}: "
                                             "unknown zone.")
                        name1 = main_part_data_lst[0]
                        name2 = main_part_data_lst[1]
                        if (not self._is_valid_zone_name(name1)
                           or not self._is_valid_zone_name(name2)):
                            raise ValueError(f"ERROR line {number_line}: "
                                             "name's zone contains invalid "
                                             "characters.")
                        else:
                            connexion_from = main_part_data_lst[0]
                            connexion_to = main_part_data_lst[1]
                        check_dup = {connexion_from, connexion_to}
                        if check_dup in seen_connexion:
                            raise ValueError(f"ERROR line {number_line}: "
                                             "a connexion cannot exist twice.")
                        else:
                            seen_connexion.append(check_dup)
                        self.connections.append({
                                        "from": connexion_from,
                                        "to": connexion_to,
                                        "max_link_capacity": max_link_capacity,
                                    })
                if not file_has_content:
                    raise ValueError("ERROR: file is empty or contains "
                                     "only comments.")
                if count_start_hub == 0:
                    raise ValueError("ERROR: should be one start_hub.")
                if count_end_hub == 0:
                    raise ValueError("ERROR: should be one end_hub.")
        except FileNotFoundError:
            raise ValueError("ERROR: file does not exist.")
        return {
                "nb_drones": self.drone_count,
                "zones": self.zones,
                "connections": self.connections,
            }
