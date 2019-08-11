function getAuthToken () {
  return `Bearer ${localStorage.getItem('token')}`;
}

export { getAuthToken };
