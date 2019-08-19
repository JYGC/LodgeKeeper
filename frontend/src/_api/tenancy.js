import axios from 'axios';

import httpCommon from './_http-common';
import config from './config.json';

const tenancyAPI = {};

tenancyAPI.addNewTenancy = (newTenancy, successCallback, failCallback) => {
  axios.post(`${config.apiURL}/tenancy/addnew`, newTenancy, {
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

export default tenancyAPI;
