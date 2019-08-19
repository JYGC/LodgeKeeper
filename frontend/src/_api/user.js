import axios from 'axios';

import httpCommon from './_http-common';
import config from './config.json';

const userAPI = {};

userAPI.checkAuthenticationAPI = (successCallback, failCallback) => {
  axios.get(`${config.apiURL}/user/auth`, {
    headers: {
      Authorization: httpCommon.getAuthToken(),
    },
  })
    .then((response) => {
      successCallback(response);
    })
    .catch((error) => {
      failCallback(error);
    });
};

userAPI.loginAPI = (_email, _password, successCallback, failCallback) => {
  axios.post(`${config.apiURL}/user/login`, {
    email: _email,
    password: _password,
  }, {
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => {
      localStorage.setItem('token', response.data.auth_token);
      successCallback(response);
    })
    .catch((error) => {
      failCallback(error);
    });
};

userAPI.logoutAPI = (successCallback, failCallback) => {
  axios.get(`${config.apiURL}/user/logout`, {
    headers: {
      Authorization: httpCommon.getAuthToken(),
    },
  })
    .then((response) => {
      localStorage.removeItem('token');
      successCallback(response);
    })
    .catch((error) => {
      failCallback(error);
    });
};

export default userAPI;
