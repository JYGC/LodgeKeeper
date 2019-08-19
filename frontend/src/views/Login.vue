<template>
  <div id="login">
    <h1>Login</h1>
    <input type="text" name="email" v-model="input.email" placeholder="email" />
    <input type="password" name="password" v-model="input.password" placeholder="Password" />
    <div class="btn" v-on:click="login()">Login</div>
  </div>
</template>

<script>
import userAPI from '../_api/user';

export default {
  name: 'login',
  data() {
    return {
      input: {
        email: '',
        password: '',
      },
    };
  },
  methods: {
    login() {
      const vm = this;
      if (vm.input.email !== '' && vm.input.password !== '') {
        userAPI.loginAPI(vm.input.email, vm.input.password, () => {
          vm.$router.push('/home');
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
