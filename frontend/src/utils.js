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


function degreesToRadians(degrees) {
  return degrees * Math.PI / 180;
}

function d(coord1, coord2) {
  let [lat1, lon1] = coord1;
  let [lat2, lon2] = coord2;
  const earthRadiusKm = 6371;

  const dLat = degreesToRadians(lat2 - lat1);
  const dLon = degreesToRadians(lon2 - lon1);

  lat1 = degreesToRadians(lat1);
  lat2 = degreesToRadians(lat2);

  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2)
          + Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return earthRadiusKm * c;
}

export function distance(path) {
  let pathLength = 0;
  for (let i = 0; i < path.length - 1; i++) pathLength += d(path[i], path[i + 1]);
  return pathLength;
}

export function distanceToWalkTime(kmDistance) {
  const averageMetresInSecondSpeed = 1.4;
  const mDistance = kmDistance * 1000;
  const seconds = mDistance / averageMetresInSecondSpeed;
  let minutes = Math.round(seconds / 60);
  minutes = minutes >= 1 ? minutes : minutes + 1;
  return `${minutes} minutes`;
}
