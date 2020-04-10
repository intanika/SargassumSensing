<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.12-Madeira" hasScaleBasedVisibilityFlag="0" minScale="1e+08" styleCategories="AllStyleCategories" maxScale="0">
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
    <rasterrenderer band="1" opacity="1" type="paletted" alphaBand="-1">
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
        <paletteEntry label="Seaweed float" color="#ea3fea" value="3" alpha="255"/>
        <paletteEntry label="Seaweed land" color="#f69053" value="4" alpha="255"/>
        <paletteEntry label="Water shallow" color="#13dede" value="8" alpha="255"/>
        <paletteEntry label="Water deep" color="#0ea2a2" value="7" alpha="255"/>
        <paletteEntry label="Land beach" color="#ffffbf" value="1" alpha="255"/>
        <paletteEntry label="Land soil" color="#602c1b" value="2" alpha="255"/>
        <paletteEntry label="Vegetation mangrove" color="#1a9641" value="5" alpha="255"/>
        <paletteEntry label="Vegetation other" color="#b3df76" value="6" alpha="255"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors"/>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeBlue="128" saturation="0" colorizeOn="0" colorizeGreen="128" colorizeStrength="100" grayscaleMode="0" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
