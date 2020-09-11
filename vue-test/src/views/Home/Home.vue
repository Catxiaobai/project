<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="12">
        <div>
          <el-card style="height: 480px">
            <!--            <span style="white-space: pre-line;font-size:24px;width: 100px;height: 100px" v-show="test" @dblclick="test = false">{{ msg }}</span>-->
            <el-input type="textarea" autosize v-model="msg"> </el-input>
          </el-card>
        </div>
      </el-col>
      <el-col :span="12">
        <div>
          <el-card>
            <el-image :src="src1" alt=""></el-image>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Home.vue',
  data() {
    return {
      src1: require('@/assets/images/company.png'),
      test: true,
      msg:
        '项目介绍\n\n' +
        '这是项目的基本信息，接下来简单介绍一下\n' +
        '这是项目的基本信\n' +
        '这是项目的基本\n' +
        '这是项目的基\n' +
        '这是项目的\n' +
        '这是项目\n' +
        '这是项\n' +
        '这是\n' +
        '这\n'
    }
  }
}
</script>

<style>
.el-textarea__inner {
  border: none;
  resize: none;
  font-weight: bold;
  font-size: 24px;
  font-family: 楷体;
}
</style>
