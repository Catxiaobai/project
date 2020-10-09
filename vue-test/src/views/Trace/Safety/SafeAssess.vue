<template>
  <div>
    <div class="divHelp">
      <el-popover placement="bottom" trigger="click">
        <!--        <el-button slot="reference">click 激活</el-button>-->
        <p>此页面展示安全性评估结果</p>
        <!--        <p>对模型每次操作都会触发验证，提示操作是否可行</p>-->
        <br />
        <p>danger：存在安全隐患</p>
        <p>success：在该模型中验证结果为安全</p>
        <p>null：还未验证的场景</p>
        <!--        <p>删除边：鼠标左键单击进行选定，然后点击键盘上的"delete"或"Backspace"键</p>-->
        <!--        <p>移动节点：鼠标左键单击进行选定，将鼠标移至节点中心处，长按鼠标左键即可拖拽移动</p>-->
        <el-button icon="el-icon-message-solid" circle slot="reference"></el-button>
      </el-popover>
      <el-popover placement="bottom" trigger="click">
        <!--        <el-button slot="reference">click 激活</el-button>-->
        <div>
          <p>此页面展示安全性评估结果</p>
          <!--        <p>对模型每次操作都会触发验证，提示操作是否可行</p>-->
          <br />
          <p>danger：存在安全隐患</p>
          <p>success：在该模型中验证结果为安全</p>
          <p>null：还未验证的场景</p>
        </div>
        <el-button type="text" slot="reference">操作提示</el-button>
      </el-popover>
    </div>
    <el-card>
      <section class="chart-container" style="margin-left: 25%">
        <el-row>
          <el-col :span="12">
            <div id="chartPie" style="width:100%; height:400px;"></div>
          </el-col>
        </el-row>
      </section>
    </el-card>
  </div>
</template>

<script>
import echarts from 'echarts'

export default {
  data() {
    return {
      chartPie: null,
      yyy: 2,
      nnn: 3,
      resData: {
        numDanger: 0,
        numSuccess: 0,
        numNull: 0
      },
      tableData: []
    }
  },
  methods: {
    drawPieChart() {
      this.chartPie = echarts.init(document.getElementById('chartPie'))
      this.chartPie.setOption({
        title: {
          text: 'Evaluation Result',
          subtext: '安全性评估结果',
          x: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: ['danger', 'success', 'null']
        },
        series: [
          {
            name: '失效场景验证',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [
              { value: this.resData.numDanger, name: 'danger' },
              { value: this.resData.numSuccess, name: 'success' },
              { value: this.resData.numNull, name: 'null' }
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
            if (this.tableData[i].invalid_verify == 'danger') {
              this.resData.numDanger++
            } else if (this.tableData[i].invalid_verify == 'success') {
              this.resData.numSuccess++
            } else if (this.tableData[i].invalid_verify == 'null') {
              this.resData.numNull++
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
.divHelp {
  margin-left: 1100px;
  height: 40px;
  margin-top: -40px;
}
</style>
