L.ColorPicker = L.Toolbar2.Action.extend({
  options: {
    toolbarIcon: { className: 'leaflet-color-swatch' },
  },

  initialize(map, shape, options) {
    this._map = map;
    this._shape = shape;

    L.setOptions(this, options);
    L.Toolbar2.Action.prototype.initialize.call(this, map, options);
  },

  addHooks() {
    this._shape.setStyle({ color: this.options.color });
    this.disable();
  },

  _createIcon(toolbar, container, args) {
    const colorSwatch = L.DomUtil.create('div');
    let width; let
      height;

    L.Toolbar2.Action.prototype._createIcon.call(this, toolbar, container, args);

    L.extend(colorSwatch.style, {
      backgroundColor: this.options.color,
      width: L.DomUtil.getStyle(this._link, 'width'),
      height: L.DomUtil.getStyle(this._link, 'height'),
      border: `3px solid ${L.DomUtil.getStyle(this._link, 'backgroundColor')}`,
    });

    this._link.appendChild(colorSwatch);

    L.DomEvent.on(this._link, 'click', function () {
      this._map.removeLayer(this.toolbar.parentToolbar);
    }, this);
  },
});
