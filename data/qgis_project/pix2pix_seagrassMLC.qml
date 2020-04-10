<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="1e+08" version="3.4.12-Madeira" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="identify/format" value="Value"/>
  </customproperties>
  <pipe>
    <rasterrenderer band="5" alphaBand="-1" opacity="1" type="paletted">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <colorPalette>
        <paletteEntry alpha="255" value="1" color="#d7191c" label="Base"/>
        <paletteEntry alpha="255" value="10" color="#fdae61" label="10%"/>
        <paletteEntry alpha="255" value="11" color="#ffffbf" label="Base, 10%"/>
        <paletteEntry alpha="255" value="111" color="#abdda4" label="Base, 10%, 20%"/>
        <paletteEntry alpha="255" value="1111" color="#2b83ba" label="Base, 10%, 20%, 50%"/>
      </colorPalette>
      <colorramp name="[source]" type="gradient">
        <prop k="color1" v="215,25,28,255"/>
        <prop k="color2" v="43,131,186,255"/>
        <prop k="discrete" v="0"/>
        <prop k="rampType" v="gradient"/>
        <prop k="stops" v="0.25;253,174,97,255:0.5;255,255,191,255:0.75;171,221,164,255"/>
      </colorramp>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation colorizeGreen="128" grayscaleMode="0" colorizeOn="0" saturation="0" colorizeRed="255" colorizeStrength="100" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
