<template>
  <div id="requirements">
    <el-card>
      <div style="margin-top: 20px">
        <div id="table">
          <download-excel :data="tableData" :fields="json_fields" name="output.xls">
            <el-button type="primary" style="margin-bottom: 20px;margin-left: 90%">导出</el-button>
          </download-excel>
          <el-table :data="tableData" border style="width: 100%">
            <el-table-column prop="id" label="序号" width="80" align="center"> </el-table-column>
            <el-table-column prop="describe" label="失效描述" width="180" align="center"> </el-table-column>
            <el-table-column prop="improve" label="改进措施" width="180" align="center"> </el-table-column>
            <el-table-column prop="demand" label="软件安全性需求" align="center"> </el-table-column>
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
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Requirements.vue',
  data() {
    return {
      json_fields: {
        序号: 'id',
        失效描述: 'describe',
        改进措施: 'improve',
        软件安全性需求: 'demand'
      },
      tableData: [],
      pagination: {
        limit: 7, //每页显示条数
        total: 0, //项目总数
        page: 1 //第几页
      },
      search: '',
      itemInfo: ''
    }
  },
  created() {
    this.getItemInfo()
    this.pageList()
  },
  methods: {
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
        .post(this.Global_Api + '/api/demand_list', this.itemInfo)
        .then(response => {
          console.log(response.data.demand_list)
          this.data = response.data.demand_list
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
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('失效分析', this.itemInfo)
    }
  }
}
</script>

<style scoped></style>
