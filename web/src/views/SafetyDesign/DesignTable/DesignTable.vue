<template>
  <div id="designTable">
    <el-card>
      <div style="margin-top: 20px">
        <div id="table">
          <el-button type="primary" style="margin-bottom: 20px;margin-left: 90%">导出</el-button>
          <el-table :data="tableData" border style="width: 100%">
            <el-table-column prop="id" label="序号" width="50" align="center"> </el-table-column>
            <el-table-column prop="element" label="要素" width="150" align="center"> </el-table-column>
            <el-table-column prop="type" label="类别" width="150" align="center"> </el-table-column>
            <el-table-column prop="describe" label="准则描述" width="180" align="center"> </el-table-column>
            <el-table-column prop="problem" label="问题描述" width="180" align="center"> </el-table-column>
            <el-table-column prop="complete" label="完善措施" align="center"> </el-table-column>
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
  name: 'DesignTable.vue',
  data() {
    return {
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
        .post('http://127.0.0.1:8000/api/complete_list', this.itemInfo)
        .then(response => {
          console.log(response.data.complete_list)
          this.data = response.data.complete_list
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
    }
  }
}
</script>

<style scoped></style>
