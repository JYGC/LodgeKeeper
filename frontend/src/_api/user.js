import axios from 'axios';

import { getAuthToken } from './_http-common';
import config from './config.json';

function apiCheckAuthentication(successCallback, failCallback) {
  axios.get(`${config.apiURL}/user/auth`, {
    headers: {
      Authorization: getAuthToken(),
    },
  })
    .then((response) => {
      console.log(response);
      successCallback();
    })
    .catch((error) => {
      console.log(error);
      failCallback();
    });
}

function apiLogin(_email, _password, successCallback, failCallback) {
  axios.post(`${config.apiURL}/user/login`, {
    email: _email,
    password: _password,
  }, {
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => {
      console.log(response);
      localStorage.setItem('token', response.data.auth_token);
      successCallback(response);
    })
    .catch((error) => {
      failCallback(error);
    });
}

function apiLogout(successCallback, failCallback) {
  axios.get(`${config.apiURL}/user/logout`, {
    headers: {
      Authorization: getAuthToken(),
    },
  })
    .then((response) => {
      console.log(response);
      localStorage.removeItem('token');
      successCallback(response);
    })
    .catch((error) => {
      failCallback(error);
    });
}

export { apiCheckAuthentication, apiLogin, apiLogout };
