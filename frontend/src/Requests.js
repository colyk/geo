import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

export function fetchPath(points = []) {
  return axios.post(`${BASE_URL}/path`, { points });
}
