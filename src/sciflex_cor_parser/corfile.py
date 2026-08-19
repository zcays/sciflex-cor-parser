"""Parser for sciFLEX .cor files and compatible .log files."""

class CorFile:
    ATTRIBUTE_MAP = {
        "Well No.": ("well_number", str),
        "Nozzle No.": ("nozzle_number", int),
        "Camera Position": ("camera_position", int),
        "Nozzle Z Offset": ("nozzle_z_offset", int),
        "X Axis Position": ("x_axis_position", int),
        "Y Axis Position": ("y_axis_position", int),
        "Z Axis Position": ("z_axis_position", int),
        "Nozzle Voltage [V]": ("nozzle_voltage", float),
        "Nozzle Pulse [µs]": ("nozzle_pulse", str),
        "Frequency [Hz]": ("frequency", float),
        "Drop Volume [pl]": ("drop_volume", float),
        "Volume StDev [%]": ("volume_stdev", float),
    }

    def __init__(self):
        self.speed = None
        self.deviation = None

        self.well_number = None
        self.nozzle_number = None
        self.camera_position = None
        self.nozzle_z_offset = None
        self.x_axis_position = None
        self.y_axis_position = None
        self.z_axis_position = None
        self.nozzle_voltage = None
        self.nozzle_pulse = None
        self.frequency = None
        self.drop_volume = None
        self.volume_stdev = None


        self.extra_attributes = {}

    @classmethod
    def from_file(cls, filename):
        lower_filename = filename.lower()

        if not (
            lower_filename.endswith(".cor")
            or lower_filename.endswith(".log")
        ):
            raise ValueError("File must be a .cor or .log file")

        result = cls()

        with open(filename, "r", encoding="utf-8", errors="replace") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                # Ignore blank lines and the random-number line.
                if not line or line.startswith("§"):
                    continue

                # Recognize the speed and deviation data row.
                if "\t" in line and "=" not in line:
                    columns = line.split("\t")

                    if len(columns) >= 2:
                        try:
                            result.speed = float(columns[0].strip())
                            result.deviation = float(columns[1].strip())
                        except ValueError:
                            # This is probably the column-header row.
                            pass

                    continue

                # Recognize attribute=value lines.
                if "=" not in line:
                    continue

                label, raw_value = line.split("=", 1)
                label = label.strip()
                raw_value = raw_value.strip()

                if label in cls.ATTRIBUTE_MAP:
                    attribute_name, value_type = cls.ATTRIBUTE_MAP[label]

                    try:
                        value = value_type(raw_value)
                    except ValueError:
                        print(
                            "Invalid value on line "
                            + str(line_number)
                            + ": "
                            + line
                        )
                        continue

                    setattr(result, attribute_name, value)

                else:
                    # Keep attributes that are not yet in ATTRIBUTE_MAP.
                    result.extra_attributes[label] = cls.infer_value(
                        raw_value
                    )

        return result

    @staticmethod
    def infer_value(value):
        """Try to recognize integers, decimals, and text."""
        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            return value

    def print_attributes(self):
        attribute_names = [
            "speed",
            "deviation",
            "well_number",
            "nozzle_number",
            "camera_position",
            "nozzle_z_offset",
            "x_axis_position",
            "y_axis_position",
            "z_axis_position",
            "nozzle_voltage",
            "nozzle_pulse",
            "frequency",
            "drop_volume",
            "volume_stdev",
        ]

        for attribute_name in attribute_names:
            value = getattr(self, attribute_name)

            if value is not None:
                print(attribute_name + " = " + str(value))

        for attribute_name, value in self.extra_attributes.items():
            print(attribute_name + " = " + str(value))
