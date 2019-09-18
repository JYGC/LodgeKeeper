export default {
  /**
   *  Get auth token and append it to the string 'Bearer '
   */
  getAuthToken() {
    return `Bearer ${localStorage.getItem('token')}`;
  },
};
