<template>
  <div>
    <el-card>
      <i>这是项目一的内容</i>
      <p>Test</p>
      <p>Test</p>
      <p>Test</p>
      <p>Test</p>
      <p>Test</p>
      <p>Test</p>
      <!--    </el-card>-->
      <!--    <el-card style="margin-top: 20px">-->
      <el-button type="primary" @click="gotolink" style="margin-top: 30px;margin-left: 44%">进入项目一</el-button>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ItemOne.vue',
  methods: {
    gotolink() {
      this.$router.replace('/trace')
    }
  }
}
</script>

<style scoped></style>
