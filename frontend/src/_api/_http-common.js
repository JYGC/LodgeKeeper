const httpCommon = {};

httpCommon.getAuthToken = () => `Bearer ${localStorage.getItem('token')}`;

export default httpCommon;
