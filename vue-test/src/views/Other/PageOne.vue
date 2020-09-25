<template>
  <el-card class="echartLayout">
    <!--    <div class="echartLayout">-->
    <div id="container" style="overflow: hidden;height: 600px;width: 100%" class="test"></div>
    <!--    </div>-->
  </el-card>
</template>

<script>
import echarts from 'echarts'
import imgSrc from '../../assets/images/head_1.png'
export default {
  name: 'personRelation',
  data() {
    return {
      myChart: null,
      chartData: [],
      chartLink: []
    }
  },
  mounted() {
    this.initEchart()
  },
  methods: {
    initEchart() {
      let dom = document.getElementById('container')
      this.myChart = echarts.init(dom)
      this.chartData = this.dataEChart()
      this.chartLink = this.linkEChart()
      // let option = {
      //   tooltip: {
      //     // show: true
      //   },
      //   series: [
      //     {
      //       edgeLabel: {
      //         normal: {
      //           formatter: '{c}',
      //           show: true
      //         }
      //       },
      //       edgeSymbol: 'circle',
      //       force: {
      //         repulsion: 2000
      //       },
      //       layout: 'force',
      //       roam: true,
      //       itemStyle: {
      //         normal: {
      //           color: '#6495ED'
      //         },
      //         //鼠标放上去有阴影效果
      //         emphasis: {
      //           shadowColor: '#3721db',
      //           shadowOffsetX: 0,
      //           shadowOffsetY: 0,
      //           shadowBlur: 40
      //         }
      //       },
      //       label: {
      //         normal: {
      //           show: true
      //         }
      //       },
      //       //头像
      //       // symbol: `image://${imgSrc}`,
      //       symbolSize: 86,
      //       type: 'graph',
      //       links: this.chartLink,
      //       data: this.chartData
      //     }
      //   ]
      // }
      let option = {
        title: {
          text: ''
        },
        tooltip: {},
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        label: {
          normal: {
            show: true,
            textStyle: {
              fontSize: 12
            }
          }
        },
        legend: {
          x: 'center',
          show: false,
          data: ['1', '2', '3']
        },
        series: [
          {
            type: 'graph',
            layout: 'force',
            symbolSize: 45,
            focusNodeAdjacency: true,
            roam: true,
            categories: [
              {
                name: '1',
                itemStyle: {
                  normal: {
                    color: '#009800'
                  }
                }
              },
              {
                name: '2',
                itemStyle: {
                  normal: {
                    color: '#4592FF'
                  }
                }
              },
              {
                name: '3',
                itemStyle: {
                  normal: {
                    color: '#3592F'
                  }
                }
              }
            ],
            label: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 12
                }
              }
            },
            force: {
              repulsion: 1000
            },
            edgeSymbolSize: [4, 50],
            edgeLabel: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 10
                },
                formatter: '{c}'
              }
            },
            data: [
              {
                name: '节点0',
                draggable: true
              },
              {
                name: '节点1',
                category: 1,
                draggable: true
              },
              {
                name: '节点2',
                category: 1,
                draggable: true
              },
              {
                name: '节点3',
                category: 1,
                draggable: true
              },
              {
                name: '节点4',
                category: 1,
                draggable: true
              },
              {
                name: '节点5',
                category: 1,
                draggable: true
              },
              {
                name: '节点6',
                category: 1,
                draggable: true
              },
              // {
              //   name: '节点7',
              //   category: 1,
              //   draggable: true
              // },
              {
                name: '节点8',
                category: 1,
                draggable: true
              },
              {
                name: '节点9',
                category: 1,
                draggable: true
              },
              {
                name: '节点10',
                category: 1,
                draggable: true
              },
              {
                name: '节点11',
                category: 1,
                draggable: true
              },
              {
                name: '节点12',
                category: 1,
                draggable: true
              }
            ],
            links: [
              {
                source: 0,
                target: 1,
                category: 0,
                value: '0-1'
              },
              {
                source: 0,
                target: 2,
                value: '0-2'
              },
              {
                source: 0,
                target: 3,
                value: '0-3'
              },
              {
                source: 0,
                target: 4,
                value: '0-4'
              },
              {
                source: 1,
                target: 2,
                value: '1-2'
              },
              {
                source: 0,
                target: 5,
                value: '0-5'
              },
              {
                source: 4,
                target: 5,
                value: '4-5'
              },
              {
                source: 2,
                target: 8,
                value: '2-8'
              },
              {
                source: 0,
                target: 12,
                value: '0-12'
              },
              {
                source: 6,
                target: 11,
                value: '6-11'
              },
              {
                source: 6,
                target: 3,
                value: '6-3'
              },
              {
                source: 7,
                target: 5,
                value: '7-5'
              },
              {
                source: 9,
                target: 10,
                value: '9-10'
              },
              {
                source: 3,
                target: 10,
                value: '3-10'
              },
              {
                source: 2,
                target: 11,
                value: '2-11'
              }
            ],
            lineStyle: {
              normal: {
                opacity: 0.9,
                width: 1,
                curveness: 0
              }
            }
          }
        ]
      }
      this.myChart.setOption(option)
      this.myChart.on('click', function(params) {
        console.log(params.data) //获取点击的头像的数据信息
      })
      //去除默认的鼠标事件
      document.oncontextmenu = function() {
        return false
      }
      //新加上鼠标右击事件
      this.myChart.on('contextmenu', function(params) {
        console.log('右键事件')
        console.log(params)
      })
    },
    /**
     * 数据集合
     */
    dataEChart() {
      let data = [
        {
          name: '张1',
          id: '1',
          des: 'qwe',
          test: 'sasa'
        },
        {
          name: '张2',
          id: '2',
          des: 'qwe',
          test: 'sasa'
        },
        {
          name: '张3',
          id: '3',
          des: 'qwe',
          test: 'sasa'
        },
        {
          name: '张4',
          id: '4',
          des: 'qwe',
          test: 'sasa'
        },
        {
          name: '张5',
          id: '5',
          des: 'qwe',
          test: 'sasa'
        },
        {
          name: '张6',
          id: '6',
          des: 'qwe',
          test: 'sasa'
        },
        {
          name: '张7',
          id: '7',
          des: 'qwe',
          test: 'sasa'
        },
        {
          name: '张8',
          id: '8',
          des: 'qwe',
          test: 'sasa'
        }
      ]
      return data
    },
    /**
     * 关系数据集合
     */
    linkEChart() {
      let dataLink = [
        { value: '同事', source: '1', target: '2' },
        { value: '同事', source: '1', target: '3' },
        { value: '同事', source: '1', target: '4' },
        { value: '同学', source: '1', target: '5' },
        { value: '同学', source: '1', target: '6' },
        { value: '同学', source: '1', target: '7' },
        { value: '爸爸', source: '1', target: '8' }
      ]
      return dataLink
    }
  }
}
</script>

<style lang="scss" scoped>
.echartLayout {
  margin: auto;
  /*position: absolute;*/
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  height: 600px;
  width: 100%;
}
</style>
