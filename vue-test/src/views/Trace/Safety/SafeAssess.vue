<template>
  <section class="chart-container">
    <el-row>
      <el-col :span="12">
        <div id="chartPie" style="width:100%; height:400px;"></div>
      </el-col>
    </el-row>
  </section>
</template>

<script>
import echarts from 'echarts'

export default {
  data() {
    return {
      chartPie: null,
      yyy: 0,
      nnn: 0,
      tableData: []
    }
  },
  methods: {
    drawPieChart() {
      this.chartPie = echarts.init(document.getElementById('chartPie'))
      this.chartPie.setOption({
        title: {
          text: 'Test Chart',
          subtext: '测试数据',
          x: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: ['失效', '未失效', '联盟广告', '视频广告', '搜索引擎']
        },
        series: [
          {
            name: '失效序列',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [
              { value: this.yyy, name: '失效' },
              { value: this.nnn, name: '未失效' }
              // { value: 234, name: '联盟广告' },
              // { value: 135, name: '视频广告' },
              // { value: 1548, name: '搜索引擎' }
            ],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      })
    },
    drawCharts() {
      this.drawPieChart()
    },
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/invalid_list')
        .then(response => {
          this.tableData = response.data.invalid_list
          console.log(this.tableData[0].invalid_verify)
          for (var i = 0; i < this.tableData.length; i++) {
            if (this.tableData[i].invalid_verify == 'Y') {
              this.yyy++
            } else if (this.tableData[i].invalid_verify == 'N') {
              this.nnn++
            }
          }
          console.log(this.yyy)
          this.drawCharts()
        })
        .catch(function(error) {
          console.log(error)
        })
    }
  },
  created() {
    this.pageList()
  },
  mounted: function() {
    this.drawCharts()
  },
  updated: function() {
    this.drawCharts()
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  float: left;
}
.el-col {
  padding: 30px 20px;
}
</style>
