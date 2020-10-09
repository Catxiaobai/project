<template>
  <div class="bottom">
    <span style="margin-left: 10px;margin-top: 10px">>项目简介</span>
    <!--    todo: 项目选择不起作用-->
    <el-select v-model="value" placeholder="请选择项目" style="margin-left: 40px">
      <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled"> </el-option>
    </el-select>
    <!--    <el-card class="bottom"></el-card>-->
  </div>
</template>

<script>
export default {
  name: 'InnerMain.vue',
  data() {
    return {
      options: [
        {
          value: '选项1',
          label: '项目一'
        },
        {
          value: '选项2',
          label: '项目二',
          disabled: true
        }
      ],
      value: ''
    }
  }
}
</script>

<style lang="scss" scoped>
.bottom {
  background-color: #eef4f8;
  //background-color: #66cff0;
  height: 40px;
}
</style>
