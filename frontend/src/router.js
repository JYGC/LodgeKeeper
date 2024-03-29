import Vue from 'vue';
import Router from 'vue-router';

import userAPI from '@/_api/user';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import TenancyListAll from '@/views/TenancyListAll.vue';
import TenancyAdd from '@/views/TenancyAdd.vue';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'tenancy-list-all',
      component: TenancyListAll,
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
  const nextPageIsPublic = publicPages.includes(to.path);
  userAPI.checkAuthenticationAPI(() => {
    if (nextPageIsPublic) {
      next('/');
    } else {
      next();
    }
  }, () => {
    next(nextPageIsPublic ? to.path : '/login');
  });

  // NOT UNDERSTOOD
  next();
});

export default router;
