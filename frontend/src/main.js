import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

import Default from './_layouts/Default.vue';
import NotLoggedIn from './_layouts/NotLoggedIn.vue';

Vue.component('default-layout', Default);
Vue.component('not-logged-in-layout', NotLoggedIn);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
