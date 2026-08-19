# sciflex-cor-parser

`sciflex-cor-parser` reads sciFLEX correction data from a `.cor` file or a
compatible `.log` file. It recognizes the speed/deviation row, all configured
correction attributes, and preserves unknown `label=value` entries in
`extra_attributes`. It has no runtime dependencies.

## Install

```bash
python3 -m pip install git+https://github.com/zcays/sciflex-cor-parser.git
```

## Use

```python
from sciflex_cor_parser import CorFile

filename = "/path/to/example.cor"
cor_data = CorFile.from_file(filename)

# Print the full report
cor_data.print_attributes()
```

### Access specific attributes

```python
print(cor_data.speed)
print(cor_data.deviation)
print(cor_data.well_number)
print(cor_data.nozzle_number)
print(cor_data.camera_position)
print(cor_data.nozzle_z_offset)
print(cor_data.x_axis_position)
print(cor_data.y_axis_position)
print(cor_data.z_axis_position)
print(cor_data.nozzle_voltage)
print(cor_data.nozzle_pulse)
print(cor_data.frequency)
print(cor_data.drop_volume)
print(cor_data.volume_stdev)
print(cor_data.extra_attributes)
```

## Error handling

```python
from sciflex_cor_parser import CorFile

try:
    cor_data = CorFile.from_file("/path/to/example.cor")
except ValueError as error:
    print("Invalid file:", error)
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Permission denied")
except OSError as error:
    print("Could not read file:", error)
```
