import axios from 'axios';

import { getAuthToken } from './_http-common';
import config from './config.json';

function apiCheckAuthentication(callback) {
  axios.get(`${config.apiURL}/user/auth`, {
    headers: {
      Authorization: getAuthToken(),
    },
  })
    .then((response) => {
      console.log(response);
      callback(response.data.status === 'success');
    })
    .catch((error) => {
      console.log(error);
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
      if (typeof response.data.auth_token === 'string' && response.status === 201) {
        localStorage.setItem('token', response.auth_token);
        successCallback(response);
      } else {
        failCallback(response);
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

export { apiCheckAuthentication, apiLogin };
