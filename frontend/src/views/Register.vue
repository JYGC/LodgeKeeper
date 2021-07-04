<template>
  <div id="register">
    <h1>Register</h1>
    <input type="text" name="email" v-model="input.email" placeholder="email" />
    <input type="text" name="address" v-model="input.address" placeholder="address" />
    <input type="tel" name="phone" v-model="input.phone" placeholder="phone"
     pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}" />
    <input type="password" name="password" v-model="input.password"
     placeholder="Password" />
    <!-- <input type="password" name="confirm password" v-model="input.confirm_password"
     placeholder="Password" /> -->
    <div class="btn" v-on:click="register()">Register</div>
  </div>
</template>

<script>
import userAPI from '../_api/user';

export default {
  name: 'register',
  data() {
    return {
      input: {
        email: '',
        address: '',
        phone: '',
        password: '',
      },
    };
  },
  methods: {
    register() {
      const vm = this;
      if (vm.input.email !== '' && vm.input.address !== '' && vm.input.phone !== '' && vm.input.password !== '') {
        userAPI.registerAPI(vm.input.email, vm.input.address, vm.input.phone, vm.input.password,
          () => {
            vm.$router.push('/home');
          }, () => {
            console.log('Registration failed. Contact admin.');
          });
      } else {
        console.log('A email, address, phone and password must be present');
      }
    },
  },
};
</script>
