<template>
  <div class="login">
    <div class="background">
      <el-image class="bgImg" :src="bgImg"></el-image>
    </div>
    <div class="front">
      <el-card>
        <span class="title">软件安全性分析与设计工具</span>
        <el-form class="loginForm" :model="loginForm" :rules="rules">
          <el-form-item prop="name">
            <el-input v-model="loginForm.name" placeholder="用户账号" value="test"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input type="password" v-model="loginForm.password" placeholder="密码"></el-input>
          </el-form-item>
        </el-form>
        <el-checkbox v-model="checked" @change="remember(checked)">记住密码</el-checkbox>
        <div class="action">
          <el-button type="primary" @click="gotolink" style="width: 240px">登录</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bgImg: require('@/assets/images/background.jpg'),
      loginForm: {
        name: 'admin',
        password: 'admin'
      },
      rules: {
        name: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
        ],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      },
      checked: true
    }
  },
  methods: {
    gotolink() {
      console.log(this.loginForm.name)
      this.$router.replace('/main')
    },
    remember(data) {
      // console.log(data)
      if (data) {
        this.loginForm.name = 'admin'
        this.loginForm.password = 'admin'
      } else {
        this.loginForm.name = ''
        this.loginForm.password = ''
      }
    }
  }
}
</script>

<style lang="scss">
.title {
  text-align: center;
  margin-left: 20%;
}
.login {
  height: 100%;
  width: 100%;
}
.background {
  height: 100%;
  width: 100%;
  z-index: 0;
  position: absolute;
}
.bgImg {
  height: 100%;
}
.front {
  z-index: 1;
  position: absolute;
  margin-top: 15%;
  margin-left: 40%;
  width: 350px;
  height: 500px;
}
.loginForm {
  margin-top: 20px;
}
.action {
  margin-top: 20px;
  text-align: center;
}
</style>
