<template>
  <el-container style="height: 100%">
    <el-header height="80px"><common-header></common-header></el-header>
    <el-container>
      <el-aside width="auto"><common-aside></common-aside></el-aside>
      <common-tab></common-tab>
      <el-main>
        <router-view> </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import CommonHeader from '@/components/CommonHeader'
import CommonAside from '@/components/CommonAside'
import CommonTab from '@/components/CommonTab'
export default {
  name: 'Main.vue',
  components: {
    CommonHeader,
    CommonAside,
    CommonTab
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
