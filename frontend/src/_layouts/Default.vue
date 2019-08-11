<template>
  <div>
    <div id="nav">
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> |
        <div class="btn" v-on:click="logout()">Logout</div>
    </div>
    <slot />
  </div>
</template>

<script>
import { apiLogout } from '../_api/user';

export default {
  methods: {
    logout() {
      const vm = this;
      apiLogout(() => {
        vm.$router.push('/login');
      }, () => {
        console.log('Logout failure');
      });
    },
  },
}
</script>
