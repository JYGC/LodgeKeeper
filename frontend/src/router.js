import Vue from 'vue';
import Router from 'vue-router';

import userAPI from './_api/user';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Register from './views/Register.vue';
import About from './views/About.vue';
import TenancyAdd from './views/TenancyAdd.vue';

Vue.use(Router);

const router = new Router({
  mode: 'history',
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
      path: '/tenancy-add',
      name: 'tenancy-add',
      component: TenancyAdd,
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
    {
      path: '*',
      redirect: '/',
    },
  ],
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/register'];
  userAPI.checkAuthenticationAPI(() => {
    if (publicPages.includes(to.path)) {
      next('/');
    } else {
      next();
    }
  }, () => {
    next('/login');
  });

  // NOT UNDERSTOOD
  next();
});

export default router;
