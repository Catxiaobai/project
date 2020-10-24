<template>
  <div id="failureAnalysis">
    <el-card>
      <span style="font-size: large;margin-left: 10px;margin-right: 10px">选择失效分析方法</span>
      <el-select v-model="value" placeholder="请选择" @change="onChange">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
      </el-select>
      <div id="fmea" v-show="divShow">fmea</div>
      <div id="faultTree" v-show="!divShow">tree</div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'FailureAnalysis.vue',
  data() {
    return {
      value: 'FMEA',
      options: [
        {
          value: 'FMEA',
          label: 'FMEA'
        },
        {
          value: '故障树',
          label: '故障树'
        }
      ],
      divShow: true
    }
  },
  methods: {
    onChange(val) {
      console.log(val)
      if (val === '故障树') {
        this.divShow = false
      } else {
        this.divShow = true
      }
    }
  }
}
</script>

<style scoped></style>
