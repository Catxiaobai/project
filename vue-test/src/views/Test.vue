<template>
  <el-container style="height: 100%">
    <el-header height="80px"><inner-header></inner-header></el-header>
    <el-container>
      <el-aside width="auto"><inner-aside></inner-aside></el-aside>
      <inner-tab></inner-tab>
      <el-main>
        <router-view> </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import InnerHeader from '@/components/InnerHeader'
import InnerAside from '@/components/InnerAside'
import InnerTab from '@/components/InnerTab'
export default {
  name: 'Test.vue',
  components: {
    InnerHeader,
    InnerAside,
    InnerTab
  }
}
</script>

<style lang="scss" scoped>
.el-header {
  background-color: #333;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>
