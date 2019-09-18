import axios from 'axios';

import httpCommon from './_http-common';
import config from './config.json';

export default {
  addNewTenancy(newTenancy, successCallback, failCallback) {
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
  },
  listTenancies(successCallback, failCallback) {
    axios.get(`${config.apiURL}/tenancy/list`, {
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
};
