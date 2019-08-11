<template>
  <div id="login">
    <h1>Login</h1>
    <input type="text" name="email" v-model="input.username" placeholder="email" />
    <input type="password" name="password" v-model="input.password" placeholder="Password" />
    <button type="button" v-on:click="login()">Login</button>
  </div>
</template>

<script>
import { apiLogin } from '../_api/user';

export default {
  name: 'login',
  data() {
    return {
      input: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    login() {
      const thisObj = this;
      if (thisObj.input.email !== '' && thisObj.input.password !== '') {
        apiLogin(thisObj.input.email, thisObj.input.password, () => {
          thisObj.$router.push('home');
        }, () => {
          console.log('A email or password is wrong');
        });
      } else {
        console.log('A email and password must be present');
      }
    },
  },
};
</script>
