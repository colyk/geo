export function getCurrentPosition(options = { enableHighAccuracy: true }) {
  navigator.geolocation.getCurrentPosition(() => {});
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject, options);
  });
}
