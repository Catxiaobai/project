<template>
  <el-container style="height: 100%">
    <el-header height="90px"><inner-header></inner-header></el-header>
    <el-container>
      <el-aside width="240px"><inner-aside></inner-aside></el-aside>
      <inner-tab></inner-tab>
      <el-main>
        <inner-main style="margin-top: -10px" @transferItemMsg="getMsg" :item-msg="itemMsg"></inner-main>
        <!--        <Home @transferItemMsg="getMsg" v-show="true"></Home>-->
        <router-view> </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import InnerHeader from '@/components/InnerHeader'
import InnerAside from '@/components/InnerAside'
import InnerTab from '@/components/InnerTab'
import InnerMain from '@/components/InnerMain'
// import Home from '@/views/Home/Home'
export default {
  name: 'Test.vue',
  components: {
    InnerHeader,
    InnerAside,
    InnerTab,
    InnerMain
    // Home
  },
  data() {
    return {
      itemMsg: '>系统简介'
    }
  },
  methods: {
    getMsg(data) {
      this.itemMsg = data
      console.log(data)
    }
  }
}
</script>

<style lang="scss" scoped>
.el-header {
  background-color: #deebf7;
}
.el-main {
  background-color: #f5f5f5;
}
//.el-menu-vertical-demo:not(.el-menu--collapse) {
//  width: 200px;
//  min-height: 400px;
//}
</style>
