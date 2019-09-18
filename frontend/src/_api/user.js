import axios from 'axios';

import httpCommon from './_http-common';
import config from './config.json';

export default {
  checkAuthenticationAPI(successCallback, failCallback) {
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
  },
  loginAPI(_email, _password, successCallback, failCallback) {
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
  },
  logoutAPI(successCallback, failCallback) {
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
  },
};
