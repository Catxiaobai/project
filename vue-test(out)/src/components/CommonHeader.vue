<template>
  <div>
    <el-card style="height: 92px;margin-top: 2px" :body-style="{ padding: '0px' }" shadow="always">
      <el-row>
        <el-col :span="6">
          <div class="tabMain">
            <el-breadcrumb separator-class="el-icon-arrow-right" style="font-size: 30px">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item :to="current.path" v-if="current">
                {{ current.label }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
        </el-col>
        <el-col :span="10">
          <div class="testWord">
            <span style="font-size: 45px;color: #2E75B6;letter-spacing: 6px;display:block;margin-top: 5px;font-family: 宋体">软件安全性验证分析平台</span>
            <span style="font-size: 30px;display: block;margin-top: 5px">Software safety verification and analysis</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div>
            <el-image :src="planeImg" style="width: 100%;height: 90px"></el-image>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'CommonHeader.vue',
  computed: {
    ...mapState({
      current: state => state.tab.currentMenu
    })
  },
  data() {
    return {
      userImg: require('../assets/images/head_1.png'),
      planeImg: require('@/assets/images/plane.jpg'),
      logoImg: require('@/assets/images/logo.png')
    }
  },
  methods: {
    collapseMenu() {
      this.$store.commit('collapseMenu')
    }
  }
}
</script>

<style lang="scss">
.tabMain {
  //background: #b3d8ff;
  float: left;
  margin-top: 30px;
  margin-left: 50px;
  font-size: 1000px;
  //width: 200px;
  //height: 100px;
  line-height: 100px; /*让黄色div中的文字内容垂直居中*/
  text-align: center; /*让文字水平居中*/
  //position: absolute;
  //top: 50%;
  //margin-top: -50px;
  //margin-left: 200px;
}
</style>
