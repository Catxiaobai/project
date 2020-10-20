<template>
  <div id="home">
    <div id="body">
      <el-card id="bodyCard">
        <el-image class="bodyImg" :src="bodyImg"> </el-image>
        <el-input class="bodyMsg" type="textarea" autosize v-model="bodyMsg"> </el-input>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'home',
  data() {
    return {
      bodyImg: require('@/assets/images/homePage.jpg'),
      bodyMsg:
        '    平台基于软件场景进行软件系统安全性分析验证。' +
        '软件场景描述软件系统的各种使用方式，涵盖软件系统不同状态及各种操作，包含使用场景及风险场景。' +
        '平台设计软件场景的形式化模式，并维护软件场景。平台基于使用场景刻画软件系统的模型，并实现软件系统开发及设计人员与模型的动态交互。' +
        '并对模型进行完整性验证；同时可依据风险场景对模型进行安全性验证分析，实现对软件系统的安全性进行评估。'
    }
  },
  methods: {}
}
</script>

<style scoped lang="scss">
#body {
  height: 100%;
  width: 100%;
}
</style>
<style lang="scss">
.bodyMsg {
  .el-textarea__inner {
    border: none;
    resize: none;
    font-weight: bold;
    font-size: 24px;
    font-family: 楷体;
  }
}
.bodyImg {
  width: 100%;
  .el-image__inner {
    height: 435px;
    width: 100%;
  }
}
</style>
