import Vue from 'vue';
import Router from 'vue-router';

import { apiCheckAuthentication } from './_api/user'
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Register from './views/Register.vue';

Vue.use(Router);

export default router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/about',
      name: 'about',
      component: About,
    },
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { layout: 'not-logged-in' },
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { layout: 'not-logged-in' },
    },
  ],
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);

  apiCheckAuthentication((isAuthenticated) => {
    if (authRequired && isAuthenticated) {
      next('/login');
    }

    next();
  });
})
