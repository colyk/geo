L.Toolbar2.DrawAction = {
  fromHandler(Handler, defaultToolbarIcon, defaultSubToolbar) {
    return L.Toolbar2.Action.extend({
      options: {
        toolbarIcon: L.extend({}, L.Toolbar2.Action.prototype.options.toolbarIcon, defaultToolbarIcon),
        subToolbar: defaultSubToolbar || L.Toolbar2.Action.prototype.options.subToolbar,
      },

      initialize(map, options) {
        const action = this;

        this._handler = new Handler(map, options);
        this._handler.on('disabled', () => {
          action.disable();
        });

        L.Toolbar2.Action.prototype.initialize.call(this, options);
      },

      enable(e) {
        this._handler.enable();
        L.Toolbar2.Action.prototype.enable.call(this, e);
      },

      disable() {
        this._handler.disable();
        L.Toolbar2.Action.prototype.disable.call(this);
      },

      setOptions(options) {
        this._handler.setOptions(options);
        L.Toolbar2.Action.prototype.setOptions.call(this, options);
      },
    });
  },
};
