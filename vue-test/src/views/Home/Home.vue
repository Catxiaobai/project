<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="12">
        <div>
          <el-card>
            <span style="white-space: pre-line;font-size:24px">{{ msg }}</span>
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
      msg:
        '项目介绍\n\n' +
        '这是项目的基本信息，接下来简单介绍一下，举个栗子\n' +
        '这是项目的基本信\n' +
        '这是项目的基本\n' +
        '这是项目的基\n' +
        '这是项目的\n' +
        '这是项目\n' +
        '这是项\n' +
        '这是\n' +
        '这\n' +
        '测\n' +
        '测试\n' +
        '测试信\n' +
        '测试信息\n' +
        '测试信\n' +
        '测试\n' +
        '测'
    }
  }
}
</script>

<style></style>
