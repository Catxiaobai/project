<template>
  <div id="failureAnalysis">
    <el-card>
      <span style="font-size: large;margin-left: 10px;margin-right: 10px">选择失效分析方法</span>
      <el-select v-model="value" placeholder="请选择" @change="onChange">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
      </el-select>
      <div id="fmea" v-show="divShow" style="margin-top: 20px">
        <div id="table">
          <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelection">
            <el-table-column prop="id" label="序号" width="80" align="center"> </el-table-column>
            <el-table-column prop="type" label="失效描述" width="180" align="center"> </el-table-column>
            <el-table-column prop="reason" label="软件失效原因" width="120" align="center"> </el-table-column>
            <el-table-column label="软件失效影响" align="center">
              <el-table-column prop="local_influence" label="本层影响" width="120" align="center"> </el-table-column>
              <el-table-column prop="upper_influence" label="上一层影响" width="120" align="center"> </el-table-column>
              <el-table-column prop="system_influence" label="系统影响" width="120" align="center"> </el-table-column>
            </el-table-column>
            <el-table-column prop="influence_level" label="影响等级" width="180" align="center"> </el-table-column>
            <el-table-column prop="improve" label="改进措施" align="center"> </el-table-column>
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
          // console.log(response.data.analysis_list)
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
      // let list = this.data.filter((item, index) => item.name.includes(this.search))
      let list = this.data
      this.tableData = list.filter(
        (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
      )
      this.pagination.total = list.length
      // console.log(this.tableData)
    }
  }
}
</script>

<style scoped></style>
