# Entities
## Building Entities
_These classes are used to model the physical attributes of a building for load calculations._

### Dimensions Class
- Represents the height and width of a structure.
- `height`: Float, vertical dimension of the building.
- `width`: Float, horizontal dimension of the building.

### Cladding Class
- Defines cladding factors for the top and bottom of a structure.
- `c_top`: Float, cladding factor for the top.
- `c_bot`: Float, cladding factor for the bottom.

### Roof Class
- Represents various attributes of a building's roof.
- `w_roof`: Float, width of the roof.
- `l_roof`: Float, length of the roof.
- `slope`: Float, slope angle of the roof.

### Building Class
- Main class representing a building with dimensions, cladding, and roof.
- `dimensions`: Instance of Dimensions class.
- `cladding`: Instance of Cladding class.
- `roof`: Instance of Roof class.
- `hz_num`: Integer, hazard number for the building.
- `h_opening`: Float, height of openings in the building.

## Snow Entities

### SnowFactor Class
- Represents the factors influencing snow load on a structure.
- `cs`: Float, slope factor of the snow load.
- `ca`: Float, accumulation factor of the snow load.
- `cw`: Float, wind exposure factor for the snow load.
- `cb`: Float, basic roof snow load factor.

### SnowLoad Class
- Models the snow load on a structure.
- `factor`: Instance of SnowFactor class, encapsulating various snow load factors.
- `s`: Float, total calculated snow load on the structure.

## Wind Entities

### WindFactor Class
- Represents the factors affecting wind load on a structure.
- `ct`: Float, topographic factor.
- `ce`: Float, wind exposure factor.
- `cei`: Float, internal wind exposure factor.
- `cg`: Float, gust factor.

### WindPressure Class
- Models the wind pressure on different zones of a building.
- `pi_pos`: Float, positive internal pressure.
- `pi_neg`: Float, negative internal pressure.
- `pe_pos`: Float, positive external pressure.
- `pe_neg`: Float, negative external pressure.

### Zone Class
- Represents a specific zone of a building for wind load analysis.
- `name`: String, name of the zone.
- `num`: Integer, number identifier for the zone.
- `pressure`: Instance of WindPressure class.
- `wind_load`: Float, calculated wind load for the zone.

### WindLoad Class
- Main class for modeling wind load on a structure.
- `factor`: Instance of WindFactor class.
- `pressure`: Instance of WindPressure class.
- `zones`: Set of Zone objects, representing different parts of the building.

