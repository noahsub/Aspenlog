# Snow and Wind Constants

## RoofType (Enum)
- `UNOBSTRUCTED_SLIPPERY_ROOF`: Represents unobstructed slippery roofs.
- `OTHER`: Represents all other roof types.

## WindExposureFactorSelections (Enum)
- `OPEN`: Open areas with minimal obstruction to wind.
- `ROUGH`: Areas with rough terrain or obstructions.
- `INTERMEDIATE`: Intermediate conditions between open and rough.

## InternalPressureSelections (Enum)
- `ENCLOSED`: Completely enclosed structures.
- `PARTIALLY_ENCLOSED`: Partially enclosed with openings.
- `LARGE_OPENINGS`: Structures with large open areas.

## WindImportanceFactor (Enum)
- `ULS_LOW`, `ULS_NORMAL`, `ULS_HIGH`, `ULS_POST_DISASTER`: Ultimate Limit State factors for various building importance levels.
- `SLS_LOW`, `SLS_NORMAL`, `SLS_HIGH`, `SLS_POST_DISASTER`: Service Limit State factors for various building importance levels.

## SnowImportanceFactor (Enum)
- `ULS_LOW`, `ULS_NORMAL`, `ULS_HIGH`, `ULS_POST_DISASTER`: Ultimate Limit State factors for snow loading.
- `SLS_LOW`, `SLS_NORMAL`, `SLS_HIGH`, `SLS_POST_DISASTER`: Service Limit State factors for snow loading.

## SeismicImportanceFactor (Enum)
- `ULS_LOW`, `ULS_NORMAL`, `ULS_HIGH`, `ULS_POST_DISASTER`: Ultimate Limit State factors for seismic impacts.
- `SLS_LOW`, `SLS_NORMAL`, `SLS_HIGH`, `SLS_POST_DISASTER`: Service Limit State factors for seismic impacts.

_Note: These constants are used in calculations to determine various loads on structures._
