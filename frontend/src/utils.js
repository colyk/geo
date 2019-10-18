export function getCurrentPosition(options = { enableHighAccuracy: true }) {
  navigator.geolocation.getCurrentPosition(() => {});
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject, options);
  });
}

export function hasCoords(array, coords) {
  for (let i = 0; i < array.length; i++) {
    const c = array[i];
    if (c[0] === coords[0] && c[1] === coords[1]) return true;
  }
  return false;
}
