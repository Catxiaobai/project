<template>
  <div id="common-header">
    <div id="top">
      <div id="left-content">
        <div id="imgLogo">
          <el-image :src="imgLogo"></el-image>
        </div>
        <div id="leftTitle">
          <span>软件安全性分析与设计工具</span>
        </div>
      </div>
      <div id="right-content">
        <div id="rightTitle">
          <el-link>首页</el-link> |
          <el-link>退出</el-link>
        </div>
      </div>
    </div>
    <div id="bottom"></div>
  </div>
</template>

<script>
export default {
  name: 'CommonHeader.vue',
  data() {
    return {
      imgLogo: require('@/assets/image/logo.png')
    }
  }
}
</script>

<style scoped lang="scss">
#common-header {
  background: #f5f9f9;
  width: 100%;
  height: 96px;
  display: flex;
  flex-direction: column;
  #top {
    display: flex;
    height: 60px;
    #left-content {
      width: 100%;
      display: flex;
      #imgLogo {
        //height: 60px;
        width: 65px;
      }
      #leftTitle {
        height: 60px;
        font-size: xx-large;
        font-weight: bold;
        font-family: 楷体;
        margin-top: 10px;
        margin-left: 20px;
      }
    }
    #right-content {
      width: 100px;
      float: right;
      #rightTitle {
        margin-top: 20px;
      }
    }
  }
  #bottom {
    height: 36px;
    background: skyblue;
    //z-index: 12;
  }
}
</style>
