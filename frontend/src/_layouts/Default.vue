<template>
  <div>
    <div id="nav">
        <router-link to="/">Home</router-link> |
        <router-link to="/tenancy">Tenancy</router-link> |
        <router-link to="/logout">Logout</router-link>
    </div>
    <slot />
  </div>
</template>
