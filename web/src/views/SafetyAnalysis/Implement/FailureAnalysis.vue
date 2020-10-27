<template>
  <div id="failureAnalysis">
    <el-card>
      <span style="font-size: large;margin-left: 10px;margin-right: 10px">选择失效分析方法</span>
      <el-select v-model="value" placeholder="请选择" @change="onChange">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
      </el-select>
      <div id="fmea" v-show="divShow" style="margin-top: 20px">
        <div id="table">
          <el-table :data="tableData" border style="width: 100%">
            <el-table-column prop="id" label="序号" width="80" align="center"> </el-table-column>
            <el-table-column prop="describe" label="失效描述" width="180" align="center"> </el-table-column>
            <el-table-column prop="reason" label="软件失效原因" width="120" align="center">
              <template slot-scope="scope">
                <el-input class="tableCell" type="textarea" autosize v-model="scope.row.reason" @change="saveData(scope.row)"> </el-input>
              </template>
            </el-table-column>
            <el-table-column label="软件失效影响" align="center">
              <el-table-column prop="local_influence" label="本层影响" width="120" align="center">
                <template slot-scope="scope">
                  <el-input class="tableCell" type="textarea" autosize v-model="scope.row.local_influence" @change="saveData(scope.row)"> </el-input>
                </template>
              </el-table-column>
              <el-table-column prop="upper_influence" label="上一层影响" width="120" align="center">
                <template slot-scope="scope">
                  <el-input class="tableCell" type="textarea" autosize v-model="scope.row.upper_influence" @change="saveData(scope.row)"> </el-input>
                </template>
              </el-table-column>
              <el-table-column prop="system_influence" label="系统影响" width="120" align="center">
                <template slot-scope="scope">
                  <el-input class="tableCell" type="textarea" autosize v-model="scope.row.system_influence" @change="saveData(scope.row)"> </el-input>
                </template>
              </el-table-column>
            </el-table-column>
            <el-table-column prop="influence_level" label="影响等级" width="180" align="center">
              <template slot-scope="scope">
                <el-select v-model="scope.row.influence_level" placeholder="请选择" style="border: 0;margin: 0;padding: 0" @change="saveData(scope.row)">
                  <el-option v-for="item in options2" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                </el-select>
              </template>
            </el-table-column>
            <el-table-column prop="improve" label="改进措施" align="center">
              <template slot-scope="scope">
                <el-input class="tableCell" type="textarea" autosize v-model="scope.row.improve" @change="saveData(scope.row)"> </el-input>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div id="page">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="pagination.page"
            :page-sizes="[1, 2, 5, 7, 10]"
            :page-size="pagination.limit"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total"
            style="margin-left: 30%;margin-top: 20px"
          >
          </el-pagination>
        </div>
      </div>
      <div id="faultTree" v-show="!divShow">
        <div style="margin-top: 20px">
          <div id="table2">
            <el-table :data="tableData2" border style="width: 100%">
              <el-table-column prop="id" label="事件编号" width="80" align="center"> </el-table-column>
              <el-table-column prop="name" label="事件名称" width="180" align="center"> </el-table-column>
              <el-table-column prop="logic" label="逻辑门" width="180" align="center">
                <template slot-scope="scope">
                  <el-select v-model="scope.row.logic" placeholder="请选择" style="border: 0;margin: 0;padding: 0">
                    <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column prop="node" label="节点数" align="center">
                <template slot-scope="scope">
                  <el-input class="tableCell" type="textarea" autosize v-model="scope.row.node"> </el-input>
                </template>
              </el-table-column>
              <el-table-column prop="event" label="节点事件" align="center">
                <template slot-scope="scope">
                  <el-input class="tableCell" type="textarea" autosize v-model="scope.row.event"> </el-input>
                </template>
              </el-table-column>
            </el-table>
            <el-button style="width: 100%;background: beige">add</el-button>
          </div>
          <div id="page2">
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="pagination.page"
              :page-sizes="[1, 2, 5, 7, 10]"
              :page-size="pagination.limit"
              layout="total, sizes, prev, pager, next, jumper"
              :total="pagination.total"
              style="margin-left: 30%;margin-top: 20px"
            >
            </el-pagination>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'FailureAnalysis.vue',
  data() {
    return {
      value: 'FMEA',
      tableData2: [
        {
          id: 0,
          name: 'T1',
          logic: '与门',
          node: '3',
          event: 'G1、G2、G3'
        },
        {
          id: 1,
          name: 'G1',
          logic: '与门',
          node: '3',
          event: 'G1、G2、G3'
        },
        {
          id: 2,
          name: 'G2',
          logic: '或门',
          node: '2',
          event: 'G1、G2、G3'
        },
        {
          id: 3,
          name: 'G3',
          logic: '与门',
          node: '2',
          event: 'G1、G2、G3'
        },
        {
          id: 4,
          name: 'G4',
          logic: '或门',
          node: '2',
          event: 'G1、G2、G3'
        },
        {
          id: 5,
          name: 'G5',
          logic: '或门',
          node: '2',
          event: 'G1、G2、G3'
        }
      ],
      options3: [
        {
          value: '与门',
          label: '与门'
        },
        {
          value: '或门',
          label: '或门'
        }
      ],
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
      options2: [
        {
          value: '灾难性的',
          label: '灾难性的'
        },
        {
          value: '严重的',
          label: '严重的'
        },
        {
          value: '一般的',
          label: '一般的'
        },
        {
          value: '轻微的',
          label: '轻微的'
        }
      ],
      divShow: true,
      tableData: [],
      pagination: {
        limit: 7, //每页显示条数
        total: 0, //项目总数
        page: 1 //第几页
      },
      search: '' //搜索框
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    onChange(val) {
      console.log(val)
      if (val === '故障树') {
        this.divShow = false
      } else {
        this.divShow = true
      }
    },
    handleSizeChange(val) {
      // 当每页数量改变
      console.log(`每页 ${val} 条`)
      this.pagination.limit = val
      this.getList()
    },
    handleCurrentChange(val) {
      // 当当前页改变
      console.log(`当前页: ${val}`)
      this.pagination.page = val
      this.getList()
    },
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/fmea_list')
        .then(response => {
          console.log(response.data.fmea_list)
          this.data = response.data.fmea_list
          this.getList()
        })
        .catch(function(error) {
          console.log(error)
        })
      // this.data = this.tableData
      // this.getList()
    },
    getList() {
      // 处理数据，根据表格中name字段来筛选
      let list = this.data.filter((item, index) => item.describe.includes(this.search))
      // let list = this.data
      this.tableData = list.filter(
        (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
      )
      this.pagination.total = list.length
      // console.log(this.tableData)
    },
    saveData(val) {
      console.log(val)
      this.$http
        .post('http://127.0.0.1:8000/api/edit_fmea', val)
        .then(response => {
          if (response.data.error_code === 0) {
            this.pageList()
          } else {
            console.log(response.data)
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped></style>
<style lang="scss">
.tableCell {
  .el-textarea__inner {
    border: none;
    resize: none;
  }
}
</style>
