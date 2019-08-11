function getAuthToken() {
  return `Bearer ${localStorage.getItem('token')}`;
}

function tokan() {
  return null;
}

export { getAuthToken, tokan };
