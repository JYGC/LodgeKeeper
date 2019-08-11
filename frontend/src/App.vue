<template>
  <div id="app">
    <component :is="layout">
      <router-view/>
    </component>
  </div>
</template>

<script>
const default_layout = "default";

export default {
  computed: {
    // If layout not specified in router, assume defualt layout
    layout() {
      return (this.$layout.meta.layout || default_layout) + '-layout';
    }
  }
}
</script>
