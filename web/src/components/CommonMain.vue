<template>
  <div id="common-main">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'CommonMain.vue'
}
</script>

<style scoped lang="scss">
#common-main {
  background: red;
  height: 100px;
  width: 100%;
}
</style>
