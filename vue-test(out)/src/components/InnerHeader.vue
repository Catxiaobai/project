<template>
  <div>
    <el-card style="height: 82px;margin-top: 2px" :body-style="{ padding: '0px' }" shadow="always">
      <el-row>
        <el-col :span="3">
          <div @click="gotolink">
            <el-image :src="logoImg" style="height: 80px;width: 130px;margin-left: 30px"></el-image>
          </div>
        </el-col>
        <el-col :span="10">
          <div class="testWord" @click="gotolink">
            <span style="font-size: 45px;color: #2E75B6;letter-spacing: 6px;display:block;margin-top: 2px;font-family: 宋体">软件安全性验证分析平台</span>
            <span style="font-size: 30px;display: block;margin-top: 2px">Software safety verification and analysis</span>
          </div>
        </el-col>
        <el-col :span="9">
          <div @click="gotolink">
            <el-image :src="planeImg" style="width: 100%;height: 80px"></el-image>
          </div>
        </el-col>
        <el-col :span="2">
          <!--          <el-button icon="el-icon-circle-close" style="margin-left: 15px;margin-top: 20px" type="danger" @click="backLogin">退出</el-button>-->
          <!--          <el-image :src="headImg" style="width: 100%;height: 80px" ></el-image>-->
          <div class="userMsg">
            <!--            <el-dropdown trigger="click">-->
            <!--              <span><img :src="headImg" class="user"/></span>-->
            <!--              <el-dropdown-menu slot="dropdown">-->
            <!--                &lt;!&ndash;                <el-dropdown-item icon="el-icon-plus">个人中心</el-dropdown-item>&ndash;&gt;-->
            <!--                <el-dropdown-item icon="el-icon-circle-close" @click.native="backLogin">退出</el-dropdown-item>-->
            <!--              </el-dropdown-menu>-->
            <!--            </el-dropdown>-->
            <p>admin</p>
            <br />
            <el-link @click="backLogin">退出</el-link>
            <!--            <el-button type="text">退出</el-button>-->
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
  <!--  <header>-->
  <!--    <div class="l-content">-->
  <!--      <el-button plain icon="el-icon-menu" circle size="large" @click="collapseMenu"></el-button>-->
  <!--      <el-breadcrumb separator="/">-->
  <!--        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>-->
  <!--        <el-breadcrumb-item :to="{ path: '/trace' }">场景</el-breadcrumb-item>-->
  <!--        <el-breadcrumb-item :to="current.path" v-if="current">-->
  <!--          {{ current.label }}-->
  <!--        </el-breadcrumb-item>-->
  <!--      </el-breadcrumb>-->
  <!--    </div>-->
  <!--    <div>-->
  <!--      <el-image :src="planeImg" alt=""></el-image>-->
  <!--    </div>-->
  <!--      <div class="r-content">-->
  <!--        <el-dropdown trigger="click" size="mini">-->
  <!--          <span class="el-dropdown-link"><img :src="userImg" class="user"/></span>-->
  <!--          <el-dropdown-menu slot="dropdown">-->
  <!--            <el-dropdown-item icon="el-icon-plus">个人中心</el-dropdown-item>-->
  <!--            <el-dropdown-item icon="el-icon-circle-plus">退出</el-dropdown-item>-->
  <!--          </el-dropdown-menu>-->
  <!--        </el-dropdown>-->
  <!--      </div>-->
  <!--  </header>-->
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'InnerHeader.vue',
  inject: ['reload'],
  // computed: {
  //   ...mapState({
  //     current: state => state.inner.currentMenu
  //   })
  // },
  data() {
    return {
      // userImg: require('../assets/images/head_1.png'),
      planeImg: require('@/assets/images/plane.jpg'),
      logoImg: require('@/assets/images/logo.png'),
      headImg: require('@/assets/images/userHead2.jpg')
    }
  },
  methods: {
    // collapseMenu() {
    //   this.$store.commit('collapseMenu')
    // }
    gotolink() {
      this.$router.replace('/trace')
    },
    backLogin() {
      // console.log('tets')
      // this.reload()
      // this.$router.replace('/')
      window.location.href = '/'
    }
  }
}
</script>

<style lang="scss" scoped>
header {
  display: flex;
  height: 100%;
  align-items: center;
  justify-content: space-between;
}

//.l-content {
//  display: flex;
//  align-items: center;
//  .el-button {
//    margin-right: 20px;
//  }
//}
.r-content {
  //background-color: red;
  height: 100px;
  .user {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    margin-left: 30px;
    margin-top: 10px;
  }
}
.userMsg {
  margin-left: 25%;
  margin-top: 10%;
  .el-link {
    text-decoration: underline;
  }
}
</style>
