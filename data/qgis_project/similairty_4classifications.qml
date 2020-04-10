<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.8-Madeira" minScale="1e+08" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <rasterrenderer type="paletted" alphaBand="-1" band="1" opacity="1">
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
        <paletteEntry alpha="255" label="MLC" color="#d7191c" value="10"/>
        <paletteEntry alpha="255" label="DTC, MLC" color="#e34731" value="11"/>
        <paletteEntry alpha="255" label="GNDVI" color="#ef7546" value="100"/>
        <paletteEntry alpha="255" label="DTC, GNDVI" color="#fba35c" value="101"/>
        <paletteEntry alpha="255" label="MLC, GNDVI" color="#fec177" value="110"/>
        <paletteEntry alpha="255" label="DTC, MLC, GNDVI" color="#ffda94" value="111"/>
        <paletteEntry alpha="255" label="PCA" color="#fff3b2" value="1000"/>
        <paletteEntry alpha="255" label="DTC, PCA" color="#f2fab3" value="1001"/>
        <paletteEntry alpha="255" label="MLC,PCA" color="#d6ee98" value="1010"/>
        <paletteEntry alpha="255" label="DTC, MLC, PCA" color="#bbe27e" value="1011"/>
        <paletteEntry alpha="255" label="GNDVI, PCA" color="#9bd467" value="1100"/>
        <paletteEntry alpha="255" label="DTC, GNDVI, PCA" color="#70bf5a" value="1101"/>
        <paletteEntry alpha="255" label="MLC, GNDVI, PCA" color="#45ab4d" value="1110"/>
        <paletteEntry alpha="255" label="DTC, MLC, GNDVI, PCA" color="#1a9641" value="1111"/>
      </colorPalette>
      <colorramp type="gradient" name="[source]">
        <prop k="color1" v="215,25,28,255"/>
        <prop k="color2" v="26,150,65,255"/>
        <prop k="discrete" v="0"/>
        <prop k="rampType" v="gradient"/>
        <prop k="stops" v="0.25;253,174,97,255:0.5;255,255,192,255:0.75;166,217,106,255"/>
      </colorramp>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeOn="0" colorizeRed="255" grayscaleMode="0" colorizeBlue="128" colorizeStrength="100" saturation="0" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
