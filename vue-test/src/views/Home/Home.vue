<template>
  <div class="test">
    <!--    <div class="divHome">-->
    <!--      <inner-main :item-msg="itemMsg" style="margin-top: 40px"></inner-main>-->
    <!--    </div>-->
    <!--    <div class="selectItem">-->
    <!--      <el-select v-model="value" placeholder="请选择项目" style="margin-left: 40px" @change="selectItem(value)" clearable>-->
    <!--        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled"> </el-option>-->
    <!--      </el-select>-->
    <!--    </div>-->
    <div>
      <el-card>
        <el-image :src="src1" alt="" style="height: 420px;width: 100%"></el-image>
        <el-input type="textarea" class="homeMsg" autosize v-model="msg"> </el-input>
      </el-card>
    </div>
  </div>
</template>

<script>
// import InnerMain from '@/components/InnerMain'
export default {
  name: 'Home.vue',
  // components: { InnerMain },
  data() {
    return {
      src1: require('@/assets/images/homePage.jpg'),
      test: true,
      options: [
        {
          value: '1',
          label: '项目一'
        },
        {
          value: '2',
          label: '项目二',
          disabled: true
        }
      ],
      value: '',
      itemMsg: '>项目简介',
      msg:
        '    平台基于软件场景进行软件系统安全性分析验证。' +
        '软件场景涵盖软件系统不同状态，描述软件系统的各种使用方式，包含使用场景及失效场景。平台设计软件场景的形式化模式，并维护软件场景。平台基于使用场景刻画软件系统的模型，并实现软件系统开发及设计人员与模型的动态交互。并对模型进行完整性验证；同时可依据失效场景对模型进行安全性验证分析，实现对软件系统的安全性进行评估。'
    }
  },
  methods: {
    // selectItem(data) {
    //   if (data === '1') {
    //
    //     this.$emit('transferItemMsg', '>ATM系统')
    //     console.log('test')
    //   } else if (data === '') {
    //     this.$emit('transferItemMsg', '>项目简介')
    //   }
    // }
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
.selectItem {
  margin-left: 900px;
  margin-top: -40px;
}
</style>
