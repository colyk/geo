L.Toolbar2.EditAction.Control.Save = L.Toolbar2.Action.extend({
  options: {
    toolbarIcon: { html: 'Save' },
  },
  initialize(map, featureGroup, editing) {
    this.editing = editing;
    L.Toolbar2.Action.prototype.initialize.call(this);
  },
  addHooks() {
    this.editing.save();
    this.editing.disable();
  },
});
