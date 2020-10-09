<template>
  <div class="test">
    <!--    <el-row :gutter="20">-->
    <!--      <el-col :span="12">-->
    <!--        <el-card style="height: 480px">-->
    <!--          &lt;!&ndash;            <span style="white-space: pre-line;font-size:24px;width: 100px;height: 100px" v-show="test" @dblclick="test = false">{{ msg }}</span>&ndash;&gt;-->
    <!--          <el-input type="textarea" class="homeMsg" autosize v-model="msg"> </el-input>-->
    <!--        </el-card>-->
    <!--      </el-col>-->
    <!--    <el-image :src="src1" alt="" style="height: 100%;width: 100%;padding: 0"></el-image>-->
    <div>
      <el-card>
        <el-image :src="src1" alt="" style="height: 420px;width: 100%"></el-image>
        <el-input type="textarea" class="homeMsg" autosize v-model="msg"> </el-input>
      </el-card>
    </div>

    <!--    </el-row>-->
  </div>
</template>

<script>
export default {
  name: 'Home.vue',
  data() {
    return {
      src1: require('@/assets/images/homePage.jpg'),
      test: true,
      msg:
        '    平台基于软件场景进行软件系统安全性分析验证。' +
        '软件场景涵盖软件系统不同状态，描述软件系统的各种使用方式，包含使用场景及失效场景。平台设计软件场景的形式化模式，并维护软件场景。平台基于使用场景刻画软件系统的模型，并实现软件系统开发及设计人员与模型的动态交互。并对模型进行完整性验证；同时可依据失效场景对模型进行安全性验证分析，实现对软件系统的安全性进行评估。'
    }
  }
}
</script>

<style lang="scss">
.test {
  .el-textarea__inner {
    border: none;
    resize: none;
    font-weight: bold;
    font-size: 24px;
    font-family: 楷体;
  }
}
</style>
