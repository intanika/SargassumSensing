<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="1e+08" version="3.4.12-Madeira" maxScale="0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0">
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
    <rasterrenderer alphaBand="-1" opacity="1" band="1" type="paletted">
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
        <paletteEntry alpha="255" label="Lb" color="#ffffc0" value="1"/>
        <paletteEntry alpha="255" label="Ls" color="#602c1b" value="2"/>
        <paletteEntry alpha="255" label="Sf" color="#ea3fea" value="3"/>
        <paletteEntry alpha="255" label="Sl" color="#f69053" value="4"/>
        <paletteEntry alpha="255" label="Vm" color="#1a9641" value="5"/>
        <paletteEntry alpha="255" label="Vo" color="#b3df76" value="6"/>
        <paletteEntry alpha="255" label="Wd" color="#0ea2a2" value="7"/>
        <paletteEntry alpha="255" label="Ws" color="#13dede" value="8"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors"/>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeBlue="128" grayscaleMode="0" colorizeStrength="100" saturation="0" colorizeOn="0" colorizeGreen="128" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
