<template>
  <div class="bottom">
    <span class="msg">{{ itemMsg }}</span>
    <el-select v-model="value" placeholder="请选择项目" style="margin-left: 40px" @change="selectItem(value)" clearable>
      <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled"> </el-option>
    </el-select>
    <!--    <el-card class="bottom"></el-card>-->
  </div>
</template>

<script>
export default {
  name: 'InnerMain.vue',
  props: ['itemMsg'],
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
  },
  methods: {
    selectItem(data) {
      if (data === '选项1') {
        // todo: 改变项目简介

        this.$emit('transferItemMsg', '>ATM系统')
        console.log('test')
      } else if (data === '') {
        // todo: 改回项目简介
        this.$emit('transferItemMsg', '>项目简介')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.bottom {
  background-color: #eef4f8;
  //background-color: #66cff0;
  height: 40px;
  line-height: 40px;
}
.msg {
  margin-left: 10px;
}
</style>
